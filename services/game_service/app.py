from flask import Flask, g

from services.game_service.game_service import GameService
from services.game_service.routes import game_routes

app = Flask(__name__)
app.register_blueprint(game_routes)

game_service = GameService("data/games.csv")


def get_game_service():
    """Return the GameService instance."""
    if "GAME_SERVICE" in app.config:
        return app.config["GAME_SERVICE"]
    return game_service


@app.before_request
def set_game_service():
    """Set the GameService instance in the global context."""
    g.game_service = get_game_service()


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5001)
