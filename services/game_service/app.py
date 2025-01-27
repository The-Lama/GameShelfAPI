import logging
import sys

from flask import Flask, g

from .game_service import GameService
from .routes import game_routes
from .utils.config import configure_logging, parse_arguments

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

    args = parse_arguments()
    configure_logging(args.verbose)

    logger.info("Starting the Flask application...")
    logger.info("Application is configured with the following settings:")
    logger.info(f"HOST: {host}, PORT: {port}, Dataset Path: {dataset_path}")

    try:
        game_service = GameService(dataset_path)
        app.run(host="0.0.0.0", port=5001)
    except Exception as e:
        logger.critical(f"Application failed to start: {e}", exc_info=True)
        sys.exit(1)
