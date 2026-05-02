import yfinance as yf
import pandas as pd

YAHOO_SYMBOLY = {
    "USOIL":  "CL=F",
    "XAUUSD": "GC=F",
    "NASDAQ": "NQ=F",
    "CORN":   "ZC=F",
    "COFFEE": "KC=F",
    "US500":  "ES=F",
}

def get_trend_signal(symbol="USOIL"):
    try:
        ticker = YAHOO_SYMBOLY.get(symbol, "CL=F")
        print(f"Stahuji trend data pro: {symbol} ({ticker})")

        df = yf.download(ticker, period="100d", interval="1d", progress=False)

        if df.empty:
            print("Žádná data")
            return 0

        if isinstance(df.columns, pd.MultiIndex):
            df.columns = df.columns.get_level_values(0)

        close = df["Close"].squeeze()
        ma20  = close.rolling(window=20).mean()
        ma50  = close.rolling(window=50).mean()

        cena = float(close.iloc[-1])
        m20  = float(ma20.iloc[-1])
        m50  = float(ma50.iloc[-1])

        print(f"  Cena: {cena:.2f}")
        print(f"  MA20: {m20:.2f}")
        print(f"  MA50: {m50:.2f}")

        if cena > m20 and m20 > m50:
            print("  Trend: BULLISH")
            return 1
        elif cena < m20 and m20 < m50:
            print("  Trend: BEARISH")
            return -1
        else:
            print("  Trend: NEURČITÝ")
            return 0

    except Exception as e:
        print(f"Chyba: {e}")
        return 0

if __name__ == "__main__":
    signal = get_trend_signal("USOIL")
    print("\nVýsledný trend signál:", signal)
    