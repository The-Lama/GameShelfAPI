from ..utils.data_loader import load_csv
from .database import db
from .models import Game


def seed_data(dataset_path: str) -> None:
    """Seed the database with initial data."""
    if Game.query.count() == 0:
        games_data = load_csv(dataset_path)
        for _, row in games_data.iterrows():
            game = Game(
                bgg_id=row["BGGId"],
                name=row["Name"],
            )
            db.session.add(game)
        db.session.commit()


def seed_test_data():
    """Seed the database with test data."""
    test_games = [
        Game(bgg_id=1, name="Die Macher"),
        Game(bgg_id=2, name="Dragonmaster"),
        Game(bgg_id=3, name="Samurai"),
        Game(bgg_id=4, name="Tal der Könige"),
        Game(bgg_id=5, name="Acquire"),
        Game(bgg_id=6, name="Mare Mediterraneum"),
        Game(bgg_id=32, name="Buffalo Chess"),
        Game(bgg_id=171, name="Chess"),
    ]

    db.session.add_all(test_games)
    db.session.commit()
