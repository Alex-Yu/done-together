import os

from django.core.exceptions import ImproperlyConfigured

from .base import *  # noqa: F403

DEBUG = False
ALLOWED_HOSTS = ["127.0.0.1", "localhost", "testserver"]
EMAIL_BACKEND = "django.core.mail.backends.locmem.EmailBackend"
SESSION_COOKIE_SECURE = False
CSRF_COOKIE_SECURE = False

# Fail before Django's test runner can create, reuse, or destroy a database.
_test_name = os.environ.get("TEST_DB_NAME", "")
_app_name = DATABASES["default"]["NAME"]  # noqa: F405
if not _test_name.startswith("test_") or _test_name == _app_name:
    raise ImproperlyConfigured("TEST_DB_NAME must be a separate test_ database")
DATABASES["default"]["TEST"] = {"NAME": _test_name}  # noqa: F405
