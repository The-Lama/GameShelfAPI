import pandas as pd

def load_csv(path):
    try:
        return pd.read_csv(path)
    except FileNotFoundError:
        raise Exception(f"Dataset as {path} was not found.")