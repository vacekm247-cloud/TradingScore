from datetime import datetime

SEZONNOST = {
    "CORN": {
        1:  1, 2:  1, 3:  1, 4:  1, 5:  1, 6:  0,
        7: -1, 8: -1, 9: -1, 10: 0, 11: 0, 12: 0,
    },
    "COFFEE": {
        1:  1, 2:  1, 3: -1, 4: -1, 5: -1, 6: -1,
        7: -1, 8: -1, 9:  0, 10: 1, 11: 1, 12: 1,
    },
    "USOIL": {
        1: -1, 2: -1, 3:  1, 4:  1, 5:  1, 6:  1,
        7:  1, 8:  0, 9: -1, 10:-1, 11: 0, 12: 0,
    },
    "XAUUSD": {
        1:  1, 2:  0, 3:  0, 4: -1, 5: -1, 6: -1,
        7: -1, 8:  0, 9:  1, 10: 1, 11: 1, 12: 1,
    },
    "NASDAQ": {
        1:  1, 2:  1, 3:  1, 4:  0, 5: -1, 6: -1,
        7:  0, 8:  0, 9: -1, 10: 0, 11: 1, 12: 1,
    },
    "US500": {
        1:  1, 2:  1, 3:  1, 4:  0, 5: -1, 6: -1,
        7:  0, 8:  0, 9: -1, 10: 0, 11: 1, 12: 1,
    },
}

MESICE = {
    1: "Leden", 2: "Únor", 3: "Březen", 4: "Duben",
    5: "Květen", 6: "Červen", 7: "Červenec", 8: "Srpen",
    9: "Září", 10: "Říjen", 11: "Listopad", 12: "Prosinec"
}

def get_sezonnost_signal(symbol: str) -> int:
    mesic = datetime.now().month
    mesic_nazev = MESICE.get(mesic, str(mesic))
    data = SEZONNOST.get(symbol)
    if data is None:
        print(f"Sezónnost: symbol '{symbol}' nenalezen → neutrální")
        return 0
    signal = data.get(mesic, 0)
    popis = "Bullish" if signal == 1 else ("Bearish" if signal == -1 else "Neutrální")
    print(f"Sezónnost [{symbol}] {mesic_nazev}: {popis}")
    return signal

if __name__ == "__main__":
    symboly = ["CORN", "COFFEE", "USOIL", "XAUUSD", "NASDAQ", "US500"]
    mesic = datetime.now().month
    print(f"=== Sezónnost pro {MESICE[mesic]} ===\n")
    for s in symboly:
        sig = get_sezonnost_signal(s)
        popis = "🟢 Bullish" if sig == 1 else ("🔴 Bearish" if sig == -1 else "⚪ Neutrální")
        print(f"  {s:8} → {popis}\n")
        