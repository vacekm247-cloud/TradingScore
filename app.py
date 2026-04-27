from flask import Flask, render_template, request

app = Flask(__name__)

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/score", methods=["POST"])
def score():
    # Načtení hodnot z formuláře
    symbol    = request.form.get("symbol")
    pinbar    = int(request.form.get("pinbar"))
    trend     = int(request.form.get("trend"))
    cot       = int(request.form.get("cot"))
    sezonnost = int(request.form.get("sezonnost"))
    kalendar  = int(request.form.get("kalendar"))

    # Výpočet skóre (váhy v procentech)
    skore = 0
    skore += pinbar    * 30   # Pin Bar = 30 bodů
    skore += (1 if trend == 1 else 0)     * 25   # Trend = 25 bodů
    skore += (1 if cot == 1 else 0)       * 20   # COT = 20 bodů
    skore += (1 if sezonnost == 1 else 0) * 15   # Sezónnost = 15 bodů
    skore += (1 if kalendar == 1 else 0)  * 10   # Kalendář = 10 bodů

    # Hodnocení
    if skore >= 80:
        hodnoceni = "🟢 Silný signál - vstup zvážit"
        barva = "success"
    elif skore >= 50:
        hodnoceni = "🟡 Středně silný signál - opatrně"
        barva = "warning"
    else:
        hodnoceni = "🔴 Slabý signál - raději nečekat"
        barva = "danger"

    return render_template("score.html",
                           symbol=symbol,
                           skore=skore,
                           hodnoceni=hodnoceni,
                           barva=barva)

if __name__ == "__main__":
    app.run(debug=True)
    