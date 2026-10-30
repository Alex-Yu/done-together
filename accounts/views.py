import secrets

from allauth.account.adapter import get_adapter
from allauth.account.models import EmailAddress, EmailConfirmation
from allauth.account.views import ConfirmEmailView, PasswordResetFromKeyView
from django import forms
from django.db import transaction
from django.http import Http404
from django.shortcuts import redirect, render
from django.utils.decorators import method_decorator
from django.views import View
from django.views.decorators.debug import sensitive_post_parameters

from .tokens import OneHourResetTokenGenerator


class PrivateConfirmEmailView(ConfirmEmailView):
    def get(self, *args, **kwargs):
        try:
            confirmation = self.get_object()
        except Http404:
            return render(
                self.request,
                "account/email_confirm.html",
                {"confirmation": None},
                status=400,
            )
        self.logout_other_user(confirmation)
        self.request.session["private_email_confirmation"] = confirmation.key
        flow = secrets.token_urlsafe(18)
        self.request.session["private_email_confirmation_flow"] = flow
        return redirect("account_confirm_email_session", flow=flow)

    def get_object(self, queryset=None):
        confirmation = super().get_object(queryset)
        if confirmation.sent is None or confirmation.key_expired():
            raise Http404()
        return confirmation

    def post(self, *args, **kwargs):
        with transaction.atomic():
            # Lock before reloading validity; a competing request sees consumption.
            if (
                not EmailConfirmation.objects.select_for_update()
                .filter(key=self.kwargs["key"])
                .exists()
            ):
                raise Http404()
            return super().post(*args, **kwargs)


class SessionConfirmEmailView(PrivateConfirmEmailView):
    def dispatch(self, request, *args, **kwargs):
        key = request.session.get("private_email_confirmation")
        if not key or not secrets.compare_digest(
            str(kwargs.get("flow", "")),
            request.session.get("private_email_confirmation_flow", ""),
        ):
            return render(
                request,
                "account/email_confirm.html",
                {"confirmation": None},
                status=400,
            )
        kwargs["key"] = key
        self.kwargs = kwargs
        return super().dispatch(request, *args, **kwargs)

    def get(self, *args, **kwargs):
        return ConfirmEmailView.get(self, *args, **kwargs)

    def post(self, *args, **kwargs):
        response = super().post(*args, **kwargs)
        self.request.session.pop("private_email_confirmation", None)
        self.request.session.pop("private_email_confirmation_flow", None)
        return response


@method_decorator(sensitive_post_parameters("password1", "password2"), name="dispatch")
class PrivatePasswordResetView(PasswordResetFromKeyView):
    def form_valid(self, form):
        with transaction.atomic():
            locked = (
                type(self.reset_user)
                .objects.select_for_update()
                .get(pk=self.reset_user.pk)
            )
            if not OneHourResetTokenGenerator().check_token(locked, self.key):
                form.add_error(
                    None,
                    "This link is invalid or has expired. Request a new password reset.",
                )
                return self.form_invalid(form)
            form.user = locked
            self.reset_user = locked
            return super().form_valid(form)


class ResendForm(forms.Form):
    email = forms.EmailField(
        label="Email", widget=forms.EmailInput(attrs={"autocomplete": "email"})
    )


class ResendVerificationView(View):
    def get(self, request):
        return render(request, "accounts/resend.html", {"form": ResendForm()})

    def post(self, request):
        form = ResendForm(request.POST)
        if form.is_valid():
            email = form.cleaned_data["email"].strip().lower()
            address = EmailAddress.objects.filter(
                email__iexact=email, verified=False
            ).first()
            if address:
                address.send_confirmation(request)
            else:
                # Equal delivery attempt/status for unknown/already verified addresses.
                get_adapter(request).send_mail(
                    "account/email/verification_request", email, {}
                )
            return render(request, "accounts/resend.html", {"sent": True})
        return render(request, "accounts/resend.html", {"form": form})
