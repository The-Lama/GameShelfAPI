import logging

import pandas as pd

logger = logging.getLogger(__name__)


def load_csv(path: str) -> pd.DataFrame:
    """Load a CSV file as a pandas dataframe."""
    logger.info(f"Attempting to load dataset from {path}")
    try:
        df = pd.read_csv(path)
    except FileNotFoundError:
        logger.error(f"Dataset at {path} was not found.")
        raise FileNotFoundError(f"Dataset at {path} was not found.")
    except pd.errors.EmptyDataError:
        logger.error(f"Dataset at {path} is empty.")
        raise ValueError(f"Dataset at {path} is empty.")
    except Exception as e:
        logger.exception(f"An error occurred while loading the dataset at {path}: {e}")
        raise RuntimeError(
            f"An error occurred while loading the dataset at {path}: {e}"
        )

    logger.info(f"Dataset loaded successfully from {path}, with {len(df)} rows.")
    return df
