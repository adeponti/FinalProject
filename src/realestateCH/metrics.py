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


def compute_price_to_rent_ratio(buy_df: pd.DataFrame, rent_df: pd.DataFrame) -> pd.DataFrame:
    """
    Compute the price-to-rent ratio by merging buy and rent datasets based on zip code.

    Formula:
        ratio = buy_price_chf / (12 * monthly_rent_chf)

    Parameters
    ----------
    buy_df : pandas.DataFrame
        Dataset containing purchase prices.
    rent_df : pandas.DataFrame
        Dataset containing monthly rental prices.

    Returns
    -------
    pandas.DataFrame
        DataFrame with columns:
        - zip_code
        - buy_price_chf
        - rent_price_chf
        - price_to_rent_ratio
    """

    required_cols_buy = {"zip_code", "price_chf"}
    required_cols_rent = {"zip_code", "price_chf"}

    # Check columns exist
    if not required_cols_buy.issubset(buy_df.columns):
        raise ValueError("buy_df must contain 'zip_code' and 'price_chf' columns")
    if not required_cols_rent.issubset(rent_df.columns):
        raise ValueError("rent_df must contain 'zip_code' and 'price_chf' columns")

    # Rename for clarity
    buy_df = buy_df.rename(columns={"price_chf": "buy_price_chf"})
    rent_df = rent_df.rename(columns={"price_chf": "rent_price_chf"})

    # Merge on ZIP code
    df = pd.merge(buy_df, rent_df, on="zip_code", how="inner")

    # Compute ratio
    df["price_to_rent_ratio"] = df["buy_price_chf"] / (12 * df["rent_price_chf"])

    return df


def average_rent_per_m2_by_canton(df: pd.DataFrame) -> pd.DataFrame:
    """
    Compute the average rent price per square meter for each canton.

    Parameters
    ----------
    df : pandas.DataFrame
        Cleaned rent dataset containing 'canton', 'price_chf', and 'area_m2'.

    Returns
    -------
    pandas.DataFrame
        DataFrame with:
        - canton
        - avg_rent_per_m2
    """

    df = df.copy()

    required_cols = {"canton", "price_chf", "area_m2"}
    if not required_cols.issubset(df.columns):
        raise ValueError("DataFrame must contain canton, price_chf and area_m2 columns.")

    # Compute rent per m2
    df["rent_per_m2"] = df["price_chf"] / df["area_m2"]

    # Group by canton
    result = (
        df.groupby("canton")["rent_per_m2"]
        .mean()
        .reset_index(name="avg_rent_per_m2")
        .sort_values("avg_rent_per_m2", ascending=False)
    )

    return result


def rank_cantons_by_rent(df: pd.DataFrame) -> pd.DataFrame:
    """
    Rank cantons by average rent per square meter (descending).

    Parameters
    ----------
    df : pandas.DataFrame
        Cleaned rent dataset.

    Returns
    -------
    pandas.DataFrame
        DataFrame with:
        - canton
        - avg_rent_per_m2
    """

    # Reuse the previous function
    result = average_rent_per_m2_by_canton(df)

    # Already sorted by highest rent, but ensure sorting:
    result = result.sort_values("avg_rent_per_m2", ascending=False).reset_index(drop=True)

    return result
