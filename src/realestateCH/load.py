import pandas as pd

def load_data(path: str):
    """
    Load a CSV file into a pandas DataFrame.

    Parameters
    ----------
    path : str
        Path to the CSV file.

    Returns
    -------
    pandas.DataFrame
        Loaded dataset.
    """
    return pd.read_csv(path)

from .clean import clean_data

def load_rent_data():
    """
    Load and clean the official Total-Rent dataset.
    """
    path = "data_raw/Total-Rent.csv"
    df = pd.read_csv(path)
    return clean_data(df)

def load_buy_data():
    """
    Load and clean the official Total-Buy dataset.
    """
    path = "data_raw/Total-Buy.csv"
    df = pd.read_csv(path)
    return clean_data(df)

