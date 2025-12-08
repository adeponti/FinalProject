# realestateCH: Swiss Real Estate Analytics

realestateCH is a Python package designed to load, clean, analyze, and visualize Swiss real estate data (rent & buy markets).  
Developed for the Business Analytics course at HEC Lausanne.

## Features
- Load rent & buy datasets  
- Clean inconsistent or missing values  
- Compute rent per m², buy per m², price-to-rent ratio  
- Produce visualizations  
- Fully tested with pytest + GitHub Actions  
- Documentation website built with Quarto  

## Roles & Contributions
- Alessandro De Ponti — Role 1: Data collection & preparation  
- Gabriele Miglioranzi — Role 2: Package development & documentation  
- Federico Baldicchi — Role 2: Package development & documentation  
- Vasko Georgiev — Role 3: Dashboard & Web App

## Installation

To work with the **realestateCH** package, first clone the repository:

```bash
git clone https://github.com/adeponti/FinalProject.git
cd FinalProject
```

Install the package in editable mode:

```bash
pip install -e .
```

Run the test suite:

```bash
pytest
```

## Quick Start

### Load datasets
```python
from realestateCH.load import load_rent_data, load_buy_data

rent = load_rent_data("data_raw/Total-Rent.csv")
buy = load_buy_data("data_raw/Total-Buy.csv")
```

### Clean data
```python
from realestateCH.clean import clean_data

rent_clean = clean_data(rent)
buy_clean = clean_data(buy)
```

### Compute metrics
```python
from realestateCH.metrics import compute_rent_per_m2

rent_clean["rent_m2"] = compute_rent_per_m2(rent_clean)
```

### Create a plot
```python
from realestateCH.plots import plot_average_rent_per_canton

plot_average_rent_per_canton(rent_clean)
```

## Repository Structure
```text
│
├── data_raw/
│ ├── Total-Rent.csv
│ ├── Total-Buy.csv
│
├── src/
│ └── realestateCH/
│ ├── init.py
│ ├── clean.py
│ ├── load.py
│ ├── metrics.py
│ ├── plots.py
│
├── tests/
│ ├── test_clean.py
│ ├── test_load.py
│ ├── test_metrics.py
│ ├── test_plots.py
│
├── docs/
│ ├── index.qmd
│ ├── installation.qmd
│ ├── get_started.qmd
│ ├── examples.qmd
│ ├── api.qmd
│ └── _quarto.yml
│
├── pyproject.toml
└── README.md
```

## Run the Final Web App

To run the final web application, first clone the repository; in VS Code make sure that you are in the correct folder. Also make sure that you have installed the following: 
-   Python 3.8 or higher 
-   packages: streamlit, pandas, plotly, if not installed, you can do it via pip: 

```bash
pip install streamlit pandas plotly
```
Then make sure that the project folder is organized as above, and run the following command in the terminal: 

```bash
streamlit run app.py
```

## Documentation Website:
https://adeponti.github.io/FinalProject/
