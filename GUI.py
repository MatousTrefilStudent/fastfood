from API import API
import tkinter as tk
from tkinter import simpledialog

class GUI:
    def __init__(self):
        self.api = API()
        self.api.nacti_z_json()  # Načte objednávky při spuštění GUI
        self.root = tk.Tk()
        self.root.title("FastFood Objednávkový Systém")
        self.root.geometry("400x300")

        self.buttons = [tk.Button(self.root, text="Přidat objednávku", command=self.pridat_objednavku, width=30, height=2),
                        tk.Button(self.root, text="Zobrazit všechny objednávky", command=self.zobrazit_vsechny, width=30, height=2),
                        tk.Button(self.root, text="Zobrazit objednávky podle stavu", command=self.zobrazit_podle_stavu, width=30, height=2),
                        tk.Button(self.root, text="Změnit stav objednávky", command=self.zmenit_stav, width=30, height=2),
                        tk.Button(self.root, text="Zobrazit celkový obrat", command=self.zobrazit_obrat, width=30, height=2),
                        tk.Button(self.root, text="Ukončit", command=self.ukoncit, width=30, height=2)]
        
        for button in self.buttons:
            button.pack(pady=3, anchor="w")
        

    def pridat_objednavku(self):
        nazev = simpledialog.askstring("Přidat objednávku", "Zadejte název položky:", parent=self.root)
        if nazev is None or not nazev.strip():
            tk.messagebox.showinfo("Objednávka", "Nebyl zadán název položky.", parent=self.root)
            return

        while True:
            cena_text = simpledialog.askstring("Přidat objednávku", "Zadejte cenu položky:", parent=self.root)
            if cena_text is None:
                return
            cena_text = cena_text.strip()
            if not cena_text:
                tk.messagebox.showerror("Chyba", "Cena nesmí být prázdná.", parent=self.root)
                continue
            try:
                cena = float(cena_text.replace(",", "."))
                break
            except ValueError:
                tk.messagebox.showerror("Chyba", "Zadejte platnou cenu.", parent=self.root)

        try:
            self.api.pridej_objednavku(nazev, cena)
            tk.messagebox.showinfo("Objednávka přidána", f"Objednávka přidána: {nazev} ({cena}CZK)", parent=self.root)
        except Exception:
            tk.messagebox.showerror("Chyba", "Nepodařilo se přidat objednávku.", parent=self.root)


    def zobrazit_vsechny(self):
        objednavky = []
        try:
            objednavky = self.api.vsechny_objednavky() if hasattr(self.api, 'vsechny_objednavky') else []
        except Exception:
            objednavky = []
        text = "Žádné objednávky k zobrazení." if not objednavky else "\n".join(str(o) for o in objednavky)
        tk.messagebox.showinfo("Všechny objednávky", text, parent=self.root)


    def zobrazit_podle_stavu(self):
        stav = tk.simpledialog.askstring("Objednávky podle stavu", "Zadejte stav objednávek:", parent=self.root)
        if stav is None:
            return
        objednavky = []
        try:
            objednavky = self.api.objednavky_podle_stavu(stav)
            print(objednavky)
        except Exception:
            objednavky = []

        print(objednavky)

        if objednavky is None:
            text = "Žádné objednávky se stavem " + stav
        else:
            text = "Žádné objednávky k zobrazení." if not objednavky else "\n".join(str(o) for o in objednavky)
        tk.messagebox.showinfo("Objednávky podle stavu", text, parent=self.root)

    def zmenit_stav(self):
        objednavka_id = tk.simpledialog.askstring("Změnit stav", "Zadejte ID objednávky:", parent=self.root)
        if objednavka_id is None:
            return
        
        novy_stav = tk.simpledialog.askstring("Změnit stav", "Zadejte nový stav:", parent=self.root)
        if novy_stav is None:
            return
        try:
            self.api.zmen_stav_objednavky(int(objednavka_id), novy_stav)
            tk.messagebox.showinfo("Změna stavu", "Stav objednávky byl změněn.", parent=self.root)
        except Exception as e: # Zachytí chybu do proměnné 'e'
            print(f"DEBUG CHYBA: {e}") # Vytiskne text chyby do konzole
            tk.messagebox.showerror("Chyba", "Nepodařilo se změnit stav objednávky.", parent=self.root)

    def zobrazit_obrat(self):
        obrat = None
        try:
            obrat = self.api.celkovy_obrat()
        except Exception:
            obrat = None

        text=""
        if obrat:
            text = "Celkový obrat: {:.2f} CZK".format(obrat)
        else:
            text = "Obrat není k dispozici"
        tk.messagebox.showinfo("Celkový obrat", text, parent=self.root)

    def ukoncit(self):
        self.api.uloz_do_json()
        self.root.destroy()

        
"""AKCE = {
    "1": pridat_objednavku,
    "2": zobrazit_vsechny,
    "3": zobrazit_podle_stavu,
    "4": zmenit_stav,
    "5": zobrazit_obrat,
}"""

if __name__ == "__main__":
    gui=GUI()
    input()