import logging

import pandas as pd

logger = logging.getLogger(__name__)


def load_csv(path: str) -> pd.DataFrame:
    """
    Load a CSV file as a pandas dataframe.

    Args:
        path (str): The file path of the CSV dataset.

    Returns:
        pd.Dataframe: A pandas DataFrame containing the CSV data.

    Raises:
        FileNotFoundError: If the specified file is not found.
        ValueError: If the CSV file is empty.
    """
    logger.info(f"Attempting to load dataset from {path}")

    try:
        df = pd.read_csv(path)
    except FileNotFoundError as e:
        logger.error(f"Dataset at {path} was not found.")
        raise FileNotFoundError(f"Dataset at {path} was not found.") from e
    except pd.errors.EmptyDataError as e:
        logger.error(f"Dataset at {path} is empty.")
        raise ValueError(f"Dataset at {path} is empty.") from e

    logger.info(f"Dataset loaded successfully from {path}, with {len(df)} rows.")
    return df
