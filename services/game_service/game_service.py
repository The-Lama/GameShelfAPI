import logging
from typing import List, TypedDict

from .database.models import Game
from .exceptions import GameNotFoundError, NoGamesMatchNameFilterError

logger = logging.getLogger(__name__)


class GameDict(TypedDict):
    """A TypedDict representing a board game."""

    game_id: int
    name: str


class GameService:
    """A service for managing board game data."""

    def list_games(self, name_filter: str = "") -> List[GameDict]:
        """List board games that satisfy an optional name_filter."""
        query = Game.query

        logger.debug(f"name_filtering games with name containing: '{name_filter}'")
        query = query.filter(Game.name.ilike(f"%{name_filter}%"))
        games = query.all()
        if not games:
            logger.warning(f"No Games found containing '{name_filter}'")
            raise NoGamesMatchNameFilterError(name_filter)

        logger.debug(f"Found {len(games)} for name_filter {name_filter}")
        return [game.to_dict() for game in games]

    def get_game(self, game_id: int) -> GameDict:
        """Get board game by game_id."""
        logger.debug(f"Fetching game with game_id: {game_id}")
        game = Game.query.filter_by(game_id=game_id).one_or_none()
        if not game:
            logger.warning(f"Game with ID {game_id} not found.")
            raise GameNotFoundError(game_id=game_id)
        return game.to_dict()
