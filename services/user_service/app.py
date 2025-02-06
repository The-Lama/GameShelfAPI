import logging
import sys

from flask import Flask

from ..common.arg_parser import configure_logging, parse_arguments
from .database.database import db, init_db
from .routes import user_routes

logger = logging.getLogger(__name__)


def create_app(database_url: str) -> Flask:
    """
    Create and configure the Flask application.

    Args:
        database_url (str): The database connection URL.

    Returns:
        Flask: The configured Flask application instance.
    """
    logger.debug(f"Creating app with database URL: {database_url}")

    app = Flask(__name__)
    app.config["SQLALCHEMY_DATABASE_URI"] = database_url
    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

    app.register_blueprint(user_routes)
    return app


def setup_database(app: Flask) -> None:
    """
    Initialize the database.

    Args:
        app (Flask): The Flask application instance.
    """
    logger.info("Initializing database...")
    init_db(app)
    with app.app_context():
        db.create_all()


if __name__ == "__main__":
    args = parse_arguments("user_service")
    configure_logging(args.verbose)

    port = args.port
    host = args.host
    database_url = args.database_url

    logger.info("Starting the user service...")
    logger.info("Application is configured with the following settings:")
    logger.info(f"HOST: {host}, PORT: {port}")
    logger.info(f"Database_url: {database_url}")

    try:
        app = create_app(database_url)

        setup_database(app)

        app.run(host=host, port=port)
    except Exception as e:
        logging.critical(f"User service could not start: {e}", exc_info=True)
        sys.exit(1)
