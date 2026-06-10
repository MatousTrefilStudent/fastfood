PLATNE_STAVY = ("prijata", "pripravuje_se", "vydana")


class Task:
    def __init__(self, task_id: int, nazev: str, cena: float, stav: str = "prijata"):
        if not nazev or not nazev.strip():
            raise ValueError("Název objednávky nesmí být prázdný.")
        if stav not in PLATNE_STAVY:
            raise ValueError(f"Neplatný stav '{stav}'. Povolené stavy: {PLATNE_STAVY}")
        if cena < 0:
            raise ValueError("Cena nesmí být záporná.")

        self.task_id = task_id
        self.nazev = nazev.strip()
        self.cena = cena
        self.stav = stav

    def zmen_stav(self, novy_stav: str) -> None:
        if novy_stav not in PLATNE_STAVY:
            raise ValueError(f"Neplatný stav '{novy_stav}'. Povolené stavy: {PLATNE_STAVY}")
        self.stav = novy_stav

    def to_dict(self) -> dict:
        return {
            "task_id": self.task_id,
            "nazev": self.nazev,
            "cena": self.cena,
            "stav": self.stav,
        }

    @classmethod
    def from_dict(cls, data: dict) -> "Task":
        return cls(
            task_id=data["task_id"],
            nazev=data["nazev"],
            cena=data["cena"],
            stav=data.get("stav", "prijata"),
        )

    def __str__(self) -> str:
        stavy_popis = {
            "prijata":       "📥 Přijata",
            "pripravuje_se": "🍳 Připravuje se",
            "vydana":        "✅ Vydána",
        }
        popis_stavu = stavy_popis.get(self.stav, self.stav)
        return (
            f"[{self.task_id:>3}] {self.nazev:<30} "
            f"{self.cena:>8.2f} Kč   {popis_stavu}"
        )