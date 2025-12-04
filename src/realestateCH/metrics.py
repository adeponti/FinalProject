import pandas as pd

def compute_rent_per_m2(df: pd.DataFrame) -> pd.DataFrame:
    """
    Compute the monthly rent price per square meter.

    Parameters
    ----------
    df : pandas.DataFrame
        Cleaned dataset containing at least 'price_chf' and 'area_m2'.

    Returns
    -------
    pandas.DataFrame
        DataFrame with an additional column 'rent_per_m2'.
    """
    df = df.copy()

    if "price_chf" not in df.columns or "area_m2" not in df.columns:
        raise ValueError("DataFrame must contain 'price_chf' and 'area_m2' columns.")

    df["rent_per_m2"] = df["price_chf"] / df["area_m2"]

    return df


def compute_buy_price_per_m2(df: pd.DataFrame) -> pd.DataFrame:
    """
    Compute the purchase price per square meter.

    Parameters
    ----------
    df : pandas.DataFrame
        Dataset containing at least 'price_chf' and 'area_m2'.

    Returns
    -------
    pandas.DataFrame
        DataFrame with an additional column 'buy_price_per_m2'.
    """
    df = df.copy()

    if "price_chf" not in df.columns or "area_m2" not in df.columns:
        raise ValueError("DataFrame must contain 'price_chf' and 'area_m2' columns.")

    df["buy_price_per_m2"] = df["price_chf"] / df["area_m2"]

    return df
