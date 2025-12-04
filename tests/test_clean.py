import pandas as pd
from realestateCH.clean import clean_data

def test_clean_data():
    sample = pd.DataFrame({
        "price_chf": ["1000", "N/A"],
        "rooms": ["2.5", "N/A"],
        "area_m2": ["50", "N/A"]
    })

    cleaned = clean_data(sample)

    # After cleaning, numeric columns should not have type 'object'
    assert cleaned["price_chf"].dtype != object
    assert cleaned["rooms"].dtype != object
    assert cleaned["area_m2"].dtype != object
