import logging
from typing import List, Optional, TypedDict

import pandas as pd

from services.game_service.utils.data_loader import load_csv

logger = logging.getLogger(__name__)


class GameDict(TypedDict):
    """A TypedDict representing a board game."""

    BGGId: int
    Name: str


class GameService:
    """A service class for managing board game data."""

    games: pd.DataFrame

    def __init__(self, dataset_path: str = "data/games.csv") -> None:
        """Initialize the game service with a dataset."""
        logger.info(f"Initializing GameService with dataset: {dataset_path}")
        self.games = load_csv(dataset_path)
        self._validate_dataset()

    def _validate_dataset(self) -> None:
        """Validate the structure of the loaded dataset."""
        required_columns = {"BGGId", "Name"}
        if not required_columns.issubset(self.games.columns):
            logger.error(f"Dataset is missing required columns: {required_columns}")
            raise ValueError(f"Dataset must contain columns: {required_columns}")
        self.games = self.games[list(required_columns)]
        logger.info("Dataset validated successfully.")

    @classmethod
    def from_static_data(cls, games: List[GameDict]) -> "GameService":
        """Create a GameService using a static list of games."""
        logger.debug("Creating GameService from static data.")
        instance = cls.__new__(cls)
        games_df = pd.DataFrame(games)
        instance.games = games_df
        logger.info("GameService created from static data successfully.")
        return instance

    def list_games(self) -> List[GameDict]:
        """List all board games."""
        logger.debug("Listing all board games.")
        return self.games.to_dict(orient="records")

    def get_game(self, game_id: int) -> Optional[GameDict]:
        """Get board game by id."""
        logger.debug(f"Fetching game with ID: {game_id}")
        game = self.games.loc[self.games["BGGId"] == game_id]
        if game.empty:
            logger.warning(f"Game with ID {game_id} not found.")
            return None
        return game.iloc[0].to_dict()
