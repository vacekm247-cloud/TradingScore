<<<<<<< HEAD
import requests
from datetime import datetime

def get_kalendar_signal():
    dnes = datetime.now().strftime("%Y-%m-%d")
    print(f"Stahuji kalendář pro: {dnes}")
    try:
        url = "https://nfs.faireconomy.media/ff_calendar_thisweek.json"
        headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64)",
            "Accept": "application/json"
        }
        response = requests.get(url, headers=headers, timeout=10)
        print(f"Status: {response.status_code}")
        if response.status_code != 200:
            print("Forex Factory nedostupná, používám zálohu.")
            return get_manual_signal(dnes)
        data = response.json()

        vysoke  = 0
        stredni = 0
        for zprava in data:
            datum_raw = zprava.get("date", "")
            datum = datum_raw[:10]
            if datum != dnes:
                continue
            mena = zprava.get("currency", "")
            if mena != "USD":
                continue
            impact = zprava.get("impact", "")
            nazev  = zprava.get("title", "")
            print(f"  → [{impact}] {nazev}")
            if impact == "High":
                vysoke += 1
            elif impact == "Medium":
                stredni += 1

        print(f"\nVysoký dopad (USD): {vysoke}")
        print(f"Střední dopad (USD): {stredni}")

        # Pokud FF nenašel nic, zkontroluj ještě zálohu
        if vysoke == 0 and stredni == 0:
            manual = get_manual_signal(dnes)
            if manual != 1:
                print("Záloha detekovala riziko → přebíjí FF výsledek!")
                return manual

        if vysoke > 0:
            print("Signál: VYSOKÉ RIZIKO")
            return -1
        elif stredni > 0:
            print("Signál: MENŠÍ ZPRÁVY")
            return 0
        else:
            print("Signál: ŽÁDNÉ RIZIKO")
            return 1
    except Exception as e:
        print(f"Chyba při stahování kalendáře: {e}")
        return get_manual_signal(dnes)

VYSOKE_RIZIKO = {
    "2026-04-29": "FED zasedání",
    "2026-05-02": "NFP",
    "2026-05-08": "ECB zasedání",
    "2026-06-06": "NFP",
}

STREDNI_RIZIKO = {
    "2026-04-30": "GDP data USA",
    "2026-05-05": "ISM Services",
}

def get_manual_signal(dnes: str) -> int:
    if dnes in VYSOKE_RIZIKO:
        print(f"VYSOKÉ RIZIKO (záloha): {VYSOKE_RIZIKO[dnes]}")
        return -1
    elif dnes in STREDNI_RIZIKO:
        print(f"STŘEDNÍ RIZIKO (záloha): {STREDNI_RIZIKO[dnes]}")
        return 0
    else:
        print("Žádné rizikové zprávy (záloha)")
        return 1

if __name__ == "__main__":
    signal = get_kalendar_signal()
    print("\nVýsledný kalendář signál:", signal)
=======
import requests
from datetime import datetime

def get_kalendar_signal():
    dnes = datetime.now().strftime("%Y-%m-%d")
    print(f"Stahuji kalendář pro: {dnes}")
    try:
        url = "https://nfs.faireconomy.media/ff_calendar_thisweek.json"
        headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64)",
            "Accept": "application/json"
        }
        response = requests.get(url, headers=headers, timeout=10)
        print(f"Status: {response.status_code}")
        if response.status_code != 200:
            print("Forex Factory nedostupná, používám zálohu.")
            return get_manual_signal(dnes)
        data = response.json()

        vysoke  = 0
        stredni = 0
        for zprava in data:
            datum_raw = zprava.get("date", "")
            datum = datum_raw[:10]
            if datum != dnes:
                continue
            mena = zprava.get("currency", "")
            if mena != "USD":
                continue
            impact = zprava.get("impact", "")
            nazev  = zprava.get("title", "")
            print(f"  → [{impact}] {nazev}")
            if impact == "High":
                vysoke += 1
            elif impact == "Medium":
                stredni += 1

        print(f"\nVysoký dopad (USD): {vysoke}")
        print(f"Střední dopad (USD): {stredni}")

        # Pokud FF nenašel nic, zkontroluj ještě zálohu
        if vysoke == 0 and stredni == 0:
            manual = get_manual_signal(dnes)
            if manual != 1:
                print("Záloha detekovala riziko → přebíjí FF výsledek!")
                return manual

        if vysoke > 0:
            print("Signál: VYSOKÉ RIZIKO")
            return -1
        elif stredni > 0:
            print("Signál: MENŠÍ ZPRÁVY")
            return 0
        else:
            print("Signál: ŽÁDNÉ RIZIKO")
            return 1
    except Exception as e:
        print(f"Chyba při stahování kalendáře: {e}")
        return get_manual_signal(dnes)

VYSOKE_RIZIKO = {
    "2026-04-29": "FED zasedání",
    "2026-05-02": "NFP",
    "2026-05-08": "ECB zasedání",
    "2026-06-06": "NFP",
}

STREDNI_RIZIKO = {
    "2026-04-30": "GDP data USA",
    "2026-05-05": "ISM Services",
}

def get_manual_signal(dnes: str) -> int:
    if dnes in VYSOKE_RIZIKO:
        print(f"VYSOKÉ RIZIKO (záloha): {VYSOKE_RIZIKO[dnes]}")
        return -1
    elif dnes in STREDNI_RIZIKO:
        print(f"STŘEDNÍ RIZIKO (záloha): {STREDNI_RIZIKO[dnes]}")
        return 0
    else:
        print("Žádné rizikové zprávy (záloha)")
        return 1

if __name__ == "__main__":
    signal = get_kalendar_signal()
    print("\nVýsledný kalendář signál:", signal)
>>>>>>> 7a07018ef4187cae59f2152bb3fa0170dd88c6f8
    