from ..utils.data_loader import load_csv
from .database import db
from .models import Game


def seed_data(dataset_path: str) -> None:
    """
    Seed the database with initial data.

    Args:
        dataset_path (str): The path to the database URL.

    Raises:
        FileNotFoundError: if the dataset file is not found.
        ValueError: If the dataset is empty.
    """
    if Game.query.count() == 0:
        games_data = load_csv(dataset_path)
        for _, row in games_data.iterrows():
            game = Game(
                game_id=row["BGGId"],
                name=row["Name"],
            )
            db.session.add(game)
        db.session.commit()


def seed_test_data() -> None:
    """Seed the database with test data."""
    test_games = [
        Game(game_id=1, name="Die Macher"),
        Game(game_id=2, name="Dragonmaster"),
        Game(game_id=3, name="Samurai"),
        Game(game_id=4, name="Tal der Könige"),
        Game(game_id=5, name="Acquire"),
        Game(game_id=6, name="Mare Mediterraneum"),
        Game(game_id=32, name="Buffalo Chess"),
        Game(game_id=171, name="Chess"),
    ]

    db.session.add_all(test_games)
    db.session.commit()
