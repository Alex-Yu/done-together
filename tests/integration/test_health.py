import pytest
from django.db import OperationalError
from django.test import Client


@pytest.mark.django_db
def test_health_queries_database_and_returns_minimal_readiness(
    client, django_assert_num_queries
):
    with django_assert_num_queries(1):
        response = client.get("/health/")
    assert response.status_code == 200
    assert response.json() == {"status": "ok"}
    assert "no-store" in response.headers["Cache-Control"]


def test_health_database_failure_is_generic(client, monkeypatch):
    def unavailable(*args, **kwargs):
        raise OperationalError("private connection detail must not escape")

    monkeypatch.setattr("board.views.connection.cursor", unavailable)
    response = client.get("/health/")
    assert response.status_code == 503
    assert response.json() == {"status": "unavailable"}
    assert b"private" not in response.content


def test_smoke_requires_post_and_csrf():
    client = Client(enforce_csrf_checks=True)
    assert client.get("/smoke/").status_code == 405
    assert client.post("/smoke/").status_code == 403
    client.get("/")
    response = client.post(
        "/smoke/", HTTP_X_CSRFTOKEN=client.cookies["csrftoken"].value
    )
    assert response.status_code == 200
    assert b"Connection checked successfully" in response.content


@pytest.mark.django_db
def test_real_database_connection_failure_returns_no_details(
    client, monkeypatch, settings
):
    import socket

    from django.db.utils import ConnectionHandler

    with socket.socket() as probe:
        probe.bind(("127.0.0.1", 0))
        unused_port = probe.getsockname()[1]
    config = settings.DATABASES["default"] | {"PORT": str(unused_port)}
    isolated = ConnectionHandler({"default": config})["default"]
    monkeypatch.setattr("board.views.connection", isolated)
    try:
        response = client.get("/health/")
        assert response.status_code == 503
        assert response.json() == {"status": "unavailable"}
        assert b"password" not in response.content.lower()
        assert str(unused_port).encode() not in response.content
    finally:
        isolated.close()
