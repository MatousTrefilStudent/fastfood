import pytest
import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))

from modules.task import Task

"""Generované github copilotem"""

def test_vytvoreni_objednavky():
    o = Task(1, "Burger", 150.0)
    assert o.task_id == 1
    assert o.nazev == "Burger"
    assert o.cena == 150.0
    assert o.stav == "prijata"


def test_vychozi_stav_je_prijata():
    o = Task(2, "Pizza", 200.0)
    assert o.stav == "prijata"


def test_zmena_stavu_na_platnou_hodnotu():
    o = Task(1, "Kebab", 120.0)
    o.zmen_stav("pripravuje_se")
    assert o.stav == "pripravuje_se"
    o.zmen_stav("vydana")
    assert o.stav == "vydana"


def test_to_dict_a_from_dict():
    o = Task(5, "Hranolky", 60.0, "pripravuje_se")
    slovnik = o.to_dict()
    obnovena = Task.from_dict(slovnik)
    assert obnovena.task_id == o.task_id
    assert obnovena.nazev == o.nazev
    assert obnovena.cena == o.cena
    assert obnovena.stav == o.stav


def test_str_obsahuje_nazev_a_cenu():
    o = Task(1, "Cola", 40.0)
    text = str(o)
    assert "Cola" in text
    assert "40" in text


# ---- Negativní testy ----

def test_neplatny_stav_pri_vytvoreni():
    with pytest.raises(ValueError, match="Neplatný stav"):
        Task(1, "Burger", 100.0, stav="hotovo")


def test_neplatny_stav_pri_zmene():
    o = Task(1, "Burger", 100.0)
    with pytest.raises(ValueError, match="Neplatný stav"):
        o.zmen_stav("zrusena")


def test_zaporna_cena_vyhodi_chybu():
    with pytest.raises(ValueError, match="záporná"):
        Task(1, "Burger", -50.0)