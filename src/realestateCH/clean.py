import pandas as pd

def clean_data(df: pd.DataFrame) -> pd.DataFrame:
    """
    Clean and preprocess the raw real estate dataset.

    Steps:
    - Convert numeric columns to numeric values
    - Replace invalid values with NaN
    - Remove rows with missing or zero area (cannot compute m2 metrics)
    - Drop duplicate rows
    - Standardize canton names if present

    Parameters
    ----------
    df : pandas.DataFrame

    Returns
    -------
    pandas.DataFrame
    """
    df = df.copy()

    # Convert numeric columns
    numeric_cols = ["price_chf", "rooms", "area_m2"]
    for col in numeric_cols:
        if col in df.columns:
            df[col] = pd.to_numeric(df[col], errors="coerce")

    # Remove entries with no area
    if "area_m2" in df.columns:
        df = df[df["area_m2"].notna() & (df["area_m2"] > 0)]

    # Remove duplicate rows
    df = df.drop_duplicates()

    # Standardize canton names if present (optional)
    if "canton" in df.columns:
        df["canton"] = df["canton"].str.strip().str.upper()

    return df
