import requests
import os
import time
from datetime import datetime

figi_list = "figi.txt"
token = "t.RGHTeiIzzQ1jS026aH06FFRUQ7RNpv2reed0m5azzlY0hjpWID-fxS1C1t1BNDBVRxZizgvR3GP9K4UirjVJrA"
minimum_year = 2013
current_year = datetime.now().year
url = "https://invest-public-api.tinkoff.ru/history-data"

def download(figi, year):
    # Download all archives from the current year to 2013
    if year < minimum_year:
        return

    file_name = os.path.join("D:/Programing/Stocks_app/model/download_data/zip_file", f"{figi}_{year}.zip")
    print(f"Downloading {figi} for year {year}")
    headers = {"Authorization": f"Bearer {token}"}
    response = requests.get(f"{url}?figi={figi}&year={year}", headers=headers)

    # Save the response content to a file
    with open(file_name, "wb") as file:
        file.write(response.content)

    # Get the HTTP response code
    response_code = response.status_code
    print(f"HTTP response code: {response_code}")

    # If the request limit per minute (30) is exceeded, retry the request
    if response.status_code == 429:
        print("Rate limit exceeded. Sleeping for 5 seconds.")
        time.sleep(5)
        download(figi, year)
        return

    # If the token is invalid, exit
    if response.status_code == 401 or response.status_code == 500:
        print("Invalid token")
        exit(1)

    # If data for the instrument and year is not found
    if response.status_code == 404:
        print(f"Data not found for figi={figi}, year={year}. Removing empty file.")
        try:
            # Remove the empty archive
            os.remove(file_name)
        except FileNotFoundError:
            pass
    elif response.status_code != 200:
        # In case of any other error, print the error code and exit
        print(f"Unspecified error with code: {response.status_code}")
        exit(1)

    year -= 1
    download(figi, year)

with open(figi_list, "r") as file:
    for figi in file:
        figi = figi.strip()
        download(figi, current_year)