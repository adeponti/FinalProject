import pandas as pd
from realestateCH.plots import (
    plot_average_rent_per_canton,
    plot_price_to_rent_ratio_hist,
)


def test_plot_average_rent_per_canton():
    df = pd.DataFrame({
        "canton": ["VD", "ZH"],
        "price_chf": [2000, 3000],
        "area_m2": [50, 100]
    })

    # Just check that the function returns an Axes object without errors
    ax = plot_average_rent_per_canton(df)

    assert ax is not None

def test_plot_price_to_rent_ratio_hist():
    df = pd.DataFrame({
        "price_to_rent_ratio": [10, 12, 15, 20]
    })

    ax = plot_price_to_rent_ratio_hist(df)

    assert ax is not None
