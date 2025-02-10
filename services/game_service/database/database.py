import logging

from flask import Flask
from flask_sqlalchemy import SQLAlchemy

logger = logging.getLogger(__name__)

db = SQLAlchemy()


def init_db(app: Flask):
    """Bind SQLAlchemy to the Flask app."""
    db.init_app(app)
