from smtplib import SMTPException

from allauth.account.adapter import DefaultAccountAdapter

from .limits import authenticate_identity


class EmailDeliveryError(Exception):
    """Recoverable delivery failure without provider/credential details."""


class AccountAdapter(DefaultAccountAdapter):
    error_messages = DefaultAccountAdapter.error_messages | {
        "email_password_mismatch": "Unable to sign in. Check your details or try again in five minutes.",
        "username_password_mismatch": "Unable to sign in. Check your details or try again in five minutes.",
    }

    def authenticate(self, request, **credentials):
        identity = (
            str(credentials.get("email") or credentials.get("username") or "")
            .strip()
            .casefold()
        )
        return authenticate_identity(
            "password",
            identity,
            lambda: super(AccountAdapter, self).authenticate(request, **credentials),
        )

    def send_mail(self, template_prefix, email, context):
        try:
            return super().send_mail(template_prefix, email, context)
        except (SMTPException, OSError):
            raise EmailDeliveryError() from None
