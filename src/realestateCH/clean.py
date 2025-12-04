import pandas as pd

def clean_data(df: pd.DataFrame) -> pd.DataFrame:
    """
    Clean the raw real estate dataset.

    - Converte le colonne numeriche in numeri (price, rooms, area_m2)
    - Trasforma i valori non validi in NaN

    Parameters
    ----------
    df : pandas.DataFrame
        Raw dataset.

    Returns
    -------
    pandas.DataFrame
        Cleaned dataset.
    """
    df = df.copy()

    numeric_cols = ["price_chf", "rooms", "area_m2"]

    for col in numeric_cols:
        if col in df.columns:
            df[col] = pd.to_numeric(df[col], errors="coerce")

    return df
