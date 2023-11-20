# -*- coding: utf-8 -*-
import json
import os
from pathlib import Path

import pandas as pd
import requests
import yfinance as yf
import nasdaqdatalink as ndl
from dotenv import find_dotenv, load_dotenv

def fetch_gold_data(start_date, end_date, ASSET_DATA_DIR):
    """
    Fetches the end-of-month afternoon gold prices from the London Bullion Market 
    via the Nasdaq Data Link's Time-Series API and appends them to a CSV file.
    
    args:
    - time_series_codes (list): list of time series codes (str) of commodities.
    - start_date (str): start date in format 'YYYY-MM-DD'.
    - end_date (str): end date in format 'YYYY-MM-DD'.
    - ASSET_DATA_DIR (str): directory path where the CSV file will be saved.
    
    returns:
    - CSV: gold price data returned by nasdaqdatalink in file.csv.
    - str: message indicating fetch success or failure of request.
    - boolean: True if price data was downloaded.

    raises:
    - nasdaqdatalink.HTTPError: if there is an issue with the request.
    """
    # load the environment variables from .env file
    load_dotenv(find_dotenv())
    ndl.ApiConfig.api_key = os.getenv("NASDAQ_DATA_LINK_API_KEY")

    try:
        gold_data = ndl.get("LBMA/GOLD", start_date=start_date, end_date=end_date)

        file_path = Path(ASSET_DATA_DIR) / f"gold_{start_date}_to_{end_date}.csv"
        gold_data.to_csv(file_path)

        print(f"Gold prices were downloaded successfully to {file_path}\n")

        return True
    
    except Exception as e:
        print(f"An error occurred: {e}\n")

        return False

def fetch_equity_data(tickers, start_date, end_date, ASSET_DATA_DIR):
    """
    Fetch data from Yahoo Finance and save it in the asset folder within the raw data directory.
    
    args:
    - ticker (list): list of ticker symbols (str) of equities.
    - start_date (str): start date in format 'YYYY-MM-DD'.
    - end_date (str): end date in format 'YYYY-MM-DD'.
    - ASSET_DATA_DIR (str): directory path where the CSV file will be saved.
    
    returns:
    - CSV: stock price data returned by yfinance in file.csv.
    - str: message indicating fetch success and invalid ticker input(s).
    - boolean: True if price data for all equities were downloaded.

    raises:
    - ValueError: if the provided dates are in an incorrect format or illogical (e.g., start_date later than end_date).
    - yfinance.HTTPError: if there is an issue with the network connection or the Yahoo Finance server.
    """
    invalid_tickers = []

    for ticker in tickers:
        try:
            data = yf.download(ticker, start=start_date, end=end_date)

            if data.empty:
                invalid_tickers.append(ticker)
                continue

            file_path = ASSET_DATA_DIR / f"{ticker}_{start_date}_to_{end_date}.csv"
            data.to_csv(file_path)
            
            print(f"Prices for {ticker} saved to {file_path}")

        except Exception as e:
            print(f"An error occurred: {e}")
           
    print()

    if invalid_tickers:
        print(f"Please check invalid ticker input(s): {invalid_tickers}\n")

        return False
    else:
        print(f"Prices for all equities downloaded successfully to {ASSET_DATA_DIR}\n")

        return True

def fetch_CPI_data(start_date, end_date, CPI_DATA_DIR):
    """
    Fetch CPI-U data from the BLS API for a specific date range (set time period up to 20 years) 
    and save it in the CPI folder within the raw data directory.

    args:
    - start_year (int): start year for the data.
    - end_year (int): end year for the data.
    - CPI_DATA_DIR (str): directory path where the CSV file will be saved.


    returns:
    - CSV: CPI-U data returned by the API in file.csv.
    - bool: True if CPI-U data were downloaded.
    - str: message indicating fetch success and if most recent CPI data was accessed.

    raises:
    - requests.exceptions.RequestException: if an error occurs while making the API request.
    """
    # load the environment variables from .env file
    load_dotenv(find_dotenv())
    CPI_API_KEY = os.getenv("CPI_API_KEY")

    start_year = int(str(start_date[:4]))
    end_year = int(str(end_date[:4]))

    file_path = CPI_DATA_DIR / f"CPI-U_{start_year}_to_{end_year}.csv"
    series_id = "CUUR0000SA0"  # series ID for CPI-U, All items, U.S. city average
    url = f"https://api.bls.gov/publicAPI/v2/timeseries/data/"
  
    headers = {
        "Content-type": "application/json",
    }
    data = json.dumps({
        "seriesid": [series_id],
        "startyear": str(start_year),
        "endyear": str(end_year),
        "registrationkey": CPI_API_KEY
    })

    response = requests.post(url, data=data, headers=headers)

    if response.status_code == 200:
        response_data = json.loads(response.text)
        df = pd.DataFrame(response_data['Results']['series'][0]['data'])
        df.to_csv(file_path, index=False)

        try:
            df['latest']
            print(f"Your dataset contains the latest CPI-U data available:\n{df.head(1)}\n")
        except Exception:
            pass

        print(f"CPI-U data downloaded successfully to {file_path}\n")

        return True
    else:
        print(f"Failed to retrieve CPI-U data: {response.status_code}\n")

        return False
