# -*- coding: utf-8 -*-
import os
from datetime import datetime
from pathlib import Path

import pandas as pd

def open_directory(POST_DATA_DIR):
    # lists to store file paths
    inflation_file = None
    asset_files = []

    # loop through the directory and classify files
    for filename in os.listdir(POST_DATA_DIR):
        if filename.endswith(".csv"):
            # check if the file is the inflation data file
            if "CPI-U" in filename:
                inflation_file = os.path.join(POST_DATA_DIR, filename)
            else:
                asset_files.append(os.path.join(POST_DATA_DIR, filename))

    return inflation_file, asset_files

def merge_data(POST_DATA_DIR, MODEL_DIR):
    inflation_file, asset_files = open_directory(POST_DATA_DIR)

    # load the inflation data and convert dates to month-year format
    inflation_data = pd.read_csv(inflation_file)
    inflation_data['Date'] = pd.to_datetime(inflation_data['year'].astype(str) + '-' + 
                                            inflation_data['periodName'].apply(lambda x: datetime.strptime(x, '%B').strftime('%m')))
    inflation_data['Date'] = inflation_data['Date'].dt.to_period('M')

    # dictionary to hold merged data for each asset
    merged_data = {}

    # process each asset file
    for asset_file in asset_files:
        # extract asset name from the file name
        asset_name = os.path.basename(asset_file).split('_')[0]

        # load the asset data
        asset_data = pd.read_csv(asset_file)
        asset_data['Date'] = pd.to_datetime(asset_data['Date']).dt.to_period('M')

        # merge with inflation data
        merged_asset_data = pd.merge(asset_data, inflation_data[['Date', 'Inflation Rates']], on='Date', how='inner')
        
        # store in the dictionary
        merged_data[asset_name] = merged_asset_data

        # Save each merged DataFrame to a CSV file
        output_file_path = os.path.join(MODEL_DIR, f'{asset_name}_merged_data.csv')
        merged_asset_data.to_csv(output_file_path, index=False)

def main():
    merge_data(POST_DATA_DIR, MODEL_DIR)
    print("Data has been successfully merged.")

if __name__ == '__main__':
    PROJECT_DIR = Path(__file__).resolve().parents[2]
    MODEL_DIR = PROJECT_DIR / "models"
    POST_DATA_DIR = PROJECT_DIR / "data" / "processed"
    main()