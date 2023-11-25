# -*- coding: utf-8 -*-
from pathlib import Path

import user_input as ui
import load_data as load
import process_data as process


def main():
    """ 
    Runs data loading and processing scripts to turn raw data from (../raw) into cleaned data ready to be analyzed (saved in ../processed).
    """
    PROJECT_DIR= Path(__file__).resolve().parents[2]

    # define data directories
    BASE_DATA_DIR = PROJECT_DIR / "data"  
    RAW_DATA_DIR = BASE_DATA_DIR / "raw"
    INT_DATA_DIR = BASE_DATA_DIR / "interim"
    POST_DATA_DIR = BASE_DATA_DIR / "processed"

    RAW_DATA_DIR.mkdir(parents=True, exist_ok=True)
    INT_DATA_DIR.mkdir(parents=True, exist_ok=True)
    POST_DATA_DIR.mkdir(parents=True, exist_ok=True)

    ASSET_DATA_DIR = RAW_DATA_DIR / "assets"
    CPI_DATA_DIR = RAW_DATA_DIR / "cpi"

    CPI_DATA_DIR.mkdir(parents=True, exist_ok=True)
    ASSET_DATA_DIR.mkdir(parents=True, exist_ok=True)

    start_date = ui.input_start()
    if start_date != False:
        end_date = ui.input_end(start_date)
        if end_date != False:
            tickers = ui.input_tickers()
            if tickers:
                load.fetch_CPI_data(start_date, end_date, CPI_DATA_DIR)
                load.fetch_equity_data(tickers, start_date, end_date, ASSET_DATA_DIR)
                load.fetch_gold_data(start_date, end_date, ASSET_DATA_DIR)

                print(f"Data loading has finished, please check raw data files in {RAW_DATA_DIR}\n")
                cont = input("Continue? (y/n): ")

                if cont.lower() == "y":
                    process.get_monthly_prices(ASSET_DATA_DIR, INT_DATA_DIR)
                    process.calculate_inflation_rates(CPI_DATA_DIR, POST_DATA_DIR)
                    process.process_asset_files(INT_DATA_DIR, POST_DATA_DIR)
                    print(f"Data processing has finished, please check processed data files in {POST_DATA_DIR} ")
                
                else:
                    print("Exiting the program.")


if __name__ == '__main__':
    main()