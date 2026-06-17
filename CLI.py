from API import API


class CLI:
    def __init__(self, api: API | None = None):
        self.api = api if api is not None else API()
        self.api.nacti_z_json()

    def pridat_objednavku(self):
        nazev = input("Zadejte název položky: ").strip()
        if not nazev:
            print("Nebyl zadán název položky.")
            return

        while True:
            cena_text = input("Zadejte cenu položky: ").strip()
            if not cena_text:
                print("Cena nesmí být prázdná.")
                continue
            try:
                cena = float(cena_text.replace(",", "."))
                break
            except ValueError:
                print("Zadejte platnou cenu.")

        try:
            objednavka = self.api.pridej_objednavku(nazev, cena)
            print(f"Objednávka přidána: {objednavka.nazev} ({objednavka.cena} CZK)")
        except Exception:
            print("Nepodařilo se přidat objednávku.")

    def zobrazit_vsechny(self):
        try:
            objednavky = self.api.vsechny_objednavky()
        except Exception:
            objednavky = []

        if not objednavky:
            print("Žádné objednávky k zobrazení.")
        else:
            for objednavka in objednavky:
                print(objednavka)

    def zobrazit_podle_stavu(self):
        stav = input("Zadejte stav objednávek: ").strip()
        try:
            objednavky = self.api.objednavky_podle_stavu(stav)
        except Exception:
            objednavky = []

        if not objednavky:
            print(f"Žádné objednávky se stavem {stav}.")
        else:
            for objednavka in objednavky:
                print(objednavka)

    def zmenit_stav(self):
        try:
            task_id = int(input("Zadejte ID objednávky: ").strip())
        except ValueError:
            print("ID musí být číslo.")
            return

        novy_stav = input("Zadejte nový stav: ").strip()
        try:
            self.api.zmen_stav_objednavky(task_id, novy_stav)
            print("Stav objednávky byl změněn.")
        except Exception as e:
            print(f"Nepodařilo se změnit stav objednávky: {e}")

    def zobrazit_obrat(self):
        try:
            obrat = self.api.celkovy_obrat()
        except Exception:
            obrat = None

        if obrat is None:
            print("Obrat není k dispozici.")
        else:
            print(f"Celkový obrat: {obrat:.2f} CZK")

    def ukoncit(self):
        self.api.uloz_do_json()
        print("Objednávky uloženy.")

    def spustit(self):
        while True:
            print("\n1. Přidat objednávku")
            print("2. Zobrazit všechny objednávky")
            print("3. Zobrazit objednávky podle stavu")
            print("4. Změnit stav objednávky")
            print("5. Zobrazit celkový obrat")
            print("6. Konec")
            volba = input("Vyber možnost: ").strip()

            if volba == "1":
                self.pridat_objednavku()
            elif volba == "2":
                self.zobrazit_vsechny()
            elif volba == "3":
                self.zobrazit_podle_stavu()
            elif volba == "4":
                self.zmenit_stav()
            elif volba == "5":
                self.zobrazit_obrat()
            elif volba == "6":
                self.ukoncit()
                break
            else:
                print("Neplatná volba.")


if __name__ == "__main__":
    CLI().spustit()
