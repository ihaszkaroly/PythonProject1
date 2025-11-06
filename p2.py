import csv
import sqlite3
import tkinter as tk
from tkinter import messagebox
import p


class KockaDobasMentes(p.KockaDobas):
    def __init__(self, master):
        super().__init__(master)

        # --- A MEGLÉVŐ GOMBJAID ---
        self.mentes_txt = tk.Button(master, text="Mentés txt fájlba", command=self.mentes_txtbe)
        self.mentes_txt.grid(row=3, column=0, pady=10)

        self.mentes_csv = tk.Button(master, text="Mentés csv fájléba", command=self.mentes_csvbe)
        self.mentes_csv.grid(row=3, column=1)

        self.mentes_sql = tk.Button(master, text="Mentés SQL-be", command=self.mentes_sql)
        self.mentes_sql.grid(row=3, column=2)

        # --- ÚJ STATISZTIKAI CÍMKE HOZZÁADÁSA ---
        # 1. Az eredeti címkét kicsit balra igazítjuk, hogy legyen hely
        self.eredmeny_cimke.grid_configure(row=2, column=1, padx=(10, 20), sticky="w")

        # 2. Létrehozzuk az új címkét az összesített statisztikának
        self.osszes_cimke_szovege = tk.StringVar(value="Összesített:\n...")
        self.osszes_cimke = tk.Label(master,
                                     textvariable=self.osszes_cimke_szovege,
                                     font=("Ariel", 14, "italic"),
                                     justify=tk.LEFT,
                                     fg="#00008B")  # Sötétkék szín

        # 3. Elhelyezzük az eredeti statisztika mellé jobbra
        self.osszes_cimke.grid(row=2, column=2, padx=(20, 10), sticky="w")

        # 4. Program indulásakor azonnal betöltjük a statisztikát
        self.sql_statisztika_frissites()

    # --- AZ SQL MENTÉS KIEGÉSZÍTÉSE A FRISSÍTÉSSEL ---
    def mentes_sql(self):
        try:
            conn = sqlite3.connect("kokadobas.db")
            db = conn.cursor()
            db.execute(
                "CREATE TABLE IF NOT EXISTS kocka (dobasok INT, egy INT, ket INT, ha INT, negy INT,  ot INT, hat INT)")
            db.execute("INSERT INTO kocka VALUES (?, ?, ?, ?, ?, ?, ?)", (self.dobasok_szama,
                                                                          self.eredmenyek[1],
                                                                          self.eredmenyek[2],
                                                                          self.eredmenyek[3],
                                                                          self.eredmenyek[4],
                                                                          self.eredmenyek[5],
                                                                          self.eredmenyek[6])
                       )
            conn.commit()
            conn.close()

            # <--- ÚJ RÉSZ: Sikeres mentés után frissítjük a statisztikát ---
            self.sql_statisztika_frissites()
            # <----------------------------------------------------------

        except:
            messagebox.showerror("Hiba", "Nem sikerült az SQL-be mentés!")

    # --- ÚJ FÜGGVÉNY: STATISZTIKA OLVASÁSA SQL-BŐL ---
    def sql_statisztika_frissites(self):
        """Beolvassa az adatbázisból az összesített adatokat és frissíti a címkét."""
        try:
            conn = sqlite3.connect("kokadobas.db")
            db = conn.cursor()

            # SQL parancs, ami összeadja az összes oszlopot
            # Megjegyzés: A 'ha' oszlopot [ha]-ként írjuk, hogy biztos ne legyen kulcsszó probléma
            db.execute("SELECT SUM(egy), SUM(ket), SUM([ha]), SUM(negy), SUM(ot), SUM(hat) FROM kocka")
            eredmeny = db.fetchone()
            conn.close()

            # Ha van eredmény (nem üres a tábla)
            if eredmeny and eredmeny[0] is not None:
                szoveg = (
                    f"Összesített:\n"
                    f"1 - {eredmeny[0]}\n"
                    f"2 - {eredmeny[1]}\n"
                    f"3 - {eredmeny[2]}\n"
                    f"4 - {eredmeny[3]}\n"
                    f"5 - {eredmeny[4]}\n"
                    f"6 - {eredmeny[5]}"
                )
                self.osszes_cimke_szovege.set(szoveg)
            else:
                # Ha még üres az adatbázis
                self.osszes_cimke_szovege.set("Összesített:\n(Nincs adat)")

        except sqlite3.OperationalError:
            # Akkor fut le, ha a 'kocka' tábla még egyáltalán nem létezik
            self.osszes_cimke_szovege.set("Összesített:\n(Még nincs tábla)")
        except Exception as e:
            # Egyéb hiba
            print(f"SQL olvasási hiba: {e}")
            self.osszes_cimke_szovege.set("Összesített:\n(Hiba)")

    # <--- ÚJ FÜGGVÉNY VÉGE ---

    def mentes_csvbe(self):
        fajlnev = "mentes.csv"
        try:
            with open(fajlnev, mode="a", newline="", encoding="utf-8") as csvfajl:
                writer = csv.writer(csvfajl)
                writer.writerow([self.dobasok_szama] + [self.eredmenyek[i] for i in range(1, 7)])
                messagebox.showinfo("Mentés", "Sikeresen mentettem!")
        except:
            messagebox.showerror("Hiba", "Nem sikerült a mentés!")

    def mentes_txtbe(self):
        sor = (f"{self.dobasok_szama}, "
               f"{self.eredmenyek[1]}, {self.eredmenyek[2]}, {self.eredmenyek[3]}, "
               f"{self.eredmenyek[4]}, {self.eredmenyek[5]}, {self.eredmenyek[6]}\n")
        try:
            with open("mentes.txt", "a", encoding="utf-8") as fajl:
                fajl.write(sor)
            messagebox.showinfo("Mentés", "Sikeresen mentettem!")
        except:
            messagebox.showerror("Hiba", "Nem sikerült a mentés!")


# --- Ez a rész nem változik ---
if __name__ == "__main__":
    root = tk.Tk()
    app = KockaDobasMentes(root)
    root.mainloop()