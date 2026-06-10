import pytest
import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))

from modules.taskmanager import TaskManager


@pytest.fixture
def spravce():
    m = TaskManager()
    m.pridej_objednavku("Burger", 150.0)
    m.pridej_objednavku("Pizza", 200.0)
    m.pridej_objednavku("Cola", 40.0)
    return m


def test_pridani_objednavky_zvysi_pocet(spravce):
    pocet_pred = len(spravce.vsechny_objednavky())
    spravce.pridej_objednavku("Zmrzlina", 55.0)
    assert len(spravce.vsechny_objednavky()) == pocet_pred + 1


def test_pridana_objednavka_ma_spravne_hodnoty():
    m = TaskManager()
    o = m.pridej_objednavku("Kebab", 130.0)
    assert o.nazev == "Kebab"
    assert o.cena == 130.0
    assert o.stav == "prijata"


def test_vsechny_objednavky_vraci_vsechny(spravce):
    assert len(spravce.vsechny_objednavky()) == 3


def test_filtrace_podle_stavu(spravce):
    objednavky = spravce.vsechny_objednavky()
    spravce.zmen_stav_objednavky(objednavky[0].task_id, "vydana")
    vydane = spravce.objednavky_podle_stavu("vydana")
    assert len(vydane) == 1
    assert vydane[0].nazev == "Burger"


def test_zmena_stavu_objednavky(spravce):
    task_id = spravce.vsechny_objednavky()[0].task_id
    spravce.zmen_stav_objednavky(task_id, "pripravuje_se")
    objednavka = spravce.vsechny_objednavky()[0]
    assert objednavka.stav == "pripravuje_se"


def test_celkovy_obrat_pocita_jen_vydane(spravce):
    objednavky = spravce.vsechny_objednavky()
    # Označíme první dvě jako vydané (150 + 200 = 350)
    spravce.zmen_stav_objednavky(objednavky[0].task_id, "vydana")
    spravce.zmen_stav_objednavky(objednavky[1].task_id, "vydana")
    assert spravce.celkovy_obrat() == 350.0


def test_ulozeni_a_nacteni_json(tmp_path, spravce):
    cesta = str(tmp_path / "test_objednavky.json")
    spravce.uloz_do_json(cesta)
    assert os.path.exists(cesta)

    novy_spravce = TaskManager()
    novy_spravce.nacti_z_json(cesta)
    nactene = novy_spravce.vsechny_objednavky()
    puvodni = spravce.vsechny_objednavky()

    assert len(nactene) == len(puvodni)
    for puvod, nactena in zip(puvodni, nactene):
        assert puvod.task_id == nactena.task_id
        assert puvod.nazev == nactena.nazev
        assert puvod.cena == nactena.cena


# ---- Negativní testy ----

def test_zmena_stavu_neexistujiciho_id(spravce):
    with pytest.raises(KeyError):
        spravce.zmen_stav_objednavky(9999, "vydana")


def test_nacteni_neexistujiciho_souboru():
    m = TaskManager()
    with pytest.raises(FileNotFoundError):
        m.nacti_z_json("/neexistujici/soubor.json")


def test_celkovy_obrat_bez_vydanych_je_nula(spravce):
    # Všechny objednávky jsou ve stavu "prijata" – obrat musí být 0
    assert spravce.celkovy_obrat() == 0.0