<<<<<<< HEAD
from flask import Flask, render_template, request
from cot import get_cot_signal
from kalendar import get_kalendar_signal
from mt4 import get_mt4_signal
from trend import get_trend_signal
from sezonnost import get_sezonnost_signal
from telegram_bot import posli_zpravu
from datetime import datetime

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
        mt4_signal = mt4_data.get("signal")
        mt4_cas    = mt4_data.get("cas", "")
        mt4_purple = mt4_data.get("purple", "")

        # Kontrola stáří signálu
        try:
            cas_dt    = datetime.strptime(mt4_cas, "%Y.%m.%d %H:%M")
            stari_dni = (datetime.now() - cas_dt).days
            if stari_dni > 2:
                pinbar     = 0
                mt4_signal = f"Starý signál ({stari_dni} dní) — ignoruji"
            else:
                pinbar = 1
        except Exception:
            pinbar = 1
    else:
        pinbar     = 0
        mt4_signal = "Žádný signál"
        mt4_cas    = ""
        mt4_purple = ""

    trend      = get_trend_signal(symbol)
    cot_symbol = COT_SYMBOLY.get(symbol, "CRUDE OIL")
    cot        = get_cot_signal(cot_symbol)
    kalendar   = get_kalendar_signal()
    sezonnost  = get_sezonnost_signal(symbol)

    # Konflikt — pin bar jde proti trendu
    konflikt = ""
    if pinbar == 1 and mt4_signal == "BULLISH" and trend == -1:
        konflikt = "⚠️ POZOR: Pin Bar je BULLISH ale trend je Bearish — signál jde proti trendu!"
    elif pinbar == 1 and mt4_signal == "BEARISH" and trend == 1:
        konflikt = "⚠️ POZOR: Pin Bar je BEARISH ale trend je Bullish — signál jde proti trendu!"

    # Skóre — Pin Bar přidá body jen když jde ve směru trendu
    if pinbar == 1 and mt4_signal == "BULLISH" and trend >= 0:
        skore = 30
    elif pinbar == 1 and mt4_signal == "BEARISH" and trend <= 0:
        skore = 30
    else:
        skore = 0

    skore += (1 if trend == 1 else 0)     * 25
    skore += (1 if cot == 1 else 0)       * 20
    skore += (1 if sezonnost == 1 else 0) * 15
    skore += (1 if kalendar == 1 else 0)  * 10

    trend_popis = "Bullish" if trend == 1 else ("Bearish" if trend == -1 else "Neurčitý")
    cot_popis   = "Bullish" if cot == 1 else ("Bearish" if cot == -1 else "Neutrální")
    sezon_popis = "Bullish" if sezonnost == 1 else ("Bearish" if sezonnost == -1 else "Neutrální")
    kal_popis   = "Žádné riziko" if kalendar == 1 else ("Menší zprávy" if kalendar == 0 else "Vysoké riziko!")

    # Purple Level
    try:
        purple_val = float(mt4_purple) if mt4_purple else 0.0
        na_levelu  = purple_val > 0.0
    except Exception:
        na_levelu = False

    # Doporučení
    if kalendar == -1:
        doporuceni       = "🚫 Nevstupovat — vysoké riziko zpráv!"
        doporuceni_barva = "danger"
    elif konflikt:
        doporuceni       = "🚫 Nevstupovat — konflikt signálů!"
        doporuceni_barva = "danger"
    elif skore >= 80 and pinbar == 1 and mt4_signal == "BULLISH" and trend == 1:
        if na_levelu:
            doporuceni = "🟢 Doporučuji LONG — Pin Bar NA Purple Levelu! Silný setup!"
        else:
            doporuceni = "🟢 Doporučuji LONG"
        doporuceni_barva = "success"
    elif skore >= 80 and pinbar == 1 and mt4_signal == "BEARISH" and trend == -1:
        if na_levelu:
            doporuceni = "🔴 Doporučuji SHORT — Pin Bar NA Purple Levelu! Silný setup!"
        else:
            doporuceni = "🔴 Doporučuji SHORT"
        doporuceni_barva = "danger"
    elif skore >= 50:
        doporuceni       = "⚠️ Signál slabší — vyčkat na lepší setup"
        doporuceni_barva = "warning"
    else:
        doporuceni       = "🚫 Nevstupovat — slabý signál"
        doporuceni_barva = "danger"

    # Telegram notifikace — jen při silném signálu bez konfliktu
    if skore >= 80 and pinbar == 1 and not konflikt and kalendar != -1:
        smer = "LONG 🟢" if mt4_signal == "BULLISH" else "SHORT 🔴"
        purple_text = f"\n🎯 Pin Bar NA Purple Levelu: {mt4_purple}" if na_levelu else ""
        zprava = (
            f"📊 <b>TradingScore Alert!</b>\n"
            f"Symbol: <b>{symbol}</b>\n"
            f"Směr: <b>{smer}</b>\n"
            f"Skóre: <b>{skore}/100</b>\n"
            f"Trend: {trend_popis}\n"
            f"COT: {cot_popis}\n"
            f"Sezónnost: {sezon_popis}\n"
            f"Kalendář: {kal_popis}"
            f"{purple_text}"
        )
        posli_zpravu(zprava)

    if skore >= 80:
        hodnoceni = "Silný signál - vstup zvážit"
        barva     = "success"
    elif skore >= 50:
        hodnoceni = "Středně silný signál - opatrně"
        barva     = "warning"
    else:
        hodnoceni = "Slabý signál - raději nečekat"
        barva     = "danger"

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
                           konflikt=konflikt,
                           doporuceni=doporuceni,
                           doporuceni_barva=doporuceni_barva)

if __name__ == "__main__":
    import webbrowser
    webbrowser.open("http://127.0.0.1:5000")
    app.run(debug=True)
=======
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
>>>>>>> 7a07018ef4187cae59f2152bb3fa0170dd88c6f8
    