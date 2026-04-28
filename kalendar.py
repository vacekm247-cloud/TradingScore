import requests
from bs4 import BeautifulSoup
from datetime import datetime

def get_kalendar_signal():
    """
    Zkontroluje ekonomický kalendář na ForexFactory.
    Vrací: 1 = žádné riziko, 0 = menší zprávy, -1 = vysoké riziko
    """
    try:
        dnes = datetime.now().strftime("%b%d.%Y").lower()
        url = f"https://www.forexfactory.com/calendar?day={dnes}"

        headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36"
        }

        print(f"Stahuji kalendář pro: {dnes}")
        response = requests.get(url, headers=headers, timeout=10)

        soup = BeautifulSoup(response.text, "html.parser")

        # Hledáme události s vysokým dopadem (červené)
        high_impact = soup.find_all("td", class_="calendar__impact")

        vysoke_riziko = 0
        stredni_riziko = 0

        for impact in high_impact:
            ikona = impact.find("span")
            if ikona:
                trida = ikona.get("class", [])
                trida_str = " ".join(trida)
                if "high" in trida_str:
                    vysoke_riziko += 1
                elif "medium" in trida_str:
                    stredni_riziko += 1

        print(f"Vysoký dopad: {vysoke_riziko} zpráv")
        print(f"Střední dopad: {stredni_riziko} zpráv")

        if vysoke_riziko > 0:
            print("Signal: VYSOKÉ RIZIKO")
            return -1
        elif stredni_riziko > 0:
            print("Signal: MENŠÍ ZPRÁVY")
            return 0
        else:
            print("Signal: ŽÁDNÉ RIZIKO")
            return 1

    except Exception as e:
        print(f"Chyba při načítání kalendáře: {e}")
        return 0


if __name__ == "__main__":
    signal = get_kalendar_signal()
    print("\nVýsledný kalendář signál:", signal)
    