# -*- coding: utf-8 -*-
import click
import logging
from pathlib import Path
from dotenv import find_dotenv, load_dotenv


@click.command()
@click.argument('input_filepath', type=click.Path(exists=True))
@click.argument('output_filepath', type=click.Path())
def main(input_filepath, output_filepath):
    """ Runs data processing scripts to turn raw data from (../raw) into
        cleaned data ready to be analyzed (saved in ../processed).
    """
    logger = logging.getLogger(__name__)
    logger.info('making final data set from raw data')


if __name__ == '__main__':
    log_fmt = '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
    logging.basicConfig(level=logging.INFO, format=log_fmt)

    # not used in this stub but often useful for finding various files
    project_dir = Path(__file__).resolve().parents[2]

    # find .env automagically by walking up directories until it's found, then
    # load up the .env entries as environment variables
    load_dotenv(find_dotenv())

    main()
    
import yfinance as yf
from pathlib import Path
import requests
import os

# Load the environment variables from .env file
load_dotenv()

# Fetch the API key
CPI_API_KEY = os.getenv("CPI_API_KEY")

BASE_DATA_DIR = Path("../../data")  # directory where project data is located
RAW_DATA_DIR = BASE_DATA_DIR / "raw"

def fetch_equity_data(ticker, start_date, end_date):
    """
    Fetch data from Yahoo Finance and save it in the raw data directory.
    
    Args:
    - ticker (str): The stock/asset ticker symbol.
    - start_date (str): Start date in format 'YYYY-MM-DD'.
    - end_date (str): End date in format 'YYYY-MM-DD'.
    
    Returns:
    - pandas.DataFrame: The fetched data.
    """
    yf_data = yf.download(ticker, start=start_date, end=end_date)
    yf_data.to_csv(RAW_DATA_DIR / f"{ticker}_{start_date}_to_{end_date}.csv")
    return yf_data

def fetch_CPI_data(start_year, end_year):
    """
    Fetch CPI-U data from the BLS API for a specific date range (set time period up to 20 years).

    Args:
    - start_year (int): Start year for the data.
    - end_year (int): End year for the data.

    Returns:
    - list: List of dictionaries containing year and inflation data.
    """
    url = "	https://api.bls.gov/publicAPI/v2/timeseries/data/"
    series_id = "CUUR0000SA0"  # This is the series ID for CPI-U, All items, U.S. city average
    
    headers = {
        "Content-type": "application/json",
    }
    data = {
        "seriesid": [series_id],
        "startyear": str(start_year),
        "endyear": str(end_year),
        "registrationkey": CPI_API_KEY
    }
    
    response = requests.post(url, headers=headers, json=data)
    CPI_data = response.json()

# Example usage:
# api_key = "YOUR_BLS_API_KEY"
# inflation_data = fetch_CPI_data(api_key, 2020, 2022)
# print(inflation_data)
