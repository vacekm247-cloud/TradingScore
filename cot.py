import cot_reports as cot
import pandas as pd

def get_cot_signal(symbol="CRUDE OIL"):
    """
    Stáhne COT data pomocí knihovny cot-reports a vyhodnotí signál.
    Vrací: 1 = Bullish, -1 = Bearish, 0 = Neutrální
    """
    try:
        print("Stahuji COT data...")
        
        # Stažení Legacy Futures Only reportu
        df = cot.cot_year(2025, cot_report_type="legacy_fut")
        
        # Filtr na symbol
        df_filtered = df[df["Market and Exchange Names"].str.contains(symbol, case=False, na=False)]
        
        if df_filtered.empty:
            print(f"Symbol '{symbol}' nenalezen")
            return 0
        
        # Nejnovější data
        latest = df_filtered.iloc[-1]
        
        # Net pozice Non-Commercial (spekulanti)
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
    