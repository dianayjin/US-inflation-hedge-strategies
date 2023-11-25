US inflation hedges
==============================

What domestic assets are most useful to US individual investors to hedge against inflation?

## Data Sources
- Equities: Yahoo Finance
- Gold: London Bullion Market via Nasdaq
- CPI Data: US Bureau of Labor Statistics

## Setup Instructions
1. **Environment Setup**:
   - Create a virtual environment: `python -m venv venv_name`
   - Activate the virtual environment:
     - On Windows: `venv_name\Scripts\activate`
     - On Linux/Mac: `source venv_name/bin/activate`
   - Install required libraries: `pip install -r requirements.txt`

2. **API Keys**:
   Most data sources require API keys. Store these keys securely using environment variables. We use the `dotenv` approach for this.
   - Rename `.env.example` to `.env`.
   - Fill in the required API keys or configurations.
   - The application will load these keys automatically.

3. **Fetching Data**:
   - To populate the raw data folder, run the script [in notebooks].
   - To output processed data, run the script [].

4. **Analysis**:
   Instructions on how to run your analysis, scripts, or notebooks.
 
Project Organization
------------

    ├── LICENSE
    ├── Makefile           <- Makefile with commands like `make data` or `make train`
    ├── README.md          <- The top-level README for developers using this project.
    ├── data
    │   ├── external       <- Data from third party sources.
    │   ├── interim        <- Intermediate data that has been transformed.
    │   ├── processed      <- The final, canonical data sets for modeling.
    │   └── raw            <- The original, immutable data dump.
    │
    ├── docs               <- A default Sphinx project; see sphinx-doc.org for details
    │
    ├── models             <- Trained and serialized models, model predictions, or model summaries
    │
    ├── notebooks          <- Jupyter notebooks. Naming convention is a number (for ordering),
    │                         the creator's initials, and a short `-` delimited description, e.g.
    │                         `1.0-jqp-initial-data-exploration`.
    │
    ├── references         <- Data dictionaries, manuals, and all other explanatory materials.
    │
    ├── reports            <- Generated analysis as HTML, PDF, LaTeX, etc.
    │   └── figures        <- Generated graphics and figures to be used in reporting
    │
    ├── requirements.txt   <- The requirements file for reproducing the analysis environment, e.g.
    │                         generated with `pip freeze > requirements.txt`
    │
    ├── setup.py           <- makes project pip installable (pip install -e .) so src can be imported
    ├── src                <- Source code for use in this project.
    │   ├── __init__.py    <- Makes src a Python module
    │   │
    │   ├── data           <- Scripts to download or generate data
    │   │   └── load_data.py    
    │   │   └── make_dataset.py
    │   │   └── process_data.py
    │   │   └── user_input.py
    │   │
    │   ├── features       <- Scripts to turn raw data into features for modeling
    │   │   └── build_features.py
    │   │
    │   ├── models         <- Scripts to train models and then use trained models to make
    │   │   │                 predictions
    │   │   ├── regression_model.py
    │   │   └── run_regression.py
    │   │
    │   └── visualization  <- Scripts to create exploratory and results oriented visualizations
    │       └── visualize.py
    │
    └── tox.ini            <- tox file with settings for running tox; see tox.readthedocs.io


--------

<p><small>Project based on the <a target="_blank" href="https://drivendata.github.io/cookiecutter-data-science/">cookiecutter data science project template</a>. #cookiecutterdatascience</small></p>
