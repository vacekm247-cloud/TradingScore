import requests

TELEGRAM_TOKEN  = "7953128297:AAHCVV8U6tIzoWL_nkM5REq-GpgzNvlamRM"
TELEGRAM_CHAT_ID = "8684019398"

def posli_zpravu(text: str):
    """Pošle zprávu do Telegramu."""
    try:
        url = f"https://api.telegram.org/bot{TELEGRAM_TOKEN}/sendMessage"
        data = {
            "chat_id": TELEGRAM_CHAT_ID,
            "text": text,
            "parse_mode": "HTML"
        }
        response = requests.post(url, data=data, timeout=10)
        if response.status_code == 200:
            print("Telegram: zpráva odeslána ✅")
        else:
            print(f"Telegram chyba: {response.status_code}")
    except Exception as e:
        print(f"Telegram chyba: {e}")

if __name__ == "__main__":
    posli_zpravu("🤖 TradingScore bot funguje!")
    