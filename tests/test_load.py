from realestateCH.load import load_data, load_rent_data, load_buy_data
import os


def test_load_data_is_callable():
    # Basic test: check that load_data is a callable function
    assert callable(load_data)


def test_load_rent_data():
    # Make sure the Total-Rent file exists
    path = os.path.join("data_raw", "Total-Rent.csv")
    assert os.path.exists(path)

    df = load_rent_data()

    # Basic checks
    assert len(df) > 0
    assert "price_chf" in df.columns
    assert "area_m2" in df.columns


def test_load_buy_data():
    # Make sure the Total-Buy file exists
    path = os.path.join("data_raw", "Total-Buy.csv")
    assert os.path.exists(path)

    df = load_buy_data()

    # Basic checks
    assert len(df) > 0
    assert "price_chf" in df.columns
    assert "area_m2" in df.columns
