import argparse
import logging
import os

from dotenv import load_dotenv


def parse_arguments() -> argparse.Namespace:
    """Parse CLI arguments."""
    load_dotenv()
    parser = argparse.ArgumentParser(
        description="Run the GameShelfAPI flask application."
    )
    parser.add_argument(
        "--verbose",
        action="store_true",
        help="Enable debug logging for the application.",
    )
    parser.add_argument(
        "--port",
        type=int,
        default=os.getenv("PORT", 5001),
        help="Port number to run the Flask application",
    )
    parser.add_argument(
        "--host",
        type=str,
        default=os.getenv("HOST", "0.0.0.0"),
        help="Host address for the Flask application.",
    )
    parser.add_argument(
        "--games_dataset",
        type=str,
        default=os.getenv("DATASET_PATH", "data/games.csv"),
        help="Path to the dataset holding the BGG games data.",
    )
    parser.add_argument(
        "--database_url",
        type=str,
        default=os.getenv("DATABASE_URL", "sqlite:///instance/games.db"),
        help="Path to the database file.",
    )
    return parser.parse_args()


def configure_logging(verbose: bool) -> None:
    """Configure logging level based on verbosity."""
    logging.basicConfig(
        level=logging.DEBUG if verbose else logging.INFO,
        format="%(asctime)s - %(name)s - %(message)s",
    )
