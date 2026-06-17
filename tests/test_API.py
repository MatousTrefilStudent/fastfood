import os
import sys

import pytest

sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))

from API import API
from modules.taskmanager import TaskManager

"""Generované github copilotem"""

@pytest.fixture
def api():
    return API(TaskManager())


def test_pridej_objednavku_prida_objednavku(api):
    objednavka = api.pridej_objednavku("Burger", 120.5)

    assert objednavka.nazev == "Burger"
    assert objednavka.cena == 120.5
    assert objednavka.stav == "prijata"
    assert len(api.vsechny_objednavky()) == 1


def test_vsechny_objednavky_vraci_vsechny(api):
    api.pridej_objednavku("Burger", 120)
    api.pridej_objednavku("Pizza", 200)

    objednavky = api.vsechny_objednavky()

    assert len(objednavky) == 2
    assert [o.nazev for o in objednavky] == ["Burger", "Pizza"]


def test_objednavky_podle_stavu_filtruje(api):
    api.pridej_objednavku("Burger", 120)
    api.pridej_objednavku("Pizza", 200)

    api.zmen_stav_objednavky(1, "vydana")

    vydane = api.objednavky_podle_stavu("vydana")

    assert len(vydane) == 1
    assert vydane[0].nazev == "Burger"


def test_zmen_stav_objednavky_aktualizuje_stav(api):
    api.pridej_objednavku("Burger", 120)

    objednavka = api.zmen_stav_objednavky(1, "pripravuje_se")

    assert objednavka.stav == "pripravuje_se"
    assert api.vsechny_objednavky()[0].stav == "pripravuje_se"


def test_celkovy_obrat_pocita_jen_vydane(api):
    api.pridej_objednavku("Burger", 120)
    api.pridej_objednavku("Pizza", 200)

    api.zmen_stav_objednavky(1, "vydana")
    api.zmen_stav_objednavky(2, "vydana")

    assert api.celkovy_obrat() == 320.0


def test_uloz_do_json_a_nacti_z_json(tmp_path, api):
    api.pridej_objednavku("Burger", 120)
    api.pridej_objednavku("Pizza", 200)

    cesta = tmp_path / "test_objednavky.json"
    api.uloz_do_json(str(cesta))

    assert os.path.exists(cesta)

    novy_api = API(TaskManager())
    novy_api.nacti_z_json(str(cesta))

    assert len(novy_api.vsechny_objednavky()) == 2
    assert [o.nazev for o in novy_api.vsechny_objednavky()] == ["Burger", "Pizza"]


def test_pridej_objednavku_nepovoluje_neplatny_nazev(api):
    with pytest.raises(TypeError):
        api.pridej_objednavku(123, 10)


def test_pridej_objednavku_nepovoluje_neplatnou_cenu(api):
    with pytest.raises(TypeError):
        api.pridej_objednavku("Burger", "dva")


def test_pridej_objednavku_nepovoluje_zapornou_cenu(api):
    with pytest.raises(ValueError):
        api.pridej_objednavku("Burger", -5)


def test_nacti_z_json_neexistujiciho_souboru():
    api = API(TaskManager())

    with pytest.raises(FileNotFoundError):
        api.nacti_z_json("/neexistujici/soubor.json")

