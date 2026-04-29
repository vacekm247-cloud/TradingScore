from flask import Flask, render_template, request
from cot import get_cot_signal
from kalendar import get_kalendar_signal
from mt4 import get_mt4_signal
from trend import get_trend_signal
from sezonnost import get_sezonnost_signal

app = Flask(__name__)

COT_SYMBOLY = {
    "USOIL":  "CRUDE OIL",
    "XAUUSD": "GOLD",
    "NASDAQ": "NASDAQ",
    "CORN":   "CORN",
    "COFFEE": "COFFEE",
    "US500":  "S&P 500"
}

@app.route("/")
def index():
    mt4_data   = get_mt4_signal()
    mt4_symbol = mt4_data.get("symbol", "").replace("_stp", "") if mt4_data else ""
    mt4_signal = mt4_data.get("signal", "") if mt4_data else ""
    mt4_cas    = mt4_data.get("cas", "") if mt4_data else ""
    return render_template("index.html",
                           mt4_symbol=mt4_symbol,
                           mt4_signal=mt4_signal,
                           mt4_cas=mt4_cas)

@app.route("/score", methods=["POST"])
def score():
    symbol = request.form.get("symbol")

    mt4_data = get_mt4_signal()
    if mt4_data and mt4_data.get("signal") in ["BULLISH", "BEARISH"]:
        pinbar     = 1
        mt4_signal = mt4_data.get("signal")
        mt4_cas    = mt4_data.get("cas", "")
        mt4_purple = mt4_data.get("purple", "")
    else:
        pinbar     = 0
        mt4_signal = "Žádný signál"
        mt4_cas    = ""
        mt4_purple = ""

    trend     = get_trend_signal(symbol)
    cot_symbol = COT_SYMBOLY.get(symbol, "CRUDE OIL")
    cot       = get_cot_signal(cot_symbol)
    kalendar  = get_kalendar_signal()
    sezonnost = get_sezonnost_signal(symbol)

    skore  = pinbar                        * 30
    skore += (1 if trend == 1 else 0)      * 25
    skore += (1 if cot == 1 else 0)        * 20
    skore += (1 if sezonnost == 1 else 0)  * 15
    skore += (1 if kalendar == 1 else 0)   * 10

    trend_popis = "Bullish" if trend == 1 else ("Bearish" if trend == -1 else "Neurčitý")
    cot_popis   = "Bullish" if cot == 1 else ("Bearish" if cot == -1 else "Neutrální")
    sezon_popis = "Bullish" if sezonnost == 1 else ("Bearish" if sezonnost == -1 else "Neutrální")
    kal_popis   = "Žádné riziko" if kalendar == 1 else ("Menší zprávy" if kalendar == 0 else "Vysoké riziko!")

    # Detekce konfliktu — pin bar jde proti trendu
    konflikt = ""
    if pinbar == 1 and mt4_signal == "BULLISH" and trend == -1:
        konflikt = "⚠️ POZOR: Pin Bar je BULLISH ale trend je Bearish — signál jde proti trendu!"
    elif pinbar == 1 and mt4_signal == "BEARISH" and trend == 1:
        konflikt = "⚠️ POZOR: Pin Bar je BEARISH ale trend je Bullish — signál jde proti trendu!"

    if skore >= 80:
        hodnoceni = "Silný signál - vstup zvážit"
        barva = "success"
    elif skore >= 50:
        hodnoceni = "Středně silný signál - opatrně"
        barva = "warning"
    else:
        hodnoceni = "Slabý signál - raději nečekat"
        barva = "danger"

    return render_template("score.html",
                           symbol=symbol,
                           skore=skore,
                           hodnoceni=hodnoceni,
                           barva=barva,
                           mt4_signal=mt4_signal,
                           mt4_cas=mt4_cas,
                           mt4_purple=mt4_purple,
                           trend_popis=trend_popis,
                           cot_popis=cot_popis,
                           sezon_popis=sezon_popis,
                           kal_popis=kal_popis,
                           konflikt=konflikt)

if __name__ == "__main__":
    import webbrowser
    webbrowser.open("http://127.0.0.1:5000")
    app.run(debug=True)
    