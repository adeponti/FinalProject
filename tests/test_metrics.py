import pandas as pd
from realestateCH.metrics import (
    compute_rent_per_m2,
    compute_buy_price_per_m2,
    compute_price_to_rent_ratio,
    average_rent_per_m2_by_canton,
    rank_cantons_by_rent,
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


def test_average_rent_per_m2_by_canton():
    df = pd.DataFrame({
        "canton": ["VD", "VD", "ZH"],
        "price_chf": [2000, 1500, 3000],
        "area_m2": [50, 30, 100]
    })

    result = average_rent_per_m2_by_canton(df)

    # Check that result contains the right columns
    assert "canton" in result.columns
    assert "avg_rent_per_m2" in result.columns

    # Compute expected manually
    vd_avg = ((2000/50) + (1500/30)) / 2
    zh_avg = (3000/100)

    # Should have 2 rows
    assert len(result) == 2

    # Extract values
    res_dict = dict(zip(result["canton"], result["avg_rent_per_m2"]))

    assert abs(res_dict["VD"] - vd_avg) < 1e-6
    assert abs(res_dict["ZH"] - zh_avg) < 1e-6


def test_rank_cantons_by_rent():
    df = pd.DataFrame({
        "canton": ["VD", "VD", "ZH", "GE"],
        "price_chf": [2000, 1500, 3000, 4000],
        "area_m2": [50, 30, 100, 80]
    })

    result = rank_cantons_by_rent(df)

    # compute expected manually
    vd_avg = ((2000/50) + (1500/30)) / 2
    zh_avg = (3000/100)
    ge_avg = (4000/80)

    expected_order = ["GE", "VD", "ZH"]  # highest to lowest

    assert list(result["canton"]) == expected_order
