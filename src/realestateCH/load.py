import pandas as pd
import os

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
    script_dir = os.path.dirname(os.path.abspath(__file__))
    project_root = os.path.dirname(os.path.dirname(script_dir))
    
    # FIXED: changed 'Cantons' to 'Canton'
    file_path = os.path.join(project_root, 'data_raw', 'Total-Rent-WithCanton.csv')
    
    print(f"Loading rent data from: {file_path}")
    df = pd.read_csv(file_path)
    return df

def load_buy_data():
    script_dir = os.path.dirname(os.path.abspath(__file__))
    project_root = os.path.dirname(os.path.dirname(script_dir))
    
    # FIXED: changed 'Cantons' to 'Canton'
    file_path = os.path.join(project_root, 'data_raw', 'Total-Buy-WithCanton.csv')
    
    print(f"Loading buy data from: {file_path}")
    df = pd.read_csv(file_path)
    return df

