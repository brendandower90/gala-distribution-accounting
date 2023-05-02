import requests
from bs4 import BeautifulSoup
import datetime

def get_gala_distribution_on_date(address, date):
    dt = datetime.datetime(date.year, date.month, date.day, 23, 59, 59, 999000)
    epoch_ms = int(dt.timestamp() * 1000)
    url = f"https://app.gala.games/distribution?date={epoch_ms}&tokenType=gala"
    response = requests.get(url)

    if response.status_code == 200:
        soup = BeautifulSoup(response.text, "html.parser")
        container_div = soup.find("div", class_="v-card v-card--flat v-sheet theme--dark accent")

        if container_div:
            rows = container_div.find_all("div", class_="results-grid-list px-2 pa-2 small-font bold-1 white--text")

            for row in rows:
                address_div = row.find("div", class_="address pl-2 small-font")
                amount_div = row.find("span")

                if address_div and amount_div and address_div.text.strip() == address:
                    amount = float(amount_div.text.strip())
                    return amount

            print(f"No distribution found for {address} on {date}")
            return 0

        else:
            print(f"Error: Container div not found")
            return None

    else:
        print(f"Error fetching distribution for {date}. Status code: {response.status_code}")
        return None


def main():
    start_date = datetime.date(2021, 7, 1)
    end_date = datetime.date(2022, 6, 30)
    address = "0x9f3B3BBdC3A7D58054600b8e105a781fFd6FBfdD"
    current_date = start_date

    while current_date <= end_date:
        gala_distribution = get_gala_distribution_on_date(address, current_date)
        print(f"GALA Distribution on {current_date}: {gala_distribution}")
        current_date += datetime.timedelta(days=1)

if __name__ == "__main__":
    main()
