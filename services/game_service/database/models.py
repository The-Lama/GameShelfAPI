from .database import db


class Game(db.Model):
    """
    Represents a board game entitiy in the database.

    Attributes:
        bgg_id (int): The unique identifier of the game from BoardGameGeek.
        name (str): Teh name of the board game.
    """

    __tablename__ = "games"

    bgg_id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(255), nullable=False)

    def to_dict(self):
        """Convert the Game object into a dictionary."""
        return {"id": self.bgg_id, "name": self.name}
