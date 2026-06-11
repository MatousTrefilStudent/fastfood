import os

from modules.taskmanager import TaskManager
from modules.task import PLATNE_STAVY

spravce = TaskManager()

MENU = """
Správce úloh fastfoodu
1. Přidat objednávku
2. Zobrazit všechny objednávky
3. Zobrazit objednávky podle stavu
4. Změnit stav objednávky
5. Zobrazit celkový obrat
6. Ukončit správce úloh
"""

POPIS_STAVU = {
    "prijata":       "Přijata",
    "pripravuje_se": "Připravuje se",
    "vydana":        "Vydána",
}


def vycisti_terminal():
    """Vyčistí terminál podle použitého operačního systému."""
    if os.name == "nt":
        os.system("cls")
    else:
        os.system("clear")


def vypis_objednavky(objednavky):
    if not objednavky:
        print("  Žádné objednávky k zobrazení.")
        return
    print()
    for o in objednavky:
        print(" ", o)
    print()


# ------------------------------------------------------------------ #
# Akce menu
# ------------------------------------------------------------------ #
def pridat_objednavku():
    nazev = input("  Název položky: ").strip()
    if not nazev:
        print("  Chyba: název nesmí být prázdný.")
        return

    try:
        cena = float(input("  Cena (Kč): ").replace(",", "."))
    except ValueError:
        print("  Chyba: zadej číslo.")
        return

    objednavka = spravce.pridej_objednavku(nazev, cena)
    print(f"  ✓ Objednávka #{objednavka.task_id} přidána.")


def zobrazit_vsechny():
    vypis_objednavky(spravce.vsechny_objednavky())


def zobrazit_podle_stavu():
    print("  Dostupné stavy:")
    for klic, popis in POPIS_STAVU.items():
        print(f"    {klic} – {popis}")
    stav = input("  Zadej stav: ").strip()
    if stav not in PLATNE_STAVY:
        print(f"  Chyba: neplatný stav '{stav}'.")
        return
    vypis_objednavky(spravce.objednavky_podle_stavu(stav))


def zmenit_stav():
    try:
        task_id = int(input("  ID objednávky: "))
    except ValueError:
        print("  Chyba: ID musí být číslo.")
        return

    print("  Dostupné stavy:")
    for klic, popis in POPIS_STAVU.items():
        print(f"    {klic} – {popis}")
    novy_stav = input("  Nový stav: ").strip()

    try:
        spravce.zmen_stav_objednavky(task_id, novy_stav)
        print("  Stav změněn.")
    except (KeyError, ValueError) as e:
        print(f"  Chyba: {e}")


def zobrazit_obrat():
    obrat = spravce.celkovy_obrat()
    print(f"\n  Celkový obrat (vydané objednávky): {obrat:.2f} Kč\n")


# ------------------------------------------------------------------ #
# Hlavní smyčka
# ------------------------------------------------------------------ #
AKCE = {
    "1": pridat_objednavku,
    "2": zobrazit_vsechny,
    "3": zobrazit_podle_stavu,
    "4": zmenit_stav,
    "5": zobrazit_obrat,
}


def main():
    # Pokus o načtení uložených dat při startu
    try:
        spravce.nacti_z_json()
        print("  Objednávky načteny ze souboru.")
    except FileNotFoundError:
        pass

    while True:
        print(MENU)
        volba = input("  Vyber možnost: ").strip()

        if volba == "6":
            spravce.uloz_do_json()
            print("  Objednávky uloženy. Na shledanou!")
            break

        akce = AKCE.get(volba)
        if akce:
            akce()
        else:
            print("  Neznámá volba, zkus to znovu.")


if __name__ == "__main__":
    main()