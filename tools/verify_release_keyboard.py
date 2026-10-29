"""Keyboard-only native interaction adapter; DOM reads only, no value/focus writes.

Browser launch, zoom and captured-email URL entry are setup operations. Product
navigation uses Tab/Enter, text uses native key input, selects use arrow keys.
"""

import json

import verify_household_browsers as native
from verify_skeleton_browsers import webdriver


class Keyboard:
    def __init__(self, ui):
        self.ui = ui

    def focus(self, predicate):
        # A rendered heading precedes the first authorized synchronization.
        # Until that snapshot settles, the product intentionally disables writes
        # and navigation. Do not try to activate an aria-disabled action.
        native.wait_for(
            self.ui,
            "!document.querySelector('[data-sync]') || document.documentElement.dataset.connected === 'true'",
            True,
        )
        visited = []
        target = predicate.replace("document.activeElement", "el")
        for _ in range(120):
            if self.ui.execute(predicate):
                assert self.ui.execute(
                    "getComputedStyle(document.activeElement).outlineStyle !== 'none'"
                ), "Keyboard target has no visible focus outline"
                return
            visited.append(
                self.ui.execute(
                    "({tag:document.activeElement.tagName,name:document.activeElement.name,disabled:document.activeElement.disabled,aria:document.activeElement.getAttribute('aria-disabled')})"
                )
            )
            # Use the ordinary reverse route for an earlier control. Firefox on
            # macOS resumes the last content focus when Tab returns from browser
            # chrome, so cycling past the document end cannot reach that control.
            reverse = self.ui.execute(
                "(() => {const target = [...document.querySelectorAll('input,select,textarea,button,a')].find(el => "
                + target
                + "); return !!target && !!(document.activeElement.compareDocumentPosition(target) & Node.DOCUMENT_POSITION_PRECEDING)})()"
            )
            self.key("Shift+Tab" if reverse else "Tab")
        raise AssertionError(f"Keyboard target not reachable with Tab: {visited[-12:]}")

    def field(self, name):
        self.focus("document.activeElement.name === " + json.dumps(name))
        assert self.ui.execute("document.activeElement.labels.length > 0")

    def key(self, key):
        if isinstance(self.ui, native.Chrome):
            self.ui.page.keyboard.press(key)
            return
        if key in {"Shift+Tab", "Meta+A"}:
            modifier, value = (
                ("\ue008", "\ue004") if key == "Shift+Tab" else ("\ue03d", "a")
            )
            actions = [
                {"type": "keyDown", "value": modifier},
                {"type": "keyDown", "value": value},
                {"type": "keyUp", "value": value},
                {"type": "keyUp", "value": modifier},
            ]
            webdriver(
                "POST",
                self.ui.session + "/actions",
                {"actions": [{"type": "key", "id": "keyboard", "actions": actions}]},
            )
            return
        value = {
            "Home": "\ue011",
            "ArrowDown": "\ue015",
            "ArrowUp": "\ue013",
            "ArrowRight": "\ue014",
            "ArrowLeft": "\ue012",
            "Tab": "\ue004",
            "Space": "\ue00d",
            "Backspace": "\ue003",
        }[key]
        webdriver(
            "POST",
            self.ui.session + "/actions",
            {
                "actions": [
                    {
                        "type": "key",
                        "id": "keyboard",
                        "actions": [
                            {"type": "keyDown", "value": value},
                            {"type": "keyUp", "value": value},
                        ],
                    }
                ]
            },
        )

    def text(self, name, value):
        self.field(name)
        self.key("Meta+A")
        self.key("Backspace")
        self.type_keys(value)

    def type_keys(self, text):
        if isinstance(self.ui, native.Chrome):
            self.ui.page.keyboard.type(text)
        else:
            actions = []
            for char in text:
                actions.extend(
                    [
                        {"type": "keyDown", "value": char},
                        {"type": "keyUp", "value": char},
                    ]
                )
            webdriver(
                "POST",
                self.ui.session + "/actions",
                {"actions": [{"type": "key", "id": "keyboard", "actions": actions}]},
            )

    def select(self, name, value):
        self.field(name)
        label = self.ui.execute(
            "[...document.activeElement.options].find(o=>o.value === "
            + json.dumps(str(value))
            + ").textContent"
        )
        # Native macOS closed selects support typed option search. Unlike DOM
        # selected-value assignment, these are actual keyboard events.
        self.type_keys(label)
        self.key("Tab")
        assert self.ui.execute(
            "document.querySelector('[name=" + name + "]').value"
        ) == str(value), "Native keyboard option search did not select expected value"

    def date(self, name, value):
        self.field(name)
        # Empty segmented dates ignore printable text in headless macOS Chrome.
        # Native arrows initialize every segment, then adjust to the desired date.
        for _ in range(3):
            self.key("ArrowLeft")
        for index in range(3):
            self.key("ArrowUp")
            if index < 2:
                self.key("ArrowRight")
        current = self.ui.execute("document.querySelector('[name=" + name + "]').value")
        assert current, "Native arrow keys did not initialize date segments"
        year, month, day = map(int, current.split("-"))
        want_year, want_month, want_day = map(int, value.split("-"))
        self.key("ArrowLeft")
        self.key("ArrowLeft")
        order = self.ui.execute(
            "new Intl.DateTimeFormat().formatToParts(new Date()).map(p=>p.type).filter(t=>['day','month','year'].includes(t))"
        )
        values = {
            "month": (month, want_month),
            "day": (day, want_day),
            "year": (year, want_year),
        }
        for index, part in enumerate(order):
            actual, desired = values[part]
            for _ in range(abs(desired - actual)):
                self.key("ArrowUp" if desired > actual else "ArrowDown")
            if index < 2:
                self.key("ArrowRight")
        self.key("Tab")
        assert (
            self.ui.execute("document.querySelector('[name=" + name + "]').value")
            == value
        )

    def button(self, text):
        self.focus(
            "document.activeElement.tagName === 'BUTTON' && document.activeElement.textContent.trim() === "
            + json.dumps(text)
        )
        self.activate()

    def link(self, text):
        self.focus(
            "document.activeElement.tagName === 'A' && document.activeElement.textContent.trim() === "
            + json.dumps(text)
        )
        self.activate()

    def activate(self):
        self.ui.execute("(window.__releasePreviousBody = document.body, true)")
        self.ui.press("Enter")
        native.wait_for(self.ui, "document.body !== window.__releasePreviousBody", True)

    def heading(self, text):
        native.wait_heading(self.ui, text)
        assert self.ui.execute("innerWidth") == 1280 // self.ui.zoom
        assert self.ui.execute("innerHeight") == 720 // self.ui.zoom
        assert not self.ui.execute("document.documentElement.scrollWidth > innerWidth")
