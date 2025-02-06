import os

from dotenv import load_dotenv

load_dotenv()

# Game Service settings
GAME_SERVICE_PORT = int(os.getenv("GAME_SERVICE_PORT", 5001))
GAME_SERVICE_HOST = os.getenv("GAME_SERVICE_HOST", "0.0.0.0")
GAME_SERVICE_DATASET_PATH = os.getenv("GAME_SERVICE_DATASET_PATH", "data/games.csv")
GAME_SERVICE_DATABASE_URL = os.getenv(
    "GAME_SERVICE_DATABASE_URL", "sqlite:///games.csv"
)

# User Service settings
USER_SERVICE_PORT = int(os.getenv("USER_SERVICE_PORT", 5001))
USER_SERVICE_HOST = os.getenv("GAME_SERVICE_HOST", "0.0.0.0")
USER_SERVICE_DATABASE_URL = os.getenv("USER_SERVICE_DATABASE_URL", "sqlite:///users.db")
