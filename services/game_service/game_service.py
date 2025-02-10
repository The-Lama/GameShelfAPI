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
        """
        List board games that satisfy an optional name_filter.

        Args:
            name_filter (str): A filter to filter games by name.

        Returns:
            List[GameDict]:
                A list of dictionaries representing board games that
                match the given filter.

        Raises:
            NoGamesMatchNameFilterError:
                If no games are found that match the given filter.
        """
        query = Game.query

        logger.debug(f"name_filtering games with name containing: '{name_filter}'")
        query = query.filter(Game.name.ilike(f"%{name_filter}%"))
        games = query.all()
        if not games:
            raise NoGamesMatchNameFilterError(name_filter)

        logger.debug(f"Found {len(games)} for name_filter {name_filter}")
        return [game.to_dict() for game in games]

    def get_game(self, game_id: int) -> GameDict:
        """
        Get board game by game_id.

        Args:
            game_id (int): The unique ID of a board game.

        Returns:
            GameDict: A game dictionary object retrieved from the ID.

        Raises:
            GameNotFoundError: If no game has the game_id as ID.
        """
        logger.debug(f"Fetching game with game_id: {game_id}")
        game = Game.query.filter_by(game_id=game_id).one_or_none()
        if not game:
            raise GameNotFoundError(game_id=game_id)
        return game.to_dict()
