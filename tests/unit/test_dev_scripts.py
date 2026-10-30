"""Developer-script safety checks in isolated checkouts, without real services."""

import os
import shlex
import shutil
import socket
import subprocess
import sys
from pathlib import Path

import pytest
from dotenv import dotenv_values

ROOT = Path(__file__).resolve().parents[2]


@pytest.fixture
def checkout(tmp_path):
    shutil.copytree(ROOT / "scripts", tmp_path / "scripts")
    shutil.copy(ROOT / ".env.example", tmp_path / ".env.example")
    binaries = tmp_path / ".local/bin"
    binaries.mkdir(parents=True)
    # Execute real configuration-generation Python; isolate package/service calls.
    uv = binaries / "uv"
    uv.write_text(
        "#!/usr/bin/env bash\nset -eu\n"
        'if [[ "$1" == sync ]]; then exit 0; fi\n'
        '[[ "$1" == run && "$2" == --locked ]]\nshift 2\n'
        'if [[ "$1" == python && "${2:-}" == - ]]; then\n'
        f'    shift; exec {shlex.quote(sys.executable)} "$@"\n'
        "fi\n"
        'if [[ "$1" == pytest && "${2:-}" == --script-signal-probe ]]; then\n'
        f"    exec {shlex.quote(sys.executable)} -c 'import signal; assert callable(signal.getsignal(signal.SIGINT))'\n"
        "fi\n"
        'printf "%s\\n" "$*" >> .local/commands\n'
    )
    uv.chmod(0o755)
    for name in ("initdb", "postgres", "pg_ctl"):
        executable = binaries / name
        executable.write_text(
            '#!/usr/bin/env bash\nif [[ "${1:-}" == --version ]]; then\n'
            'echo "pg_ctl (PostgreSQL) 17.11"\nelse\n'
            'echo "Unexpected database mutation" >&2; exit 99\nfi\n'
        )
        executable.chmod(0o755)
    return tmp_path


def invoke(checkout, script, *arguments):
    directory = checkout
    # Never pass the real checkout's loaded configuration to a fixture process.
    environment = {
        key: value
        for key, value in os.environ.items()
        if key not in dotenv_values(ROOT / ".env.example")
    }
    return subprocess.run(
        [str(directory / "scripts" / script), *arguments],
        cwd=directory.parent,  # Scripts must resolve their own checkout root.
        env=environment,
        text=True,
        capture_output=True,
        timeout=15,
    )


def test_external_setup_creates_private_secrets_and_preserves_them_on_rerun(checkout):
    directory = checkout
    first = invoke(checkout, "setup.sh", "--external-db")
    assert first.returncode == 0, first.stderr
    path = directory / ".env"
    contents = path.read_bytes()
    values = dotenv_values(path)
    secrets = [
        values[key] for key in ("DJANGO_SECRET_KEY", "PIN_HASH_PEPPER", "DB_PASSWORD")
    ]
    assert len(set(secrets)) == 3
    assert all(len(secret) >= 64 for secret in secrets)
    assert path.stat().st_mode & 0o777 == 0o600
    assert all(secret not in first.stdout + first.stderr for secret in secrets)
    second = invoke(checkout, "setup.sh", "--external-db")
    assert second.returncode == 0, second.stderr
    assert path.read_bytes() == contents
    assert not (directory / ".local/pgdata").exists()
    assert (directory / ".local/commands").read_text().splitlines() == [
        "python manage.py migrate",
        "python manage.py check",
    ] * 2


def test_setup_rejects_existing_placeholders_without_replacing_configuration(checkout):
    directory = checkout
    source = (directory / ".env.example").read_bytes()
    (directory / ".env").write_bytes(source)
    result = invoke(checkout, "setup.sh", "--external-db")
    assert result.returncode != 0
    assert "DJANGO_SECRET_KEY" in result.stderr
    assert (directory / ".env").read_bytes() == source
    assert not (directory / ".local/commands").exists()


def test_managed_setup_refuses_external_database_before_cluster_mutations(checkout):
    directory = checkout
    assert invoke(checkout, "setup.sh", "--external-db").returncode == 0
    path = directory / ".env"
    path.write_text(path.read_text().replace("DB_PORT=55432", "DB_PORT=5432"))
    result = invoke(checkout, "setup.sh")
    assert result.returncode != 0
    assert "use --external-db" in result.stderr
    assert not (directory / ".local/pgdata").exists()
    assert not (directory / ".local/pgadmin-password").exists()


def test_test_lock_rejects_overlap_and_is_removed_after_a_completed_run(checkout):
    directory = checkout
    assert invoke(checkout, "setup.sh", "--external-db").returncode == 0
    lock = directory / ".local/test-suite.lock"
    lock.mkdir()
    result = invoke(checkout, "test.sh", "unit")
    assert result.returncode != 0
    assert "Another scripted test suite" in result.stderr
    lock.rmdir()
    result = invoke(checkout, "test.sh", "unit")
    assert result.returncode == 0, result.stderr
    assert not lock.exists()


def test_test_runner_preserves_interrupts_for_scheduler_subprocesses(checkout):
    assert invoke(checkout, "setup.sh", "--external-db").returncode == 0
    result = invoke(checkout, "test.sh", "pytest", "--script-signal-probe")
    assert result.returncode == 0, result.stderr


def test_port_check_refuses_listeners_but_allows_immediate_restart(checkout):
    with socket.socket() as listener:
        listener.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        listener.bind(("127.0.0.1", 0))
        listener.listen()
        port = listener.getsockname()[1]
        command = [
            "/bin/bash",
            "-c",
            'source "$1"; port_available "$2"',
            "probe",
            str(checkout / "scripts/common.sh"),
            str(port),
        ]
        occupied = subprocess.run(command, text=True, capture_output=True, timeout=15)
        assert occupied.returncode != 0
        assert "is occupied" in occupied.stderr
        # Server closes first, leaving a normal TCP TIME_WAIT after shutdown.
        with socket.create_connection(("127.0.0.1", port)) as client:
            connection, _ = listener.accept()
            connection.close()
            assert client.recv(1) == b""
    stopped = subprocess.run(command, text=True, capture_output=True, timeout=15)
    assert stopped.returncode == 0, stopped.stderr
