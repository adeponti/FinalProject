from realestateCH.load import load_data
import os

def test_load_data():
    # Path to the new rent dataset
    csv_path = os.path.join("data_raw", "Total-Rent.csv")

    df = load_data(csv_path)

    # Basic checks
    assert len(df) > 0
    assert "price_chf" in df.columns
