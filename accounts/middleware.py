from django.db import DatabaseError
from django.http import HttpResponse
from django.shortcuts import render
from django.utils.cache import add_never_cache_headers

from .adapter import EmailDeliveryError
from .limits import allow_source


class AccountSafetyMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        if (
            request.path.startswith(("/accounts/", "/households/"))
            and request.method == "POST"
        ):
            try:
                allowed = allow_source(request.META.get("REMOTE_ADDR", "unknown"))
            except DatabaseError:
                response = render(request, "accounts/unavailable.html", status=503)
                add_never_cache_headers(response)
                response["Referrer-Policy"] = self.referrer_policy(request.path)
                return response
            if not allowed:
                response = HttpResponse(
                    "Too many requests. Please try again in a minute.", status=429
                )
                response["Retry-After"] = "60"
                add_never_cache_headers(response)
                response["Referrer-Policy"] = self.referrer_policy(request.path)
                return response
        response = self.get_response(request)
        if request.path.startswith(("/accounts/", "/households/")):
            add_never_cache_headers(response)
            response["Referrer-Policy"] = self.referrer_policy(request.path)
        return response

    def process_exception(self, request, exception):
        if isinstance(exception, EmailDeliveryError):
            return render(request, "accounts/delivery_failed.html", status=503)
        if isinstance(exception, DatabaseError) and request.path.startswith(
            "/accounts/"
        ):
            return render(request, "accounts/unavailable.html", status=503)
        return None

    @staticmethod
    def referrer_policy(path):
        private_verification = (
            path.startswith("/accounts/confirm-email/")
            and path != "/accounts/confirm-email/"
        )
        private_reset = (
            path.startswith("/accounts/password/reset/key/")
            and not path.endswith("-set-password/")
            and not path.endswith("/done/")
        )
        private_invitation = path.startswith("/households/invitations/")
        return (
            "no-referrer"
            if private_verification or private_reset or private_invitation
            else "same-origin"
        )
