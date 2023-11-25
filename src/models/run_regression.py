# -*- coding: utf-8 -*-
import os
from pathlib import Path

import pandas as pd

import regression_model as rmodel

PROJECT_DIR = Path(__file__).resolve().parents[2]
MODEL_DIR = PROJECT_DIR / "models"
POST_DATA_DIR = PROJECT_DIR / "data" / "processed"

def main():
    """ 
    Runs data merging and regression modeling scripts to regress merged data and output model and robustness results (saved in ../models).
    """
    merged_data = rmodel.load_merged_data(MODEL_DIR)

    # perform regression for each asset and save the results
    results = []
    for asset_name, asset_data in merged_data.items():
        try:
            output = rmodel.run_regression(asset_name, asset_data)
            results.append(output)
        except:
            print(f"Unable to run regression for: {asset_name}\n")
    results_df = pd.DataFrame(results)

    # save the results to a CSV file
    output_file = os.path.join(MODEL_DIR, f'regression_results.csv')
    results_df.to_csv(output_file, index=False)
    print(f"Regression results saved to {output_file}\n")

    # perform robustness checks for each asset
    robustness_results = []
    for asset_name, asset_data in merged_data.items():
        try:
            output = rmodel.robustness_checks(asset_name, asset_data)
            robustness_results.append(output)
        except:
            print(f"Unable to run robustness check for: {asset_name}\n")
    robustness_results_df = pd.DataFrame(robustness_results)

    # file path for the output CSV file
    output_file = os.path.join(MODEL_DIR, f'robustness_check_results.csv')
    # save to CSV
    robustness_results_df.to_csv(output_file, index=False)
    print(f"Robustness check results saved to {output_file}\n")

if __name__ == '__main__':
    
    main()