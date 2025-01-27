import argparse
import logging


def parse_arguments() -> argparse.Namespace:
    """Parse CLI arguments."""
    parser = argparse.ArgumentParser(
        description="Run the GameShelfAPI flask application."
    )
    parser.add_argument(
        "--verbose",
        action="store_true",
        help="Enable debug logging for the application.",
    )
    return parser.parse_args()


def configure_logging(verbose: bool) -> None:
    """Configure logging level based on verbosity."""
    logging.basicConfig(
        level=logging.DEBUG if verbose else logging.INFO,
        format="%(asctime)s - %(name)s - %(message)s",
    )
