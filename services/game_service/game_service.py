import logging
from typing import List, Optional, TypedDict

from .database.models import Game

logger = logging.getLogger(__name__)


class GameDict(TypedDict):
    """A TypedDict representing a board game."""

    BGGId: int
    Name: str


class GameService:
    """A service for managing board game data."""

    def __init__(self) -> None:
        """Initialize the GameService."""
        pass

    def list_games(self, name_filter: Optional[str] = None) -> List[GameDict]:
        """List board games that satisfy and optinal filter."""
        query = Game.query

        if name_filter:
            logger.debug(f"Filtering games with name containing: '{name_filter}'")
            query = query.filter(Game.name.ilike(f"%{name_filter}%"))

        games = query.all()
        logger.debug(f"Found {len(games)} for filter {name_filter}")

        return [game.to_dict() for game in games]

    def get_game(self, bgg_id: int) -> Optional[GameDict]:
        """Get board game by BGGId."""
        logger.debug(f"Fetching game with BGGId: {bgg_id}")
        game = Game.query.filter_by(bgg_id=bgg_id).one_or_none()
        if not game:
            logger.warning(f"Game with BGGId {bgg_id} not found.")
            return None
        return game.to_dict()
