# Bank Data Warehouse & Power BI Dashboard

Projekt urposzczonej hurtowni danych (DWH) w architekturze **Modelu Gwiazdy (Star Schema)** oraz interaktywnego pulpitu menedżerskiego w **MS Power BI**. System przetwarza wolumen 10 000 transakcji banowych, relizując pełny proces ETL.

## Architektura i Model Danych
Projekt przekształca płaski plik źródłowy w zoptymalizowaną strukturę analityczną:
- **Tabela Faktów (`fakt_transakcje`)**: miary finansowe (`kwota`, `data_godzina`) oraz klucze relacji.
- **Tabela Wymiarów Klienci (`wymiar_klientow`)**: lokalizacja (`miasto`) oraz segmentacja biznesowa (`Standard`, `Premium`, `VIP`).
- **Tabela Wymiarów Typy Operacji (`wymiar_typy`)**: słownik operacji (`WPLATA`, `WYPLATA`, `PRZELEW_KRAJ`, `PRZELEW_ZAGR`).

## Technologie
- **Python (Pandas, NumPy)** - generowanie danych i automatyzacja procesu ETL.
- **SQLite / MS Excel** - silnik bazy danych oraz format wymiany danych (`pd.ExcelWriter`).
- **MS Power BI** - modelowanie relacji (1:wiele) oraz budowa interaktywnego dashboardu.

## Analiza Biznesowa (Dashboard)
Zaimplementowany raport wizualizuje obroty o łącznej wartości **7,78 mln PLN**:
1. **Wolumen i wartość transakcji wg miast** - identyfikacja najbardziej aktywnych miast (m.in. Warszawa, Ryki).
2. **Struktura segmentów klientów** - udział procentowy w obrotach banku (Premium: 27,93%, VIP: 33,73%, Standard: 38,34%).
3. **Karta KPI & Filtry (Slicers)** - agregacja sumaryczna i dynamiczne filtrowanie danych według typu operacji.
