import os
import pandas as pd

from realestateCH.load import (
    load_data,
    load_rent_data,
    load_buy_data,
)
from realestateCH.metrics import average_rent_per_m2_by_canton


def test_load_data_with_temp_file(tmp_path):
    """
    Basic test: load_data should correctly read a simple CSV.
    """
    path = tmp_path / "test.csv"
    original = pd.DataFrame({"a": [1, 2]})
    original.to_csv(path, index=False)

    loaded = load_data(path)

    assert not loaded.empty
    assert list(loaded.columns) == ["a"]
    assert loaded["a"].tolist() == original["a"].tolist()


def test_load_rent_data_file_exists():
    """
    Ensure that the official Total-Rent.csv file exists.
    """
    path = os.path.join("data_raw", "Total-Rent.csv")
    assert os.path.exists(path)


def test_load_buy_data_file_exists():
    """
    Ensure that the official Total-Buy.csv file exists.
    """
    path = os.path.join("data_raw", "Total-Buy.csv")
    assert os.path.exists(path)


def test_load_rent_data_has_canton_column():
    """
    load_rent_data should return a DataFrame
    containing a non-missing 'canton' column.
    """
    df = load_rent_data()

    assert not df.empty
    assert "canton" in df.columns
    assert df["canton"].notna().all()


def test_load_buy_data_has_canton_column():
    """
    load_buy_data should return a DataFrame
    containing a non-missing 'canton' column.
    """
    df = load_buy_data()

    assert not df.empty
    assert "canton" in df.columns
    assert df["canton"].notna().all()


def test_average_rent_per_m2_by_canton_on_real_data():
    """
    Full pipeline test: use the real rent dataset to compute
    the average rent per m2 by canton.
    """
    rent_df = load_rent_data()
    result = average_rent_per_m2_by_canton(rent_df)

    # The result should not be empty and must contain the expected columns
    assert not result.empty
    assert "canton" in result.columns
    assert "avg_rent_per_m2" in result.columns

    # At least a few cantons should be present
    assert result["canton"].nunique() >= 2
