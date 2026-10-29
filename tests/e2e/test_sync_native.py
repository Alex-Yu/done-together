"""Same-Mac independent profiles: actual accepted POST to second-board render."""

import json
import os
import sys
import time
from pathlib import Path
from tempfile import TemporaryDirectory

import pytest
from django.db import connections
from playwright.sync_api import sync_playwright

from tests.integration.test_pins import PASS_A
from tests.integration.test_review import ready

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / "tools"))
import verify_household_browsers as native  # noqa: E402

ACCEPTED = {}


class Firefox(native.Firefox):
    # Native helper returns one expression; eval keeps multi-statement test
    # setup atomic and returns its final expression in both supported engines.
    def execute(self, script):
        return super().execute("eval(" + json.dumps(script) + ")")


def wait(ui, expression, expected=True, seconds=5):
    deadline = time.monotonic() + seconds
    while time.monotonic() < deadline:
        if ui.execute(expression) == expected:
            return time.monotonic()
        time.sleep(0.04)
    raise AssertionError("Browser condition did not settle: " + expression)


def post(writer, path, data):
    # Real authenticated browser request with the CSRF token/hidden version from
    # the real scoped form. No direct service call mutates the measured board.
    return writer.page.evaluate(
        """async ({path,data}) => {
      const source = path.endsWith('/unlock/') ? path.replace('/unlock/','/board/') : path;
      const page = await fetch(source, {cache:'no-store'});
      const doc = new DOMParser().parseFromString(await page.text(),'text/html');
      const form = doc.querySelector('form[method="post"]');
      const body = new URLSearchParams();
      for (const input of form.querySelectorAll('input[type="hidden"]')) body.set(input.name,input.value);
      for (const [key,value] of Object.entries(data)) body.set(key,value);
      const result = await fetch(path,{method:'POST',body});
      return {status:result.status,redirected:result.redirected};
    }""",
        {"path": path, "data": data},
    )


@pytest.fixture
def accepted_clock(monkeypatch):
    from django.core.handlers.base import BaseHandler

    original = BaseHandler.get_response

    def timed(handler, request):
        response = original(handler, request)
        if request.method == "POST" and response.status_code == 302:
            ACCEPTED[request.path] = time.monotonic()
        return response

    monkeypatch.setattr(BaseHandler, "get_response", timed)


@pytest.mark.skipif(
    os.environ.get("RUN_NATIVE_SYNC") != "1", reason="native browsers/driver required"
)
@pytest.mark.django_db(transaction=True)
def test_native_sync_offline_focus_conflicts(accepted_clock, live_server, monkeypatch):
    monkeypatch.setenv("DJANGO_ALLOW_ASYNC_UNSAFE", "true")
    a, _, h, c, child, work = ready()
    monkeypatch.setattr(native, "BASE_URL", live_server.url)
    out = ROOT / ".local/verification/009"
    out.mkdir(parents=True, exist_ok=True)
    records = []
    with sync_playwright() as pw:
        for engine in ("chrome", "firefox"):
            for zoom in (1, 2):
                with (
                    TemporaryDirectory(
                        dir=ROOT / ".local", prefix="sync-writer-"
                    ) as wp,
                    TemporaryDirectory(
                        dir=ROOT / ".local", prefix="sync-observer-"
                    ) as op,
                ):
                    writer = native.Chrome(pw, wp, 1)
                    observer = (
                        native.Chrome(pw, op, zoom)
                        if engine == "chrome"
                        else Firefox(zoom)
                    )
                    try:
                        native.signin(writer, a.email, PASS_A)
                        native.signin(observer, a.email, PASS_A)
                        observer.apply_zoom()
                        wait(
                            observer,
                            "document.documentElement.dataset.connected",
                            "true",
                        )
                        assert observer.execute("innerWidth") == 1280 // zoom
                        assert observer.execute("innerHeight") == 720 // zoom
                        # Unlock independent writer only. Observer retains an unsaved PIN,
                        # focus and selection while its board regions change.
                        result = post(
                            writer,
                            f"/households/{h.pk}/unlock/",
                            {"parent": a.pk, "pin": "2468"},
                        )
                        assert result["status"] == 200 and result["redirected"]
                        native.tab_to(observer, "pin")
                        observer.fill("pin", "12")
                        observer.execute(
                            "document.querySelector('[name=pin]').focus();document.querySelector('[name=pin]').setSelectionRange(1,1)"
                        )
                        observer.execute(
                            "window.savedBoard=document.querySelector('.child-columns')"
                        )
                        time.sleep(2.2)
                        assert observer.execute(
                            "window.savedBoard===document.querySelector('.child-columns')"
                        )
                        prefix = f"{engine}-{zoom}"

                        def measured(kind, path, data, expression):
                            result = post(writer, path, data)
                            assert result == {"status": 200, "redirected": True}, (
                                kind,
                                result,
                            )
                            seen = wait(observer, expression)
                            elapsed = seen - ACCEPTED[path]
                            assert 0 <= elapsed <= 5, (kind, elapsed)
                            records.append(
                                {
                                    "host": "single Mac",
                                    "writer": "independent native Chrome profile",
                                    "observer": engine,
                                    "version": observer.version,
                                    "zoom": zoom * 100,
                                    "event": kind,
                                    "accepted_monotonic": ACCEPTED[path],
                                    "render_monotonic": seen,
                                    "latency_seconds": round(elapsed, 4),
                                }
                            )
                            assert observer.execute(
                                "document.activeElement.name==='pin' && document.activeElement.value==='12' && document.activeElement.selectionStart===1 && document.activeElement.selectionEnd===1"
                            )

                        measured(
                            "child-create",
                            f"/households/{h.pk}/children/new/",
                            {"name": prefix + " child", "pin": "0007"},
                            f"document.querySelector('.child-columns').textContent.includes({json.dumps(prefix + ' child')})",
                        )
                        measured(
                            "child-profile",
                            f"/households/{h.pk}/children/{child.pk}/edit/",
                            {"name": prefix + " renamed"},
                            f"document.querySelector('.child-columns').textContent.includes({json.dumps(prefix + ' renamed')})",
                        )
                        measured(
                            "chore-create",
                            f"/households/{h.pk}/chores/new/",
                            {
                                "title": prefix + " work",
                                "child": child.pk,
                                "due_date": "2026-10-29",
                            },
                            f"document.querySelector('.child-columns').textContent.includes({json.dumps(prefix + ' work')})",
                        )
                        from chores.models import Occurrence

                        w = Occurrence.objects.get(title=prefix + " work")
                        measured(
                            "chore-edit",
                            f"/households/{h.pk}/chores/{w.pk}/edit/",
                            {
                                "title": prefix + " edited",
                                "child": child.pk,
                                "due_date": "2026-10-29",
                            },
                            f"document.querySelector('[data-work-id=\"{w.pk}\"]').textContent.includes('edited')",
                        )
                        measured(
                            "submission",
                            f"/households/{h.pk}/chores/{w.pk}/submit/",
                            {"pin": "0007", "browser_timezone": "Europe/Warsaw"},
                            f"document.querySelector('[data-work-id=\"{w.pk}\"]').dataset.state==='awaiting_approval'",
                        )
                        measured(
                            "return",
                            f"/households/{h.pk}/chores/{w.pk}/review/",
                            {"action": "return", "note": prefix + " explanation"},
                            f"document.querySelector('[data-work-id=\"{w.pk}\"]').textContent.includes('explanation')",
                        )
                        measured(
                            "resubmission",
                            f"/households/{h.pk}/chores/{w.pk}/submit/",
                            {"pin": "0007", "browser_timezone": "Europe/Warsaw"},
                            f"document.querySelector('[data-work-id=\"{w.pk}\"]').dataset.state==='awaiting_approval'",
                        )
                        old = observer.execute(
                            "document.querySelector('[data-child-id=\"%s\"] [data-all-time-stars]').textContent"
                            % child.pk
                        )
                        measured(
                            "approval-and-totals",
                            f"/households/{h.pk}/chores/{w.pk}/review/",
                            {"action": "approve"},
                            f"document.querySelector('[data-work-id=\"{w.pk}\"]').dataset.state==='completed' && document.querySelector('[data-child-id=\"{child.pk}\"] [data-all-time-stars]').textContent!=={json.dumps(old)}",
                        )
                        # Delete a separately accepted chore.
                        assert post(
                            writer,
                            f"/households/{h.pk}/chores/new/",
                            {
                                "title": prefix + " delete",
                                "child": child.pk,
                                "due_date": "2026-10-29",
                            },
                        )["redirected"]
                        d = Occurrence.objects.get(title=prefix + " delete")
                        wait(
                            observer,
                            f"!!document.querySelector('[data-work-id=\"{d.pk}\"]')",
                        )
                        measured(
                            "chore-delete",
                            f"/households/{h.pk}/chores/{d.pk}/delete/",
                            {},
                            f"!document.querySelector('[data-work-id=\"{d.pk}\"]')",
                        )
                        assert not observer.execute(
                            "document.documentElement.scrollWidth>innerWidth"
                        )
                        assert (
                            observer.execute(
                                "getComputedStyle(document.activeElement).outlineStyle"
                            )
                            != "none"
                        )
                        # Poll failure/online hint cannot enable until authorized snapshot.
                        observer.execute(
                            "window.realFetch=window.fetch;window.fetch=()=>Promise.reject(new TypeError('synthetic unreachable'));window.dispatchEvent(new Event('offline'))"
                        )
                        wait(
                            observer,
                            "document.documentElement.dataset.connected",
                            "false",
                        )
                        text = observer.execute(
                            "document.querySelector('.child-columns').textContent"
                        )
                        assert observer.execute(
                            "[...document.querySelectorAll('form[method=post] button')].every(b=>b.disabled)"
                        )
                        observer.execute("window.dispatchEvent(new Event('online'))")
                        time.sleep(0.2)
                        assert (
                            observer.execute(
                                "document.documentElement.dataset.connected"
                            )
                            == "false"
                        )
                        assert (
                            observer.execute(
                                "document.querySelector('.child-columns').textContent"
                            )
                            == text
                        )
                        observer.screenshot(out / f"{engine}-{zoom * 100}-offline.png")
                        observer.execute(
                            "window.fetch=window.realFetch;window.dispatchEvent(new Event('online'))"
                        )
                        wait(
                            observer,
                            "document.documentElement.dataset.connected",
                            "true",
                        )
                        assert (
                            observer.execute(
                                "document.querySelector('[name=pin]').value"
                            )
                            == "12"
                        )
                        # Confirmed session loss clears private board, unlike transient failure.
                        from django.contrib.sessions.models import Session

                        if engine == "chrome":
                            cookie = next(
                                x["value"]
                                for x in observer.context.cookies()
                                if x["name"] == "sessionid"
                            )
                        else:
                            cookies = native.webdriver(
                                "GET", observer.session + "/cookie"
                            )
                            cookie = next(
                                x["value"] for x in cookies if x["name"] == "sessionid"
                            )
                        Session.objects.filter(session_key=cookie).delete()
                        wait(
                            observer,
                            "document.body.textContent.includes('Board access ended')",
                        )
                        assert not observer.execute(
                            "!!document.querySelector('.child-columns')"
                        )
                        print(
                            engine,
                            observer.version,
                            zoom * 100,
                            "independent same-host mutation latency/focus/offline/auth-clear PASS",
                        )
                    finally:
                        observer.close()
                        writer.close()
                        connections.close_all()
    (out / "latencies.json").write_text(json.dumps(records, indent=2))


@pytest.mark.skipif(
    os.environ.get("RUN_NATIVE_SYNC") != "1", reason="native browsers/driver required"
)
@pytest.mark.django_db(transaction=True)
def test_native_open_form_stale_lost_response_and_failure(live_server, monkeypatch):
    monkeypatch.setenv("DJANGO_ALLOW_ASYNC_UNSAFE", "true")
    a, _, h, c, child, work = ready()
    monkeypatch.setattr(native, "BASE_URL", live_server.url)
    from chores.models import Approval
    from households.models import BoardAuthority

    with sync_playwright() as pw:
        for engine in ("chrome", "firefox"):
            for zoom in (1, 2):
                selected = os.environ.get("SYNC_NATIVE_CASE")
                if selected and selected != f"{engine}-{zoom}":
                    continue
                with TemporaryDirectory(
                    dir=ROOT / ".local", prefix="sync-form-"
                ) as profile:
                    ui = (
                        native.Chrome(pw, profile, zoom)
                        if engine == "chrome"
                        else Firefox(zoom)
                    )

                    def visit(path):
                        ui.goto(path)
                        ui.apply_zoom()
                        assert ui.execute("innerWidth") == 1280 // zoom
                        assert ui.execute("innerHeight") == 720 // zoom

                    try:
                        native.signin(ui, a.email, PASS_A)
                        ui.apply_zoom()
                        wait(ui, "document.documentElement.dataset.connected", "true")
                        ui.fill("pin", "2468")
                        ui.click("Unlock parent controls")
                        native.wait_for(
                            ui,
                            "document.getElementById('parent-lock-status').textContent.trim()",
                            "Parent controls unlocked.",
                        )
                        visit(f"/households/{h.pk}/chores/{work.pk}/edit/")
                        wait(ui, "document.documentElement.dataset.connected", "true")
                        ui.fill("title", "Unsaved local title")
                        ui.execute(
                            "document.querySelector('[name=title]').focus();document.querySelector('[name=title]').setSelectionRange(3,7)"
                        )
                        work.refresh_from_db()
                        result = c.post(
                            f"/households/{h.pk}/chores/{work.pk}/edit/",
                            {
                                "version": work.version,
                                "title": "Accepted remote title",
                                "child": child.pk,
                                "due_date": "2026-10-29",
                            },
                        )
                        assert result.status_code == 302
                        wait(
                            ui,
                            "document.querySelector('[data-sync-status]').textContent.includes('input is preserved')",
                        )
                        assert ui.execute(
                            "document.activeElement.name==='title' && document.activeElement.value==='Unsaved local title' && document.activeElement.selectionStart===3 && document.activeElement.selectionEnd===7"
                        )
                        # Native keyboard submission reaches the server with the original
                        # version: explicit conflict preserves draft and displays current board.
                        ui.execute(
                            "document.querySelector('form[method=post]').requestSubmit()"
                        )
                        wait(
                            ui,
                            "document.body.textContent.includes('This chore changed')",
                        )
                        assert (
                            ui.execute("document.querySelector('[name=title]').value")
                            == "Unsaved local title"
                        )
                        assert ui.execute(
                            "document.querySelector('.child-columns').textContent.includes('Accepted remote title')"
                        )
                        ui.execute(
                            "document.querySelector('form[method=post]').scrollIntoView({block:'start'});true"
                        )
                        ui.screenshot(
                            ROOT
                            / f".local/verification/009/{engine}-{zoom * 100}-conflict.png"
                        )
                        # Transient server 500 keeps the last board and disables mutations.
                        visit(f"/households/{h.pk}/board/")
                        wait(ui, "document.documentElement.dataset.connected", "true")
                        ui.execute(
                            "window.realFetch=window.fetch; window.fetch=async (...args)=>String(args[0]).includes('/snapshot/')?new Response('Temporary failure',{status:500}):window.realFetch(...args);true"
                        )
                        wait(ui, "document.documentElement.dataset.connected", "false")
                        assert ui.execute("!!document.querySelector('.child-columns')")
                        ui.execute(
                            "window.fetch=window.realFetch;window.dispatchEvent(new Event('online'))"
                        )
                        wait(ui, "document.documentElement.dataset.connected", "true")
                        # Actual browser offline (Chrome) preserves board. Firefox's prior
                        # unreachable fetch/500 checks exercise the same transport-failure gate.
                        if engine == "chrome":
                            ui.context.set_offline(True)
                            wait(
                                ui,
                                "document.documentElement.dataset.connected",
                                "false",
                            )
                            assert ui.execute(
                                "!!document.querySelector('.child-columns')"
                            )
                            ui.context.set_offline(False)
                            wait(
                                ui, "document.documentElement.dataset.connected", "true"
                            )
                        work.refresh_from_db()
                        assert (
                            c.post(
                                f"/households/{h.pk}/chores/{work.pk}/submit/",
                                {
                                    "version": work.version,
                                    "pin": "0007",
                                    "browser_timezone": "UTC",
                                },
                            ).status_code
                            == 302
                        )
                        visit(f"/households/{h.pk}/chores/{work.pk}/review/")
                        wait(ui, "document.documentElement.dataset.connected", "true")
                        # Await the real server commit, then drop its response. The UI must
                        # not navigate/show success/retry; authorized resync permits inspection.
                        ui.execute(
                            "window.realFetch=window.fetch;window.fetch=async (...args)=>{const response=await window.realFetch(...args);if(args[1]?.method==='POST')throw new TypeError('lost response after commit');return response};true"
                        )
                        ui.execute(
                            "document.querySelector('[name=action]').value='approve';document.querySelector('form[method=post]').requestSubmit()"
                        )
                        wait(
                            ui,
                            "document.querySelector('[data-sync-status]').textContent.includes('may have committed')",
                        )
                        ui.execute(
                            "document.querySelector('[data-sync-status]').scrollIntoView({block:'end'});true"
                        )
                        ui.screenshot(
                            ROOT
                            / f".local/verification/009/{engine}-{zoom * 100}-uncertain.png"
                        )
                        assert Approval.objects.filter(occurrence=work).count() == 1
                        assert ui.execute(
                            "document.querySelector('form[method=post] button').disabled"
                        )
                        assert not ui.execute(
                            "document.body.textContent.includes('Chore approved.')"
                        )
                        ui.execute(
                            "document.querySelector('form[method=post]').requestSubmit()"
                        )
                        time.sleep(0.1)
                        assert Approval.objects.filter(occurrence=work).count() == 1
                        visit(f"/households/{h.pk}/board/")
                        wait(ui, "document.documentElement.dataset.connected", "true")
                        assert (
                            ui.execute(
                                f"document.querySelector('[data-work-id=\"{work.pk}\"]').dataset.state"
                            )
                            == "completed"
                        )
                        assert not ui.execute(
                            "document.documentElement.scrollWidth>innerWidth"
                        )
                        # Confirm passive snapshot traffic cannot extend expired authority;
                        # retain input instead of navigating away when parent controls lock.
                        from datetime import timedelta

                        from django.utils import timezone

                        BoardAuthority.objects.update(
                            last_activity=timezone.now() - timedelta(seconds=60)
                        )
                        wait(
                            ui,
                            "document.querySelector('#parent-lock-status').textContent.includes('locked. Reopen')",
                        )
                        assert ui.execute("!!document.querySelector('.child-columns')")
                        assert (
                            c.post(
                                f"/households/{h.pk}/chores/new/",
                                {
                                    "title": "Expired direct write",
                                    "child": child.pk,
                                    "due_date": "2026-10-29",
                                },
                            ).status_code
                            == 403
                        )
                        ui.screenshot(
                            ROOT
                            / f".local/verification/009/{engine}-{zoom * 100}-reconciled.png"
                        )
                        print(
                            engine,
                            ui.version,
                            zoom * 100,
                            "open draft/caret/stale conflict/500/lost commit response/no retry/expiry PASS",
                        )
                        # New eligible work for the next independent browser case.
                        from tests.integration.test_pins import unlock

                        unlock(c, h, a)
                        from chores.services import save_one_off

                        work = save_one_off(
                            h,
                            {
                                "title": "Next conflict fixture",
                                "child": child,
                                "due_date": timezone.now().date(),
                            },
                        )
                    finally:
                        ui.close()
                        connections.close_all()


@pytest.mark.skipif(
    os.environ.get("RUN_NATIVE_SYNC") != "1", reason="native browsers/driver required"
)
@pytest.mark.django_db(transaction=True)
def test_idle_household_week_and_local_midnight(live_server, monkeypatch):
    from datetime import datetime, timedelta
    from datetime import timezone as dtz

    from django.utils import timezone

    from households.models import Household
    from tests.integration.test_review import post_review, post_submit

    monkeypatch.setenv("DJANGO_ALLOW_ASYNC_UNSAFE", "true")
    current = [datetime(2026, 11, 1, 23, 59, 59, tzinfo=dtz.utc)]
    monkeypatch.setattr(timezone, "now", lambda: current[0])
    a, _, h, c, child, work = ready()
    Household.objects.filter(pk=h.pk).update(timezone="UTC")
    assert post_submit(c, h, work).status_code == 302
    work.refresh_from_db()
    assert post_review(c, h, work).status_code == 302
    from chores.services import save_one_off

    active = save_one_off(
        h,
        {
            "title": "Local midnight unfinished",
            "child": child,
            "due_date": current[0].date(),
        },
    )
    h.refresh_from_db()
    revision = h.revision
    monkeypatch.setattr(native, "BASE_URL", live_server.url)
    with (
        sync_playwright() as pw,
        TemporaryDirectory(dir=ROOT / ".local", prefix="idle-sync-") as profile,
    ):
        chrome = native.Chrome(pw, profile, 1)
        firefox = Firefox(1)
        try:
            for ui in (chrome, firefox):
                native.signin(ui, a.email, PASS_A)
                wait(ui, "document.documentElement.dataset.connected", "true")
                assert (
                    ui.execute(
                        "document.querySelector('[data-weekly-stars]').textContent"
                    )
                    == "This week: 1 star"
                )
                ui.execute(
                    "window.NativeDate=Date;window.localInstant='2026-11-01T12:00:00';window.Date=class extends window.NativeDate{constructor(...args){super(...(args.length?args:[window.localInstant]))}};document.dispatchEvent(new Event('board:updated'))"
                )
                assert not ui.execute(
                    f"document.querySelector('[data-work-id=\"{active.pk}\"]').classList.contains('is-overdue')"
                )
            current[0] += timedelta(seconds=1)
            for ui in (chrome, firefox):
                wait(
                    ui,
                    "document.querySelector('[data-weekly-stars]').textContent",
                    "This week: 0 stars",
                )
                assert (
                    ui.execute(
                        "document.querySelector('[data-all-time-stars]').textContent"
                    )
                    == "All time: 1 star"
                )
                assert not ui.execute(
                    f"!!document.querySelector('[data-work-id=\"{work.pk}\"]')"
                )
                ui.execute("window.localInstant='2026-11-02T00:00:00'")
            # Let the actual idle local-date timer fire, without mutation/events.
            for ui in (chrome, firefox):
                wait(
                    ui,
                    f"document.querySelector('[data-work-id=\"{active.pk}\"]').classList.contains('is-overdue')",
                    seconds=32,
                )
            h.refresh_from_db()
            assert h.revision == revision
            print(
                "Chrome/Firefox idle unchanged-revision household Monday and actual local-date timer PASS"
            )
        finally:
            chrome.close()
            firefox.close()
            connections.close_all()
