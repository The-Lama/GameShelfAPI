import argparse
import logging

from .config import (
    GAME_SERVICE_DATABASE_URL,
    GAME_SERVICE_DATASET_PATH,
    GAME_SERVICE_HOST,
    GAME_SERVICE_PORT,
    USER_SERVICE_DATABASE_URL,
    USER_SERVICE_HOST,
    USER_SERVICE_PORT,
)


def parse_arguments(service_name: str) -> argparse.Namespace:
    """
    Parse CLI arguments.

    Args:
        service_name (str): The name of the service ('game_service' or 'user_service')

    Returns:
        argparse.Namespace: An object containing the parsed arguments.

    Raises:
        ValueError: If an unsupported service name is provided.
    """
    parser = argparse.ArgumentParser(
        description=f"Run the {service_name} flask application."
    )

    parser.add_argument("--verbose", action="store_true", help="Enable debug logging.")

    if service_name == "game_service":
        parser.add_argument(
            "--port", type=int, default=GAME_SERVICE_PORT, help="Port number."
        )
        parser.add_argument(
            "--host", type=str, default=GAME_SERVICE_HOST, help="Host address."
        )
        parser.add_argument(
            "--games_dataset",
            type=str,
            default=GAME_SERVICE_DATASET_PATH,
            help="Dataset path.",
        )
        parser.add_argument(
            "--database_url",
            type=str,
            default=GAME_SERVICE_DATABASE_URL,
            help="Database URL.",
        )

    elif service_name == "user_service":
        parser.add_argument(
            "--port", type=int, default=USER_SERVICE_PORT, help="Port number."
        )
        parser.add_argument(
            "--host", type=str, default=USER_SERVICE_HOST, help="Host address."
        )
        parser.add_argument(
            "--database_url",
            type=str,
            default=USER_SERVICE_DATABASE_URL,
            help="Database URL.",
        )

    else:
        raise ValueError(f"Unsupported service name: {service_name}")

    return parser.parse_args()


def configure_logging(verbose: bool) -> None:
    """
    Configure logging level based on verbosity.

    Args:
        verbose (bool): Flag to set logging level DEBUG if true, INFO if false.
    """
    logging.basicConfig(
        level=logging.DEBUG if verbose else logging.INFO,
        format="%(asctime)s - %(name)s - %(message)s",
    )
