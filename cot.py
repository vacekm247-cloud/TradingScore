import cot_reports as cot
import pandas as pd
import os
from datetime import datetime, timedelta

CACHE_FILE = "cot_cache.txt"
CACHE_DATA_FILE = "annual.txt"

def je_cache_platna():
    """
    Kontroluje jestli je cache aktuální - stahujeme jen jednou týdně (v pátek).
    """
    if not os.path.exists(CACHE_FILE):
        return False
    
    try:
        with open(CACHE_FILE, "r") as f:
            datum_str = f.read().strip()
            datum = datetime.strptime(datum_str, "%Y-%m-%d")
            
            # Cache platí 7 dní
            if datetime.now() - datum < timedelta(days=7):
                print(f"Používám cache z: {datum_str}")
                return True
            else:
                print("Cache je stará — stahuji nová data...")
                return False
    except:
        return False

def uloz_cache():
    """Uloží dnešní datum jako datum poslední aktualizace."""
    with open(CACHE_FILE, "w") as f:
        f.write(datetime.now().strftime("%Y-%m-%d"))

def get_cot_signal(symbol="CRUDE OIL"):
    """
    Stáhne COT data (jen jednou týdně) a vyhodnotí signál.
    Vrací: 1 = Bullish, -1 = Bearish, 0 = Neutrální
    """
    try:
        rok = datetime.now().year

        # Stáhnout jen pokud cache není platná
        if not je_cache_platna():
            print("Stahuji COT data...")
            df_new = cot.cot_year(rok, cot_report_type="legacy_fut")
            uloz_cache()
            print(f"Data stažena a uložena do cache.")
        else:
            # Načteme z lokálního souboru
            df_new = pd.read_csv(CACHE_DATA_FILE, low_memory=False)

        # Filtr na symbol
        col = df_new.columns[0]
        df_filtered = df_new[df_new[col].str.contains(symbol, case=False, na=False)]

        if df_filtered.empty:
            print(f"Symbol '{symbol}' nenalezen")
            return 0

        latest = df_filtered.iloc[-1]

        noncom_long  = latest["Noncommercial Positions-Long (All)"]
        noncom_short = latest["Noncommercial Positions-Short (All)"]
        net_noncom   = noncom_long - noncom_short

        print(f"\nCOT {symbol}:")
        print(f"  Non-Com Long:  {noncom_long}")
        print(f"  Non-Com Short: {noncom_short}")
        print(f"  Net pozice:    {net_noncom}")

        if net_noncom > 0:
            print("  Signal: BULLISH")
            return 1
        elif net_noncom < 0:
            print("  Signal: BEARISH")
            return -1
        else:
            return 0

    except Exception as e:
        print(f"Chyba: {e}")
        return 0

if __name__ == "__main__":
    signal = get_cot_signal("CRUDE OIL")
    print("\nVýsledný COT signál:", signal)
    