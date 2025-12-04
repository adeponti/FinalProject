import pandas as pd
from realestateCH.metrics import (
    compute_rent_per_m2,
    compute_buy_price_per_m2,
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
