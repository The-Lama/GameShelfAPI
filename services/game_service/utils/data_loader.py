import pandas as pd


def load_csv(path):
    """Load a CSV file as a pandas dataframe."""
    try:
        return pd.read_csv(path)
    except FileNotFoundError:
        raise Exception(f"Dataset as {path} was not found.")
