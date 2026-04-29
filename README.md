# 📊 TradingScore

Flask aplikace pro automatické hodnocení obchodních setupů na finančních trzích.

## Co aplikace dělá

Zadáš symbol (NASDAQ, GOLD, CORN...) a aplikace automaticky vyhodnotí kvalitu obchodního signálu na základě 5 faktorů:

| Faktor | Váha | Zdroj |
|--------|------|-------|
| Pin Bar signál | 30% | MT4 (Purple Trading) |
| Trend D1 | 25% | Yahoo Finance |
| COT report | 20% | CFTC (US regulátor) |
| Sezónnost | 15% | Historické vzory |
| Ekonomický kalendář | 10% | Forex Factory |

## Technologie

- Python 3
- Flask
- Jinja2 templating
- Bootstrap 5
- Yahoo Finance API (yfinance)
- CFTC COT data

## Spuštění

```bash
pip install flask requests yfinance
python app.py
```

Aplikace se otevře na http://127.0.0.1:5000

## Autor

Martin Vacek — junior Python/Flask developer
