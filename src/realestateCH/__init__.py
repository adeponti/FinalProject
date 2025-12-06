"""
realestateCH: Tools for analysing Swiss real estate data.
"""

from .load import load_data, load_rent_data, load_buy_data
from .clean import clean_data
from .metrics import (
    compute_rent_per_m2,
    compute_buy_price_per_m2,
    compute_price_to_rent_ratio,
    average_rent_per_m2_by_canton,
    rank_cantons_by_rent,
)
from .plots import plot_average_rent_per_canton
