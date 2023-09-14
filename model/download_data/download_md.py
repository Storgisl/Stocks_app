import requests
import os
import time
from datetime import datetime

figi_list = "figi.txt"
token = ""
minimum_year = 2017
current_year = datetime.now().year
url = "https://invest-public-api.tinkoff.ru/history-data"

def download(figi, year):
    # Download all archives from the current year to 2017
    if year < minimum_year:
        return

    file_name = os.path.join("D:/Programing/Stocks_app/model/download_data/zip_file", f"{figi}_{year}.zip")

    # Skip download if the file already exists
    if os.path.exists(file_name):
        print(f"Skipping {figi} for year {year}. File already exists.")
        year -= 1
        download(figi, year)
        return

    print(f"Downloading {figi} for year {year}")
    headers = {"Authorization": f"Bearer {token}"}
    response = requests.get(f"{url}?figi={figi}&year={year}", headers=headers)

    # Get the HTTP response code
    response_code = response.status_code
    print(f"HTTP response code: {response_code}")

    # If the request limit per minute (30) is exceeded, retry the request
    if response_code == 429:
        print("Rate limit exceeded. Sleeping for 5 seconds.")
        time.sleep(5)
        download(figi, year)
        return

    # If the token is invalid, skip the download
    if response_code == 500:
        print("Invalid token. Skipping download.")
        year -= 1
        download(figi, year)
        return

    # If data for the instrument and year is not found, remove the empty file
    if response_code == 404:
        print(f"Data not found for figi={figi}, year={year}. Removing empty file.")
        try:
            os.remove(file_name)
        except FileNotFoundError:
            pass
    elif response_code != 200:
        # In case of any other error, print the error code and exit
        print(f"Unspecified error with code: {response_code}")
        exit(1)

    year -= 1
    download(figi, year)

with open(figi_list, "r") as file:
    for figi in file:
        figi = figi.strip()
        download(figi, current_year)
