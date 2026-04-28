from flask import Flask, render_template, request
from cot import get_cot_signal
from kalendar import get_kalendar_signal
from mt4 import get_mt4_signal

app = Flask(__name__)

# COT symboly pro každý instrument
COT_SYMBOLY = {
    "USOIL":  "CRUDE OIL",
    "XAUUSD": "GOLD",
    "NASDAQ": "NASDAQ",
    "CORN":   "CORN",
    "COFFEE": "COFFEE"
}

@app.route("/")
def index():
    # Načtení MT4 signálu pro předvyplnění
    mt4_data = get_mt4_signal()
    mt4_symbol = mt4_data.get("symbol", "").replace("_stp", "") if mt4_data else ""
    mt4_signal = mt4_data.get("signal", "") if mt4_data else ""
    mt4_cas    = mt4_data.get("cas", "") if mt4_data else ""
    mt4_purple = mt4_data.get("purple", "") if mt4_data else ""

    return render_template("index.html",
                           mt4_symbol=mt4_symbol,
                           mt4_signal=mt4_signal,
                           mt4_cas=mt4_cas,
                           mt4_purple=mt4_purple)

@app.route("/score", methods=["POST"])
def score():
    symbol    = request.form.get("symbol")
    trend     = int(request.form.get("trend"))
    sezonnost = int(request.form.get("sezonnost"))

    # Pin Bar automaticky z MT4
    mt4_data = get_mt4_signal()
    if mt4_data and mt4_data.get("signal") in ["BULLISH", "BEARISH"]:
        pinbar = 1
        mt4_signal = mt4_data.get("signal")
        mt4_cas    = mt4_data.get("cas", "")
        mt4_purple = mt4_data.get("purple", "")
    else:
        pinbar = 0
        mt4_signal = "Žádný signál"
        mt4_cas    = ""
        mt4_purple = ""

    # COT automaticky z CFTC
    cot_symbol = COT_SYMBOLY.get(symbol, "CRUDE OIL")
    cot = get_cot_signal(cot_symbol)

    # Ekonomický kalendář automaticky z ForexFactory
    kalendar = get_kalendar_signal()

    # Výpočet skóre
    skore  = pinbar                          * 30
    skore += (1 if trend == 1 else 0)        * 25
    skore += (1 if cot == 1 else 0)          * 20
    skore += (1 if sezonnost == 1 else 0)    * 15
    skore += (1 if kalendar == 1 else 0)     * 10

    # Popisky
    cot_popis = "Bullish" if cot == 1 else ("Bearish" if cot == -1 else "Neutrální")
    kal_popis = "Žádné riziko" if kalendar == 1 else ("Menší zprávy" if kalendar == 0 else "Vysoké riziko!")

    # Hodnocení
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
                           cot_popis=cot_popis,
                           kal_popis=kal_popis,
                           mt4_signal=mt4_signal,
                           mt4_cas=mt4_cas,
                           mt4_purple=mt4_purple)

if __name__ == "__main__":
    app.run(debug=True)
    