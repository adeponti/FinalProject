import matplotlib.pyplot as plt
import pandas as pd

from .metrics import average_rent_per_m2_by_canton


def plot_average_rent_per_canton(df: pd.DataFrame, ax=None):
    """
    Plot the average rent price per square meter for each canton.

    Parameters
    ----------
    df : pandas.DataFrame
        Cleaned rent dataset.
    ax : matplotlib.axes.Axes, optional
        Existing axes to draw the plot on. If None, a new figure and axes
        are created.

    Returns
    -------
    matplotlib.axes.Axes
        The axes containing the bar plot.
    """
    # Compute average rent per m2 by canton
    result = average_rent_per_m2_by_canton(df)

    if ax is None:
        fig, ax = plt.subplots()

    ax.bar(result["canton"], result["avg_rent_per_m2"])
    ax.set_xlabel("Canton")
    ax.set_ylabel("Average rent per m² (CHF)")
    ax.set_title("Average monthly rent per m² by canton")
    ax.tick_params(axis="x", rotation=45)

    return ax
