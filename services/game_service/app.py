import logging

from flask import Flask, g

from services.game_service.game_service import GameService
from services.game_service.routes import game_routes

logging.basicConfig(
    level=logging.INFO, format="%(asctime)s - %(name)s - %(levelname)s - %(message)s"
)
logger = logging.getLogger(__name__)

app = Flask(__name__)
app.register_blueprint(game_routes)


def get_game_service() -> GameService:
    """Return the GameService instance."""
    logger.debug("Retrieving the GameService instance.")
    if "GAME_SERVICE" in app.config:
        return app.config["GAME_SERVICE"]
    return game_service


@app.before_request
def set_game_service() -> None:
    """Set the GameService instance in the global context."""
    g.game_service = get_game_service()


if __name__ == "__main__":
    port = 5001
    host = "0.0.0.0"
    dataset_path = "data/games.csv"

    logger.info("Starting the Flask application...")
    logger.info("Application is configured with the following settings:")
    logger.info(f"HOST: {host}, PORT: {port}, Dataset Path: {dataset_path}")

    game_service = GameService(dataset_path)
    app.run(host="0.0.0.0", port=5001)
