# -*- coding: utf-8 -*-
import os
from pathlib import Path

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

from sklearn.linear_model import LinearRegression

PROJECT_DIR = Path(__file__).resolve().parents[2]
MODEL_DIR = PROJECT_DIR / "models"

def plot_regression_results(file_path):
    # load data from CSV file
    asset_data = pd.read_csv(file_path)
    asset_name = file_path.split('/')[-1].split('_')[0]  # extract asset name from file name

    # prepare data for regression
    X = asset_data['Inflation Rates'].values.reshape(-1, 1)
    y = asset_data['Log Returns'].values

    # fit the regression model
    model = LinearRegression()
    model.fit(X, y)

    # create predictions for the line
    X_line = np.linspace(X.min(), X.max(), 100).reshape(-1, 1)
    y_line = model.predict(X_line)

    # plot
    plt.figure(figsize=(10, 6))
    sns.scatterplot(x=asset_data['Inflation Rates'], y=asset_data['Log Returns'], color='blue', label='Data Points')
    plt.plot(X_line, y_line, color='red', label='Regression Line')
    plt.title(f'Regression Analysis for {asset_name}')
    plt.xlabel('Inflation Rates')
    plt.ylabel('Log Returns')
    plt.legend()
    plt.grid(True)
    plt.show()

def plot_robustness_checks(file_path):
    # load robustness check data
    robustness_data = pd.read_csv(file_path)

    # plotting
    plt.figure(figsize=(12, 6))

    # box plot for cross-validation R^2 scores
    plt.subplot(1, 2, 1)
    sns.boxplot(data=robustness_data, x='Asset Name', y='CV Average R^2')
    plt.title('Cross-Validation R² Scores')
    plt.xlabel('Asset')
    plt.ylabel('R² Score')

    # bar plot for robust regression coefficients
    plt.subplot(1, 2, 2)
    sns.barplot(data=robustness_data, x='Asset Name', y='Robust Beta Coefficient')
    plt.title('Robust Regression Beta Coefficients')
    plt.xlabel('Asset')
    plt.ylabel('Beta Coefficient')

    plt.tight_layout()
    plt.show()

def run_visualization(MODEL_DIR):
    for filename in os.listdir(MODEL_DIR):
        if filename.endswith("merged_data.csv"):
            file_path = os.path.join(MODEL_DIR, filename)
            plot_regression_results(file_path)

        elif filename.startswith("robustness_"):
            file_path = os.path.join(MODEL_DIR, filename)
            plot_robustness_checks(file_path)

def main():
    run_visualization(MODEL_DIR)

if __name__ == '__main__':
    
    main()