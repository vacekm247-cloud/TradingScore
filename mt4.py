def get_mt4_signal():
    """
    Přečte signál zapsaný MT4 indikátorem PT_PinBar_Oil.
    Vrací: slovník s daty nebo None pokud soubor neexistuje
    """
    soubor = r"C:\Users\mvace\AppData\Roaming\MetaQuotes\Terminal\B0BD842222E325E29574A178994914CC\MQL4\Files\TradingScore_signal.txt"

    try:
        data = {}
        with open(soubor, "r") as f:
            for radek in f:
                radek = radek.strip()
                if "=" in radek:
                    klic, hodnota = radek.split("=", 1)
                    data[klic] = hodnota

        print("MT4 data:", data)
        return data

    except FileNotFoundError:
        print("Soubor nenalezen - MT4 zatím nezapsal žádný signál")
        return None
    except Exception as e:
        print(f"Chyba při čtení MT4 souboru: {e}")
        return None


if __name__ == "__main__":
    signal = get_mt4_signal()
    if signal:
        print("\nSymbol:", signal.get("symbol"))
        print("Signál:", signal.get("signal"))
        print("Purple Level:", signal.get("purple"))
        print("Čas:", signal.get("cas"))
    else:
        print("Žádný signál z MT4")
        