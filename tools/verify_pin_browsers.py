"""Native PIN/child management and real60sec idle; synthetic ignored fixtures only."""

import argparse
import json
import time
from tempfile import TemporaryDirectory

from playwright.sync_api import sync_playwright
from verify_household_browsers import (
    FIXTURES,
    ROOT,
    Chrome,
    Firefox,
    fixtures,
    journey,
    signin,
    tab_to,
    wait_for,
    wait_heading,
)
from verify_release_keyboard import Keyboard


def href(ui, text):
    return ui.execute(
        "[...document.querySelectorAll('a')].find(el=>el.textContent.trim()==="
        + json.dumps(text)
        + ").getAttribute('href')"
    )


def choose_first_parent(ui):
    first = ui.execute("document.querySelector('[name=parent]').options[0].value")
    Keyboard(ui).select("parent", first)


def manage(ui):
    ui.goto(href(ui, "Manage household settings"))
    wait_heading(ui, "Household settings")


def assert_locked(ui):
    assert ui.execute(
        "[...document.querySelectorAll('[data-parent-controls] input,[data-parent-controls] select,[data-parent-controls] textarea,[data-parent-controls] button')].every(e=>e.disabled)"
    )
    assert ui.execute(
        "[...document.querySelectorAll('[data-parent-controls] a')].every(e=>e.getAttribute('aria-disabled')==='true'||e.dataset.parentLocked==='true')"
    )


def unlock_first(ui, pin):
    choose_first_parent(ui)
    ui.fill("pin", pin)
    ui.click("Unlock parent controls")
    wait_for(
        ui,
        "document.getElementById('parent-lock-status').textContent.trim()",
        "Parent controls unlocked.",
    )


def pin_journey(ui, record):
    journey(ui, record)
    ui.goto("/households/")
    wait_heading(ui, "Done Together")
    reset = href(ui, "Set or reset your own parent PIN")
    ui.goto(reset)
    wait_heading(ui, "Set or reset your parent PIN")
    choose_first_parent(ui)
    ui.fill("password", record["password"])
    ui.fill("pin", "0007")
    ui.click("Save parent PIN")
    wait_heading(ui, "Done Together")
    if (
        ui.execute("document.getElementById('parent-lock-status').textContent.trim()")
        == "Parent controls unlocked."
    ):
        ui.click("Lock parent controls")
    wait_for(
        ui,
        "document.getElementById('parent-lock-status').textContent.trim().startsWith('Parent controls locked.')",
        True,
    )
    assert_locked(ui)
    unlock_first(ui, "0007")
    manage(ui)
    ui.goto(href(ui, "Add child"))
    wait_heading(ui, "Add child")
    tab_to(ui, "name")
    ui.fill("name", "Aster native")
    ui.press("Tab")
    ui.fill("pin", "0123")
    ui.click("Save child")
    wait_heading(ui, "Household settings")
    ui.goto(href(ui, "Edit name"))
    wait_heading(ui, "Edit child name")
    ui.fill("name", "Birch native")
    ui.click("Save child")
    wait_heading(ui, "Household settings")
    ui.goto(href(ui, "Reset child PIN"))
    wait_heading(ui, "Reset child PIN")
    ui.fill("pin", "0456")
    ui.click("Save child")
    wait_heading(ui, "Household settings")
    ui.goto(href(ui, "Return to board"))
    wait_heading(ui, "Done Together")
    assert (
        ui.execute("document.querySelector('[data-child-name]').textContent.trim()")
        == "Birch native"
    )
    ui.goto(reset)
    wait_heading(ui, "Set or reset your parent PIN")
    choose_first_parent(ui)
    ui.fill("password", record["password"])
    ui.fill("pin", "0789")
    ui.click("Save parent PIN")
    wait_for(
        ui,
        "document.getElementById('parent-lock-status').textContent.trim().startsWith('Parent controls locked.')",
        True,
    )
    assert_locked(ui)
    choose_first_parent(ui)
    ui.fill("pin", "0007")
    ui.click("Unlock parent controls")
    wait_for(ui, "document.body.textContent.includes('Unable to unlock.')", True)
    assert ui.execute("document.querySelector('[name=pin]').value") == ""
    ui.fill("pin", "0789")
    ui.click("Unlock parent controls")
    wait_for(
        ui,
        "document.getElementById('parent-lock-status').textContent.trim()",
        "Parent controls unlocked.",
    )
    metrics = ui.execute(
        "({width:innerWidth,height:innerHeight,dpr:devicePixelRatio,overflow:document.documentElement.scrollWidth>innerWidth})"
    )
    assert metrics["width"] == 1280 // record["zoom"] and not metrics["overflow"]
    ui.screenshot(ROOT / f".local/pins-{record['engine']}-{record['zoom'] * 100}.png")
    record["selected_pin"] = "0789"
    record["child_name"] = "Birch native"
    print(
        record["engine"],
        ui.version,
        f"native{record['zoom'] * 100}%",
        metrics,
        "selected other-parent/child add/name/PIN update/replacement/keyboard/errors PASS",
        flush=True,
    )


def run(revisit):
    records = json.loads(FIXTURES.read_text()) if revisit else fixtures()
    records.sort(key=lambda record: (record["zoom"], record["engine"]))
    with sync_playwright() as playwright:
        held = []
        try:
            for record in records:
                profile = TemporaryDirectory(dir=ROOT / ".local", prefix="pin-chrome-")
                ui = (
                    Chrome(playwright, profile.name, record["zoom"])
                    if record["engine"] == "chrome"
                    else Firefox(record["zoom"])
                )
                if revisit:
                    try:
                        signin(ui, record["recipient"], record["password"])
                        ui.goto("/households/")
                        wait_heading(ui, "Done Together")
                        unlock_first(ui, record["selected_pin"])
                        manage(ui)
                        assert record["child_name"] in ui.execute(
                            "document.body.textContent"
                        )
                    finally:
                        ui.close()
                        profile.cleanup()
                    continue
                try:
                    pin_journey(ui, record)
                except Exception:
                    ui.close()
                    profile.cleanup()
                    raise
                if record["zoom"] == 1:
                    held.append((ui, profile, record))
                    if len(held) == 2:
                        print(
                            "Real idle61sec begins in both stable browsers; no parent input/heartbeat.",
                            flush=True,
                        )
                        time.sleep(61)
                        for idle, old_profile, old_record in held:
                            wait_for(
                                idle,
                                "document.getElementById('parent-lock-status').textContent.trim().startsWith('Parent controls locked.')",
                                True,
                            )
                            assert_locked(idle)
                            assert old_record["child_name"] in idle.execute(
                                "document.body.textContent"
                            )
                            idle.screenshot(
                                ROOT / f".local/pins-{old_record['engine']}-idle.png"
                            )
                            print(
                                old_record["engine"],
                                "real61sec lock with read-only child board visible: PASS",
                                flush=True,
                            )
                            idle.close()
                            old_profile.cleanup()
                        held = []
                else:
                    ui.close()
                    profile.cleanup()
            if not revisit:
                FIXTURES.write_text(json.dumps(records))
                FIXTURES.chmod(0o600)
        finally:
            for ui, profile, _ in held:
                ui.close()
                profile.cleanup()
    print(
        "PIN/child stored-state restart revisit: PASS"
        if revisit
        else "All native PIN/child and actual idle checks: PASS",
        flush=True,
    )


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--revisit", action="store_true")
    try:
        run(parser.parse_args().revisit)
    except Exception as error:
        raise SystemExit(
            f"PIN browser check failed ({type(error).__name__}); inspect isolated local artifacts without printing credentials or links."
        ) from None
