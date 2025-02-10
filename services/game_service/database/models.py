from .database import db


class Game(db.Model):
    """
    Represents a board game entity in the database.

    Attributes:
        game_id (int): The unique identifier of the game from BoardGameGeek.
        name (str): The name of the board game.
    """

    __tablename__ = "games"

    game_id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(255), nullable=False)

    def to_dict(self) -> dict:
        """Convert the Game object into a dictionary."""
        return {"id": self.game_id, "name": self.name}
