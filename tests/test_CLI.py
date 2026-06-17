import io
import os
import sys

import pytest

sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))

import CLI as cli_module
from modules.task import Task

"""Generované github copilotem"""

@pytest.fixture
def fake_cli(monkeypatch):
    api = cli_module.API()
    monkeypatch.setattr(api, "nacti_z_json", lambda: None)
    cli = cli_module.CLI(api=api)
    return cli


def test_pridat_objednavku_adds_order_and_prints_success(fake_cli, monkeypatch):
    inputs = iter(["Burger", "12.5"])
    monkeypatch.setattr("builtins.input", lambda prompt="": next(inputs))

    output = io.StringIO()
    monkeypatch.setattr(sys, "stdout", output)

    fake_cli.pridat_objednavku()

    assert len(fake_cli.api.vsechny_objednavky()) == 1
    assert fake_cli.api.vsechny_objednavky()[0].nazev == "Burger"
    assert "Objednávka přidána" in output.getvalue()


def test_pridat_objednavku_with_blank_name_prints_message(fake_cli, monkeypatch):
    monkeypatch.setattr("builtins.input", lambda prompt="": "   ")

    output = io.StringIO()
    monkeypatch.setattr(sys, "stdout", output)

    fake_cli.pridat_objednavku()

    assert "Nebyl zadán název položky" in output.getvalue()


def test_zobrazit_vsechny_prints_orders(fake_cli, monkeypatch):
    monkeypatch.setattr(
        fake_cli.api,
        "vsechny_objednavky",
        lambda: [Task(1, "Burger", 120.0), Task(2, "Pizza", 200.0)],
    )

    output = io.StringIO()
    monkeypatch.setattr(sys, "stdout", output)

    fake_cli.zobrazit_vsechny()

    assert "Burger" in output.getvalue()
    assert "Pizza" in output.getvalue()


def test_zmenit_stav_changes_status_and_prints_success(fake_cli, monkeypatch):
    fake_cli.api.pridej_objednavku("Burger", 120.0)
    inputs = iter(["1", "vydana"])
    monkeypatch.setattr("builtins.input", lambda prompt="": next(inputs))

    output = io.StringIO()
    monkeypatch.setattr(sys, "stdout", output)

    fake_cli.zmenit_stav()

    assert fake_cli.api.vsechny_objednavky()[0].stav == "vydana"
    assert "Stav objednávky byl změněn." in output.getvalue()


def test_zobrazit_obrat_prints_total(fake_cli, monkeypatch):
    monkeypatch.setattr(fake_cli.api, "celkovy_obrat", lambda: 345.5)

    output = io.StringIO()
    monkeypatch.setattr(sys, "stdout", output)

    fake_cli.zobrazit_obrat()

    assert "Celkový obrat: 345.50 CZK" in output.getvalue()


def test_ukoncit_saves_orders(fake_cli, monkeypatch):
    monkeypatch.setattr(fake_cli.api, "uloz_do_json", lambda: None)

    output = io.StringIO()
    monkeypatch.setattr(sys, "stdout", output)

    fake_cli.ukoncit()

    assert "Objednávky uloženy." in output.getvalue()
