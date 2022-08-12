import os
from datetime import date
from time import perf_counter
import requests
from bs4 import BeautifulSoup
import gspread

import email_sender


def main():
    start = perf_counter()
    base_url_cost = "https://www.numbeo.com/cost-of-living/in/"
    gradovi = ["Split", "Zagreb", "Zadar", "Dubrovnik", "Rijeka", "Osijek", "Solin-Croatia", "Makarska-Croatia",
                "Trogir-Croatia", "Sibenik-Croatia", "Kaštela-Croatia", "Omis-Croatia"]
    currency = "EUR"

    gcreds_filename = 'creds-google.json'

    if "GOOGLE_CREDS" in os.environ:
        gcreds_filename = os.environ["GOOGLE_CREDS"]

    gc = gspread.service_account(filename=gcreds_filename)

    for count, grad in enumerate(gradovi):

        sh = gc.open('cost_of_living')
        worksheet = sh.worksheet(grad)
        response = requests.get(base_url_cost + grad + f"?displayCurrency={currency}")
        soup = BeautifulSoup(response.text, 'html.parser')
        vrijednosti = soup.find_all("td", class_="priceValue")
        cost_of_living = {}

        for vrijednost in vrijednosti:
            cost_of_living[vrijednost.findParent('tr').findNext('td').get_text()] = vrijednost.get_text().split()[0]

        worksheet.append_row([f"{date.today()}"]+list(cost_of_living.values()))

    print(f"Vrijeme izvršavanja: {perf_counter() - start} sekundi.")


if __name__ == "__main__":
    try:
        main()
    except Exception as e:
        email_sender.send_email(f'Living gspread {date.today()}', 'senfsend@outlook.com', 'mate.mrse@gmail.com', f"{e}")
