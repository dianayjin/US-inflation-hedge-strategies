# -*- coding: utf-8 -*-
import os
from pathlib import Path

import pandas as pd
from pandas.tseries.offsets import BMonthEnd
import numpy as np

def get_monthly_prices(ASSET_DATA_DIR, INT_DATA_DIR):
    """
    Processes all CSV files in the given directory to pull end of month prices.

    args:
    - ASSET_DATA_DIR (str): path to the input directory.
    - INT_DATA_DIR (str): path to the output directory.

    returns:
    - pd.DataFrame: dataframe containing monthly prices.
    - str: message indicating processing success and invalid file input(s).
    """
    invalid_files = []
    
    for filename in os.listdir(ASSET_DATA_DIR):
        if filename.endswith('.csv'):
            file_path = Path(ASSET_DATA_DIR) / filename
            data = pd.read_csv(file_path, parse_dates=['Date'], index_col='Date')
            # find the last business day of each month in the data's date range
            last_day = pd.date_range(start=data.index.min(), end=data.index.max(), freq='BM')
            

            # filter data to only include these dates
            eom_prices = data[data.index.isin(last_day)]
            try:
                monthly_data = eom_prices['Adj Close']

            except:
                # replace missing 'USD (PM)' values with 'USD (AM)' values
                eom_prices['USD (PM)'] = eom_prices['USD (PM)'].fillna(eom_prices['USD (AM)'])
                monthly_data = eom_prices['USD (PM)']

            output_file = file_path.stem + '_monthly_prices.csv'
            monthly_data.to_csv(Path(INT_DATA_DIR) / output_file)

            print(f'Monthly prices saved to {output_file}')

        else:
            invalid_files.append(filename)
            print(f"Unsupported file format: {filename}")        
        print()

    if invalid_files:    
        print(f"Please check the following invalid file(s): {invalid_files}\n")

    else:
        print("Monthly prices were pulled successfully\n")

def calculate_inflation_rates(CPI_DATA_DIR, POST_DATA_DIR):
    """
    Processes all CSV files in the given directory to calculate inflation rates.

    args:
    - CPI_DATA_DIR (str): path to the input directory.
    - POST_DATA_DIR (str): path to the output directory.

    returns:
    - pd.DataFrame: dataframe containing the inflation rates.
    - str: message indicating processing success and invalid file input(s).
    """
    invalid_files = []
    
    for filename in os.listdir(CPI_DATA_DIR):
        if filename.endswith('.csv'):
            file_path = Path(CPI_DATA_DIR) / filename
            data = pd.read_csv(file_path)
            # preprocess data to list values in ascending chronological order
            data = data.iloc[::-1]

            data['value'] = 100 * np.log(data['value'] / data['value'].shift(1))

            output_file = file_path.stem + '_inflation_rates.csv'
            data.to_csv(Path(POST_DATA_DIR) / output_file)

            print(f'Inflation rates saved to {output_file}')

        else:
            invalid_files.append(filename)
            print(f"Unsupported file format: {filename}")        
    print()
    if invalid_files:    
        print(f"Please check the following invalid file(s): {invalid_files}\n")

    else:
        print("Inflation rates were calculated successfully\n")

def calculate_log_returns(file_path):
    """
    Calculates the log returns of asset prices in a given CSV file.

    args:
    - file_path (Path): path to the CSV file.

    returns:
    - pd.DataFrame: dataframe containing the log returns.
    """
    # load data
    data = pd.read_csv(file_path, parse_dates=['Date'], index_col='Date')

    # calculate log returns
    try:
        log_returns = 100 * np.log(data['Adj Close'] / data['Adj Close'].shift(1))

    except:
        log_returns = 100 * np.log(data['USD (PM)'] / data['USD (PM)'].shift(1))

    return log_returns.dropna()

def process_asset_files(INT_DATA_DIR, POST_DATA_DIR):
    """
    Processes all CSV files in the given directory to calculate log returns.

    args:
    - ASSET_DATA_DIR (str): path to the directory containing CSV files.
    - POST_DATA_DIR (str): path to the output directory.

    returns:
    - str: message indicating processing success and invalid file input(s).
    """
    invalid_files = []

    for filename in os.listdir(INT_DATA_DIR):
        
        if filename.endswith('.csv'):
            file_path = Path(INT_DATA_DIR) / filename
            log_returns = calculate_log_returns(file_path)

            # save the log returns to a new CSV file
            output_file = file_path.stem + '_log_returns.csv'
            log_returns.to_csv(Path(POST_DATA_DIR) / output_file)
            print(f"Log returns saved to {output_file}")

        else:
            invalid_files.append(filename)
            print(f"Unsupported file format: {filename}")
    print()
    if invalid_files:    
        print(f"Please check the following invalid file(s): {invalid_files}\n")

    else:
        print("Returns for all assets were calculated successfully\n")