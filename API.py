from modules.taskmanager import TaskManager
class API:
    def __init__(self, manager=TaskManager()):
        self.manager = manager

    def pridej_objednavku(self, nazev: str, cena: float):
        """Přidá objednávku do task manageru.

        Args:
            nazev (str): Název objednávky.
            cena (float): Cena objednávky, musí být nezáporná.

        Raises:
            TypeError: Pokud nazev není string nebo cena není číslo.
            ValueError: Pokud cena je záporná.
        """

        if not isinstance(nazev, str):
            raise TypeError("nazev musí být string")
        if not isinstance(cena, (int, float)):
            raise TypeError("cena musí být číslo")
        if cena < 0:
            raise ValueError("cena nesmí být záporná")

        return self.manager.pridej_objednavku(nazev, cena)


 

if __name__ == "__main__":
    test = API()

    print(test.pridej_objednavku("Kure",123.45))

    try:
        test.pridej_objednavku(12, 25)
    except TypeError:
        print("passed")

    try:
        test.pridej_objednavku("kure", "asd")
    except TypeError:
        print("passed")

    try:
        test.pridej_objednavku("kure", -2)
    except ValueError:
        print("passed")