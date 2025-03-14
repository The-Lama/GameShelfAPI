import logging
from typing import List

from ..game_service import GameDict

logger = logging.getLogger(__name__)


class InvalidPaginationParametersError(Exception):
    """Raised when pagination parameters are invalid."""

    def __init__(self, page, limit):
        """
        Initialize the exception.

        Args:
            page (int): The page the user wants to see.
            limit (int): The maximum amount of games per page.
        """
        super().__init__(
            f"Invalid pagination parameters: page={page}, "
            f"limit={limit}. Both must be >= 1."
        )
        self.page = page
        self.limit = limit


class PageExceedsDataRangeError(Exception):
    """Raised when the page exceeds the data range."""

    def __init__(self, page):
        """
        Initialize the exception.

        Args:
            page (int): The page the user wants to see.
        """
        super().__init__(f"Page {page} exceeds available data range.")
        self.page = page


def paginate(data: List[GameDict], page: int, limit: int) -> List[GameDict]:
    """
    Return a paginated subset of data based on the given page and limit.

    Args:
        data (List[GameDict]): A list of game dictionary objects.
        page (int): The page number to retrieve.
        limit (int): Number of game dictionary objects per page.

    Returns:
        A subset of the game dictionary objects for the requested range.
    """
    logger.debug(f"Pagination parameters - page: {page}, limit: {limit}")
    if page < 1 or limit < 1:
        raise InvalidPaginationParametersError(page, limit)

    start = (page - 1) * limit
    end = start + limit

    if start >= len(data):
        raise PageExceedsDataRangeError(page)

    return data[start:end]
