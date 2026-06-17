from modules.taskmanager import TaskManager
from modules.task import Task


class API:
    def __init__(self, manager: TaskManager | None = None) -> None:
        self.manager = manager if manager is not None else TaskManager()

    def pridej_objednavku(self, nazev: str, cena: float) -> Task:
        """Přidá novou objednávku do systému.

        Args:
            nazev (str): Název objednávky.
            cena (float): Cena objednávky, která musí být nezáporná.

        Returns:
            Task: Vytvořená objednávka.

        Raises:
            TypeError: Pokud je `nazev` jiného typu než `str` nebo
                pokud `cena` není číslo.
            ValueError: Pokud je `cena` záporná.
        """
        if not isinstance(nazev, str):
            raise TypeError("nazev musí být string")
        if not isinstance(cena, (int, float)):
            raise TypeError("cena musí být číslo")
        if cena < 0:
            raise ValueError("cena nesmí být záporná")

        return self.manager.pridej_objednavku(nazev, cena)

    def vsechny_objednavky(self) -> list[Task]:
        """Vrátí seznam všech objednávek.

        Returns:
            list[Task]: Seznam všech uložených objednávek.
        """
        return self.manager.vsechny_objednavky()

    def objednavky_podle_stavu(self, stav: str) -> list[Task]:
        """Vrátí seznam objednávek podle zadaného stavu.

        Args:
            stav (str): Stav objednávky, podle kterého se mají filtrovat.

        Returns:
            list[Task]: Seznam objednávek, které odpovídají zadanému stavu.
        """
        return self.manager.objednavky_podle_stavu(stav)

    def zmen_stav_objednavky(self, task_id: int, novy_stav: str) -> Task:
        """Změní stav objednávky.

        Args:
            task_id (int): ID objednávky, jejíž stav se má změnit.
            novy_stav (str): Nový stav objednávky.

        Returns:
            Task: Objednávka s aktualizovaným stavem.
        """
        return self.manager.zmen_stav_objednavky(task_id, novy_stav)

    def celkovy_obrat(self) -> float:
        """Vrátí celkový obrat z vydaných objednávek.

        Returns:
            float: Celkový obrat z vydaných objednávek.
        """
        return self.manager.celkovy_obrat()

    def uloz_do_json(self, cesta: str = "data/objednavky.json") -> None:
        """Uloží všechny objednávky do JSON souboru.

        Args:
            cesta (str): Cesta k souboru, kam se mají objednávky uložit.
        """
        self.manager.uloz_do_json(cesta)

    def nacti_z_json(self, cesta: str = "data/objednavky.json") -> None:
        """Načte objednávky ze JSON souboru.

        Args:
            cesta (str): Cesta k souboru, ze kterého se mají objednávky načíst.
        """
        self.manager.nacti_z_json(cesta)


if __name__ == "__main__":
    test = API()