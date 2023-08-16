from datetime import date
from time import perf_counter
import requests
from bs4 import BeautifulSoup
import gspread


def main():
    start = perf_counter()
    base_url_cost = "https://www.numbeo.com/cost-of-living/in/"
    gradovi = ["Split", "Zagreb", "Zadar", "Dubrovnik", "Rijeka", "Osijek", "Solin-Croatia", "Makarska-Croatia",
                "Trogir-Croatia", "Sibenik-Croatia", "Kaštela-Croatia", "Omis-Croatia"]
    currency = "EUR"

    gcreds_filename = 'creds-google.json'

    gc = gspread.service_account(filename=gcreds_filename)

    for count, grad in enumerate(gradovi):

        sh = gc.open('cost_of_living')
        worksheet = sh.worksheet(grad)
        response = requests.get(base_url_cost + grad + f"?displayCurrency={currency}")
        soup = BeautifulSoup(response.text, 'html.parser')
        vrijednosti = soup.find_all("td", {"class": "priceValue"})
        cost_of_living = {}

        for vrijednost in vrijednosti:
            cost_of_living[vrijednost.findParent('tr').findNext('td').get_text()] = vrijednost.get_text().split()[0]

        worksheet.append_row([f"{date.today()}"]+list(cost_of_living.values()))

    print(f"[Cost of life] performance: {perf_counter() - start} s. {date.today()}")


def send_to_telegram(content):

    api_token = creds.TELEGRAM_API_TOKEN_TECH
    chat_id = creds.TELEGRAM_CHAT_ID

    api_url = f"https://api.telegram.org/bot{api_token}/sendMessage"

    try:
        response = requests.post(api_url, json={'chat_id': chat_id, 'text': content})
        print(response.text)
    except Exception as ex:
        print(ex)


if __name__ == "__main__":
    try:
        main()
    except Exception as e:
        print(e)
        send_to_telegram(f"Greska na Cost of life scraperu:\n\n{e}")

