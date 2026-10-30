import os
import subprocess
import sys

import pytest
from django.conf import settings


def test_test_environment_uses_separate_postgresql_and_memory_email():
    database = settings.DATABASES["default"]
    assert database["ENGINE"] == "django.db.backends.postgresql"
    assert database["TEST"]["NAME"].startswith("test_")
    assert database["TEST"]["NAME"] != os.environ["DB_NAME"]
    assert settings.EMAIL_BACKEND == "django.core.mail.backends.locmem.EmailBackend"
    assert settings.AUTH_USER_MODEL == "accounts.User"


@pytest.mark.parametrize(
    "app_name,test_name",
    [
        ("done_together", "done_together"),
        ("done_together", ""),
        ("done_together", "unprotected"),
        ("test_equal", "test_equal"),
    ],
)
def test_unsafe_test_database_name_is_rejected_before_setup(app_name, test_name):
    env = os.environ | {"DB_NAME": app_name, "TEST_DB_NAME": test_name}
    result = subprocess.run(
        [sys.executable, "-c", "import config.settings.test"],
        env=env,
        capture_output=True,
        text=True,
    )
    assert result.returncode != 0
    assert "TEST_DB_NAME must be a separate test_ database" in result.stderr


@pytest.mark.parametrize("name", ["DJANGO_SECRET_KEY", "PIN_HASH_PEPPER"])
def test_missing_secret_is_rejected_even_in_debug_mode(name):
    env = os.environ | {name: "", "DJANGO_DEBUG": "True"}
    result = subprocess.run(
        [sys.executable, "-c", "import config.settings.local"],
        env=env,
        capture_output=True,
        text=True,
    )
    assert result.returncode != 0
    assert f"Required configuration missing: {name}" in result.stderr
