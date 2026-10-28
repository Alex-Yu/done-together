import logging
import re

from django.views.debug import SafeExceptionReporterFilter


class AccountLogFilter(logging.Filter):
    patterns = (
        (
            re.compile(r"/accounts/verification/confirm/[^/\s?]+/"),
            "/accounts/verification/confirm/[redacted]/",
        ),
        (re.compile(r"(/accounts/[^?\s]*)\?[^\s]*"), r"\1?[redacted]"),
        (
            re.compile(r"/accounts/confirm-email/[^/\s?]+/"),
            "/accounts/confirm-email/[redacted]/",
        ),
        (
            re.compile(r"/accounts/password/reset/key/[^/\s?]+/"),
            "/accounts/password/reset/key/[redacted]/",
        ),
        (
            re.compile(r"([?&](?:key|token|password|pin)=)[^&\s]*", re.I),
            r"\1[redacted]",
        ),
    )

    def filter(self, record):
        text = record.getMessage()
        for pattern, replacement in self.patterns:
            text = pattern.sub(replacement, text)
        record.msg = text
        record.args = ()
        return True


class PrivateExceptionFilter(SafeExceptionReporterFilter):
    hidden_settings = re.compile(
        "API|TOKEN|KEY|SECRET|PASS|SIGNATURE|HTTP_COOKIE|PEPPER", re.I
    )
