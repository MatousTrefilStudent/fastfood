import os
import sys
import types

import pytest

sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))

import GUI as gui_module
from modules.task import Task

"""Generované github copilotem"""

class FakeRoot:
    def __init__(self):
        self.destroyed = False

    def title(self, *_args, **_kwargs):
        pass

    def geometry(self, *_args, **_kwargs):
        pass

    def destroy(self):
        self.destroyed = True


class FakeButton:
    def __init__(self, *args, **kwargs):
        self.command = kwargs.get("command")

    def pack(self, *args, **kwargs):
        pass


class FakeMessageBox:
    def __init__(self):
        self.calls = []

    def showinfo(self, title, message, **kwargs):
        self.calls.append(("info", title, message))

    def showerror(self, title, message, **kwargs):
        self.calls.append(("error", title, message))


@pytest.fixture
def fake_gui(monkeypatch):
    fake_root = FakeRoot()
    fake_messagebox = FakeMessageBox()

    monkeypatch.setattr(gui_module.tk, "Tk", lambda: fake_root)
    monkeypatch.setattr(gui_module.tk, "Button", FakeButton)
    monkeypatch.setattr(gui_module.tk, "messagebox", fake_messagebox)
    monkeypatch.setattr(
        gui_module.tk,
        "simpledialog",
        types.SimpleNamespace(askstring=lambda *args, **kwargs: None),
    )
    monkeypatch.setattr(
        gui_module.simpledialog,
        "askstring",
        lambda *args, **kwargs: None,
    )
    monkeypatch.setattr(gui_module.API, "nacti_z_json", lambda self: None)

    gui = gui_module.GUI()
    gui._fake_messagebox = fake_messagebox
    gui._fake_root = fake_root
    return gui


def test_gui_init_creates_expected_number_of_buttons(fake_gui):
    assert len(fake_gui.buttons) == 6


def test_pridat_objednavku_with_blank_name_shows_info(fake_gui, monkeypatch):
    monkeypatch.setattr(
        gui_module.simpledialog,
        "askstring",
        lambda *args, **kwargs: "   ",
    )

    fake_gui.pridat_objednavku()

    assert fake_gui._fake_messagebox.calls[-1][0] == "info"
    assert "Nebyl zadán název" in fake_gui._fake_messagebox.calls[-1][2]


def test_pridat_objednavku_adds_order_and_shows_success(fake_gui, monkeypatch):
    answers = iter(["Burger", "12.5"])
    monkeypatch.setattr(
        gui_module.simpledialog,
        "askstring",
        lambda *args, **kwargs: next(answers),
    )

    fake_gui.pridat_objednavku()

    assert len(fake_gui.api.vsechny_objednavky()) == 1
    assert fake_gui.api.vsechny_objednavky()[0].nazev == "Burger"
    assert fake_gui._fake_messagebox.calls[-1][0] == "info"
    assert "Objednávka přidána" in fake_gui._fake_messagebox.calls[-1][1]


def test_zobrazit_vsechny_shows_all_orders(fake_gui, monkeypatch):
    monkeypatch.setattr(
        fake_gui.api,
        "vsechny_objednavky",
        lambda: [Task(1, "Burger", 120.0), Task(2, "Pizza", 200.0)],
    )

    fake_gui.zobrazit_vsechny()

    assert fake_gui._fake_messagebox.calls[-1][0] == "info"
    assert "Burger" in fake_gui._fake_messagebox.calls[-1][2]
    assert "Pizza" in fake_gui._fake_messagebox.calls[-1][2]


def test_zobrazit_obrat_shows_total(fake_gui, monkeypatch):
    monkeypatch.setattr(fake_gui.api, "celkovy_obrat", lambda: 345.5)

    fake_gui.zobrazit_obrat()

    assert fake_gui._fake_messagebox.calls[-1][0] == "info"
    assert "345.50 CZK" in fake_gui._fake_messagebox.calls[-1][2]


def test_ukoncit_saves_and_destroys_root(fake_gui, monkeypatch):
    monkeypatch.setattr(fake_gui.api, "uloz_do_json", lambda: None)

    fake_gui.ukoncit()

    assert fake_gui._fake_root.destroyed is True
