import pandas as pd
from realestateCH.metrics import (
    compute_rent_per_m2,
    compute_buy_price_per_m2,
    compute_price_to_rent_ratio,
)



def test_compute_rent_per_m2():
    # Simple example DataFrame
    df = pd.DataFrame({
        "price_chf": [2000, 1500],
        "area_m2": [50, 30]
    })

    result = compute_rent_per_m2(df)

    # The new column must exist
    assert "rent_per_m2" in result.columns

    # Check a couple of expected values
    assert result.loc[0, "rent_per_m2"] == 2000 / 50
    assert result.loc[1, "rent_per_m2"] == 1500 / 30


def test_compute_buy_price_per_m2():
    df = pd.DataFrame({
        "price_chf": [800000, 500000],
        "area_m2": [100, 50]
    })

    result = compute_buy_price_per_m2(df)

    assert "buy_price_per_m2" in result.columns
    assert result.loc[0, "buy_price_per_m2"] == 800000 / 100
    assert result.loc[1, "buy_price_per_m2"] == 500000 / 50



def test_price_to_rent_ratio():
    buy = pd.DataFrame({
        "zip_code": [1000],
        "price_chf": [1000000]   # prezzo di acquisto
    })

    rent = pd.DataFrame({
        "zip_code": [1000],
        "price_chf": [2000]      # affitto mensile
    })

    result = compute_price_to_rent_ratio(buy, rent)

    assert "price_to_rent_ratio" in result.columns
    expected = 1000000 / (12 * 2000)
    assert result.loc[0, "price_to_rent_ratio"] == expected
