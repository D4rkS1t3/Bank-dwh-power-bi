import numpy as np
import pandas as pd
import random
import sqlite3

# ===========================================================================
# Przygotowanie danych do analizy i zapisanie do pliku transakcje_bankowe.csv
# ===========================================================================

# inicjujemy generator liczb losowych
np.random.seed(42)
n_transakcji = 10000
print(n_transakcji)

id_klientow =[f"ACC_{i:04d}" for i in range(1, 201)]# tworzymy 200 klientow, :04d to zeby pokazac wiodace zera np 0001

dane = {
    "transakcja_id": [f"TX_{i:06d}"for i in range(1, n_transakcji+1)],
    "klient_id": [random.choice(id_klientow) for _ in range(n_transakcji)],
    "kwota": np.round(np.random.exponential(scale=3000, size=n_transakcji)+10, 2),#srednia kwota to 3000 ale przedzial 0 do nieskonczonosci
    "typ_operacji": [random.choice(["WPLATA", "WYPLATA", "PRZELEW_KRAJ", "PRZELEW_ZAGR"]) for _ in range(n_transakcji)],
    "data_godzina": pd.date_range("2026-05-01", periods=n_transakcji, freq="min")
}
df = pd.DataFrame(dane)
print(df.head(5))

# podejrzane transakcje

# tuż pod progiem 15 000
for i in range(10):
  df.loc[random.randint(0, n_transakcji-1), "kwota"] = 14900.00 #df.loc[wiersz, kolumna]

# bardzo wysokie kwoty, pranie pieniedzy
for i in range(5):
  df.loc[random.randint(0, n_transakcji-1), "kwota"] = random.randint(120000, 250000)

df.to_csv("transakcje_bankowe.csv", index=False)
print("Plik transakcje_bankowe.csv zostal wygenerowany!")

# =============================================
# Wczytanie danych i przygotowanie bazy danych
# =============================================

df = pd.read_csv('transakcje_bankowe.csv')

conn = sqlite3.connect("bank_dwh.db")
cursor = conn.cursor()

# ===============================================================================
# WYMIAR KLIENCI
# ===============================================================================
unikalni_klienci = df['klient_id'].unique()
miasta = ["Warszawa", "Krakow", "Gdansk", "Wroclaw", "Poznan", "Lublin", "Ryki", "Pulawy"]
segmenty = ["Standard", "Premium", "VIP"]

dane_klientow = []
for cid in unikalni_klienci:
  dane_klientow.append({
      "klient_id": cid,
      "miasto": miasta[hash(cid) % len(miasta)],
      "segmenty": segmenty[hash(cid) % len(segmenty)]
  })

wymiar_klientow = pd.DataFrame(dane_klientow)
wymiar_klientow.to_sql('wymiar_klientow', conn, if_exists='replace', index=False)

# ====================================================================
# WYMIAR TYPY OPERACJI
# ====================================================================
unikalne_typy = df['typ_operacji'].unique()
wymiar_typy = pd.DataFrame({
    "rodzaj_operacji": range(1, len(unikalne_typy)+1),
    "nazwa_operacji": unikalne_typy
})
wymiar_typy.to_sql('wymiar_typy', conn, if_exists='replace', index=False)

# =============================================
# TABELA FAKTOW TRANSAKCJE
# ==============================================
fakt_transakcje = df.merge(wymiar_typy, left_on='typ_operacji', right_on='nazwa_operacji')
fakt_transakcje = fakt_transakcje[["transakcja_id", "klient_id", "rodzaj_operacji", "kwota", "data_godzina"]]

fakt_transakcje.to_sql('fakt_transakcje', conn, if_exists='replace', index=False)

conn.close()
print("Hurtownia danych `bank_dwh.db` została utworzona")

with pd.ExcelWriter('bankdwh.xlsx') as writer:
  wymiar_klientow.to_excel(writer, sheet_name='wymiar_klientow', index=False)
  wymiar_typy.to_excel(writer, sheet_name='wymiar_typy', index=False)
  fakt_transakcje.to_excel(writer, sheet_name='fakt_transakcje', index=False)
