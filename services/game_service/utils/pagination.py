import logging

import pandas as pd

logger = logging.getLogger(__name__)


def paginate(data: pd.DataFrame, page: int, limit: int) -> pd.DataFrame:
    """Return a paginated subset of data based on the given page and limit."""
    logger.debug(f"Pagination parameters - page: {page}, limit: {limit}")
    if page < 1 or limit < 1:
        raise ValueError(
            f"Invalid pagination parameters: page={page}, "
            f"limit={limit}. Both must be >= 1."
        )

    start = (page - 1) * limit
    end = start + limit

    if start >= len(data):
        raise IndexError(f"Page {page} exceeds available data range.")

    return data[start:end]
