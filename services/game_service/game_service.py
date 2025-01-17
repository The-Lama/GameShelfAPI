import pandas as pd
from services.game_service.utils.data_loader import load_csv

class GameService:
    def __init__(self, dataset_path="data/games.csv"):
        self.games = load_csv(dataset_path)
        self.games = self.games[["BGGId", "Name"]]

    def list_games(self):
        return self.games.to_dict(orient="records")

    def get_game(self, game_id):
        game = self.games.loc[self.games["BGGId"] == game_id]
        return game.iloc[0].to_dict() if not game.empty else None