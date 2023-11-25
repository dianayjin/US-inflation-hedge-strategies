# -*- coding: utf-8 -*-
import os

import numpy as np
import pandas as pd

from sklearn.linear_model import LinearRegression, HuberRegressor
from sklearn.metrics import mean_squared_error, r2_score
from sklearn.model_selection import cross_val_score, KFold

def load_merged_data(DATA_DIR):
    merged_data = {}
    for filename in os.listdir(DATA_DIR):
        if filename.endswith("_merged_data.csv"):
            asset_name = filename.split('_')[0]
            file_path = os.path.join(DATA_DIR, filename)
            merged_data[asset_name] = pd.read_csv(file_path)
    
    return merged_data

def run_regression(asset_name, asset_data):
    # prepare the data for regression
    X = asset_data[['Inflation Rates']].values.reshape(-1, 1)
    y = asset_data['Log Returns'].values

    # initialize and fit the linear regression model
    model = LinearRegression()
    model.fit(X, y)

    # predictions for evaluation
    y_pred = model.predict(X)

    return {
        'Asset Name': asset_name,
        'Beta Coefficient': model.coef_[0],
        'Intercept': model.intercept_,
        'Mean Squared Error': mean_squared_error(y, y_pred),
        'Coefficient of Determination (R^2 Score)': r2_score(y, y_pred)
    }

def robustness_checks(asset_name, asset_data):
    X = asset_data[['Inflation Rates']].values.reshape(-1, 1)
    y = asset_data['Log Returns'].values

    # initialize standard linear regression model
    lr_model = LinearRegression()

    # cross-Validation
    cv = KFold(n_splits=5, shuffle=True, random_state=42)
    cv_scores = cross_val_score(lr_model, X, y, cv=cv, scoring='r2')

    # Robust Regression
    robust_model = HuberRegressor()
    robust_model.fit(X, y)
    beta_robust = robust_model.coef_[0]
    intercept_robust = robust_model.intercept_

    return {
        'Asset Name': asset_name,
        'CV Average R^2': np.mean(cv_scores),
        'CV R^2 Scores': cv_scores,
        'Robust Beta Coefficient': beta_robust,
        'Robust Intercept': intercept_robust
    }
