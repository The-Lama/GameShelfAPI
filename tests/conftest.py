from typing import Generator

import pytest
from flask import Flask
from flask.testing import FlaskClient

from services.game_service.app import create_app
from services.game_service.database.database import db
from services.game_service.database.seed import seed_test_data

ClientGenerator = Generator[FlaskClient, None, None]


@pytest.fixture(scope="session")
def app() -> Flask:
    """Create a Flask app with in-memory SQLite database."""
    app = create_app("sqlite:///:memory:")

    db.init_app(app)

    return app


@pytest.fixture
def setup_database(app: Flask):
    """Create all tables and seed them with test data, then drop them after each test."""
    with app.app_context():
        db.create_all()
        seed_test_data()
        yield
        db.drop_all()


@pytest.fixture
def client(app, setup_database):
    """
    Return a Flask test client using the 'app' fixture.

    Ensures each test has a fresh in-memory DB seeded with data.
    """
    with app.test_client() as test_client:
        yield test_client
