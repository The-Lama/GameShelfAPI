import logging

from flask import Flask
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

logger = logging.getLogger(__name__)


def init_db(app: Flask):
    """Bind SQLAlchemy to the Flask app."""
    db.init_app(app)
