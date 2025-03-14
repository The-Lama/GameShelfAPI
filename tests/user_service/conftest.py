from typing import Generator

import pytest
from flask import Flask
from flask.testing import FlaskClient
from sqlalchemy.orm import scoped_session, sessionmaker

from services.user_service.app import create_app, setup_database
from services.user_service.database.database import db

from .seed_data import seed_database


@pytest.fixture(scope="session")
def app() -> Generator[Flask, None, None]:
    """
    Create and configure a flask application instance for testing.

    Yields (Flask): A configured Flask application instance.
    """
    test_db_url = "sqlite:///:memory:"
    app = create_app(test_db_url)
    app.config["Testing"] = True
    setup_database(app)

    with app.app_context():
        seed_database()
        yield app
        db.drop_all()


@pytest.fixture(scope="session")
def client(app: Flask) -> FlaskClient:
    """
    Provide a client for the Flask application.

    Args:
        app (Flask): The Flask application instance.

    Returns:
        FlaskClient: A test client for simulating HTTP responses.
    """
    return app.test_client()


@pytest.fixture(autouse=True)
def isolated_db_session(app: Flask):
    """
    Provide an isolated database session for each test.

    Args:
        app (Flask): A Flask application instance.
    """
    with app.app_context():
        connection = db.engine.connect()
        transaction = connection.begin()
        session_factory = sessionmaker(bind=connection)
        session = scoped_session(session_factory)
        db.session = session
        yield
        transaction.rollback()
        connection.close()
        session.remove()
