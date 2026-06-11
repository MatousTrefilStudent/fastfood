import json
import os
from modules.task import Task

VYCHOZI_SOUBOR = os.path.join(os.path.dirname(__file__), "..", "data", "objednavky.json")


class TaskManager:
    def __init__(self):
        self._objednavky: list[Task] = []
        self._dalsi_id: int = 1


    def _najdi(self, task_id: int) -> Task:
        for objednavka in self._objednavky:
            if objednavka.task_id == task_id:
                return objednavka
        raise KeyError(f"Objednávka s ID {task_id} neexistuje.")


    def pridej_objednavku(self, nazev: str, cena: float) -> Task:
        objednavka = Task(self._dalsi_id, nazev, cena)
        self._objednavky.append(objednavka)
        self._dalsi_id += 1
        return objednavka

    def vsechny_objednavky(self) -> list[Task]:
        return list(self._objednavky)

    def objednavky_podle_stavu(self, stav: str) -> list[Task]:
        return [o for o in self._objednavky if o.stav == stav]

    def zmen_stav_objednavky(self, task_id: int, novy_stav: str) -> Task:
        objednavka = self._najdi(task_id)
        objednavka.zmen_stav(novy_stav)
        return objednavka

    def celkovy_obrat(self) -> float:
        # Počítáme pouze vydané objednávky
        return sum(o.cena for o in self._objednavky if o.stav == "vydana")

    def uloz_do_json(self, cesta: str = VYCHOZI_SOUBOR) -> None:
        os.makedirs(os.path.dirname(cesta), exist_ok=True)
        with open(cesta, "w", encoding="utf-8") as f:
            json.dump([o.to_dict() for o in self._objednavky], f, ensure_ascii=False, indent=4)

    def nacti_z_json(self, cesta: str = VYCHOZI_SOUBOR) -> None:
        if not os.path.exists(cesta):
            raise FileNotFoundError(f"Soubor nenalezen: {cesta}")
        
        with open(cesta, "r", encoding="utf-8") as f:
            try:
                data = json.load(f)
            except json.JSONDecodeError:

                data = []

        if data is None:
            data = []
            
        self._objednavky = [Task.from_dict(d) for d in data]
        
        if self._objednavky:
            self._dalsi_id = max(o.task_id for o in self._objednavky) + 1
        else:
            self._dalsi_id = 1
