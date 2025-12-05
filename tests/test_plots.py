import pandas as pd
from realestateCH.plots import plot_average_rent_per_canton

def test_plot_average_rent_per_canton():
    df = pd.DataFrame({
        "canton": ["VD", "ZH"],
        "price_chf": [2000, 3000],
        "area_m2": [50, 100]
    })

    # Just check that the function returns an Axes object without errors
    ax = plot_average_rent_per_canton(df)

    assert ax is not None
