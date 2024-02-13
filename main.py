from datetime import datetime
import json
import os

class Chatbot:
    def __init__(self):
        self.informacie_o_udalosti = {}

    def zadaj_otazku(self, otazka):
        odpoved = input(otazka + " ")
        return odpoved

    def ziskaj_dnesny_datum(self):
        return datetime.today().date()

    def zadaj_datum(self, otazka):
        while True:
            datum = input(otazka + " (DD.MM.RRRR): ")
            try:
                datum_obj = datetime.strptime(datum, "%d.%m.%Y").date()
                if datum_obj > self.ziskaj_dnesny_datum():
                    return datum_obj
                else:
                    print("Zadajte platný dátum, ktorý je neskorší ako dnešný.")
            except ValueError:
                print("Nesprávny formát dátumu. Použite formát DD.MM.RRRR.")

    def zadaj_datum_konca(self, otazka):
        while True:
            datum = input(otazka + " (DD.MM.RRRR): ")
            try:
                datum_obj = datetime.strptime(datum, "%d.%m.%Y").date()
                if datum_obj > self.informacie_o_udalosti["zaciatok"]:
                    return datum_obj
                else:
                    print("Zadajte platný dátum, ktorý je neskorší ako začiatok udalosti.")
            except ValueError:
                print("Nesprávny formát dátumu. Použite formát DD.MM.RRRR.")

    def zadaj_miesto_konania(self):
        miesto = self.zadaj_otazku("Zadajte miesto konania udalosti:")
        self.informacie_o_udalosti["miesto_konania"] = miesto

    def nacitaj_kategorie(self, cesta_k_suboru):
        with open(cesta_k_suboru, "r", encoding="utf-8") as f:
            return json.load(f)

    def zobraz_kategorie(self, kategorie):
        print("Vyberte hlavnú kategóriu udalosti:")
        for index, kategoria in enumerate(kategorie, start=1):
            print(f"{index}. {kategoria['Name']}")
        while True:
            vyber = input("Zadajte číslo hlavnej kategórie: ")
            if vyber.isdigit() and 1 <= int(vyber) <= len(kategorie):
                hlavna_kategoria = kategorie[int(vyber) - 1]
                self.informacie_o_udalosti["kategoria"] = hlavna_kategoria["Name"]
                print("Vyberte podkategóriu udalosti:")
                for index, podkategoria in enumerate(hlavna_kategoria["Subcategories"], start=1):
                    print(f"{index}. {podkategoria}")
                while True:
                    vyber_podkategorie = input("Zadajte číslo podkategórie: ")
                    if vyber_podkategorie.isdigit() and 1 <= int(vyber_podkategorie) <= len(hlavna_kategoria["Subcategories"]):
                        self.informacie_o_udalosti["podkategoria"] = hlavna_kategoria["Subcategories"][int(vyber_podkategorie) - 1]
                        return
                    else:
                        print("Neplatný výber. Zadajte prosím číslo z rozsahu možností.")
            else:
                print("Neplatný výber. Zadajte prosím číslo z rozsahu možností.")

    def ziskaj_informacie_o_udalosti(self):
        self.informacie_o_udalosti["nazov"] = self.zadaj_otazku("Zadajte názov udalosti:")
        kategorie = self.nacitaj_kategorie("kategorie.json")
        self.zobraz_kategorie(kategorie)
        self.zadaj_miesto_konania()
        self.informacie_o_udalosti["zaciatok"] = self.zadaj_datum("Zadajte dátum začiatku udalosti:")
        self.informacie_o_udalosti["koniec"] = self.zadaj_datum_konca("Zadajte dátum konca udalosti (nesmie byť rovnaký alebo pred dátumom začiatku):")


    def zobraz_zhrnutie(self):
        print("Zhrnutie informácií o udalosti:")
        for k, v in self.informacie_o_udalosti.items():
            if isinstance(v, datetime):
                v = v.strftime("%d.%m.%Y")
            print(f"{k.capitalize()}: {v}")

    def uloz_do_suboru(self):
        nazov_suboru = self.informacie_o_udalosti["nazov"].replace(" ", "_") + ".txt"
        with open(nazov_suboru, "w", encoding="utf-8") as f:
            f.write("Zhrnutie informácií o udalosti:\n")
            for k, v in self.informacie_o_udalosti.items():
                if isinstance(v, datetime):
                    v = v.strftime("%d.%m.%Y")
                f.write(f"{k.capitalize()}: {v}\n")
            print(f"Informácie boli uložené do súboru {nazov_suboru}")

    def spytaj_sa_potvrdenia(self):
        odpoved = input("Chcete pokračovať s týmito informáciami a uložiť ich do súboru? (Áno/Nie): ")
        return odpoved.lower() == "ano"

    def vytvor_udalost(self):
        self.ziskaj_informacie_o_udalosti()
        self.zobraz_zhrnutie()
        if self.spytaj_sa_potvrdenia():
            self.uloz_do_suboru()
        else:
            print("Zadanie informácií bolo zrušené.")

if __name__ == "__main__":
    chatbot = Chatbot()
    chatbot.vytvor_udalost()
