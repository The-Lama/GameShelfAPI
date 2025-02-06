import logging
import sys

from flask import Flask

from ..common.arg_parser import configure_logging, parse_arguments
from .database.database import db, init_db
from .database.seed import seed_data
from .routes import game_routes

logger = logging.getLogger(__name__)


def create_app(database_url: str) -> Flask:
    """Create a Flask application and set configurations and blueprints."""
    logger.debug(f"Creating app with database URL: {database_url}")

    app = Flask(__name__)
    app.config["SQLALCHEMY_DATABASE_URI"] = database_url
    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

    app.register_blueprint(game_routes)
    return app


def setup_database(app: Flask, games_dataset_path: str) -> None:
    """Initialize the database and seed the data."""
    logger.info("Initializing database...")
    init_db(app)
    with app.app_context():
        db.create_all()
        logger.info("Seeding the database with initial data...")
        seed_data(games_dataset_path)


if __name__ == "__main__":
    args = parse_arguments("game_service")
    configure_logging(args.verbose)

    port = args.port
    host = args.host
    dataset_path = args.games_dataset
    database_url = args.database_url

    logger.info("Starting the Flask application...")
    logger.info("Application is configured with the following settings:")
    logger.info(f"HOST: {host}, PORT: {port}")
    logger.info(f"Dataset Path: {dataset_path}, Database_url: {database_url}")

    try:
        app = create_app(database_url)

        setup_database(app, dataset_path)

        app.run(host=host, port=port)
    except Exception as e:
        logger.critical(f"Application failed to start: {e}", exc_info=True)
        sys.exit(1)
