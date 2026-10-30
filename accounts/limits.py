"""Database-serialized identity failures and independent source request windows."""

import hashlib
import hmac
from datetime import timedelta

from django.conf import settings
from django.db import transaction
from django.utils import timezone

from .models import AuthenticationLimit, RequestLimit


def private_key(namespace, identity):
    return hmac.new(
        settings.PIN_HASH_PEPPER.encode(),
        f"{namespace}:{identity}".encode(),
        hashlib.sha256,
    ).hexdigest()


def authenticate_identity(namespace, identity, verify):
    key = private_key(namespace, identity)
    with transaction.atomic():
        AuthenticationLimit.objects.get_or_create(key=key)
        limit = AuthenticationLimit.objects.select_for_update().get(key=key)
        now = timezone.now()
        if limit.blocked_until and now < limit.blocked_until:
            return None
        if limit.blocked_until:
            limit.failures = 0
            limit.blocked_until = None
        result = verify()
        if result:
            limit.failures = 0
            limit.blocked_until = None
        else:
            limit.failures += 1
            if limit.failures >= 5:
                limit.blocked_until = now + timedelta(minutes=5)
        limit.save(update_fields=["failures", "blocked_until"])
        return result


def allow_source(source):
    key = private_key("account-request-source", source)
    with transaction.atomic():
        RequestLimit.objects.get_or_create(key=key)
        limit = RequestLimit.objects.select_for_update().get(key=key)
        now = timezone.now()
        if now >= limit.window_started + timedelta(seconds=60):
            limit.window_started = now
            limit.count = 0
        if limit.count >= 60:
            return False
        limit.count += 1
        limit.save(update_fields=["count", "window_started"])
        return True
