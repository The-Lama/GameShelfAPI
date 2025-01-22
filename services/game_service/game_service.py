import pandas as pd

from services.game_service.utils.data_loader import load_csv


class GameService:
    """A service class for managing board game data."""

    def __init__(self, dataset_path="data/games.csv"):
        """Initialize the game service with a dataset."""
        self.games = load_csv(dataset_path)
        self.games = self.games[["BGGId", "Name"]]

    @classmethod
    def from_static_data(cls, games):
        """Create a GameService using a static list of games."""
        instance = cls.__new__(cls)
        games_df = pd.DataFrame(games)
        instance.games = games_df
        return instance

    def list_games(self):
        """List all board games."""
        return self.games.to_dict(orient="records")

    def get_game(self, game_id):
        """Get board game by id."""
        game = self.games.loc[self.games["BGGId"] == game_id]
        return game.iloc[0].to_dict() if not game.empty else None
