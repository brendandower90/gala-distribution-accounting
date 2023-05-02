import requests
import datetime
import csv
import time

def get_gala_price_aud_on_date(date):
    dt = datetime.datetime(date.year, date.month, date.day)
    url = f"https://api.coingecko.com/api/v3/coins/gala/history?date={date.strftime('%d-%m-%Y')}&localization=false"
    response = requests.get(url)

    if response.status_code == 200:
        data = response.json()
        try:
            aud_price = round(data['market_data']['current_price']['aud'],5)
            print(f"Date: {date}, Price: ${aud_price}")
            return aud_price
        except KeyError:
            print(f"Error fetching price for {date}: Data not found")
            return None
    else:
        print(f"Error fetching price for {date}. Status code: {response.status_code}")
        return None


def get_gala_price_aud_range(start_date, end_date):
    date_prices = []
    current_date = start_date

    while current_date <= end_date:
        aud_price = get_gala_price_aud_on_date(current_date)
        if aud_price is not None:
            date_prices.append((current_date, aud_price))
        current_date += datetime.timedelta(days=1)
        time.sleep(6)  # Add a delay of 6 seconds between API calls to avoid rate limiting on the free tier

    return date_prices


def main():
    start_date = datetime.date(2021, 7, 1)
    end_date = datetime.date(2022, 7, 30)
    
    gala_prices = get_gala_price_aud_range(start_date, end_date)
    
    with open('gala_prices_aud.csv', mode='w', newline='') as csvfile:
        fieldnames = ['Date', 'Price (AUD)']
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        
        writer.writeheader()
        for date, price in gala_prices:
            writer.writerow({'Date': date, 'Price (AUD)': price})

    print("GALA prices fetched and saved to gala_prices_aud.csv")

if __name__ == "__main__":
    main()
