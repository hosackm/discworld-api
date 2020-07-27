import os
import tempfile
import pytest
from discworld import create_app


@pytest.fixture
def app():
    config = {
        "AUTH0_DOMAIN": "test_auth0_domain",
        "AUTH0_AUDIENCE": "test_auth0_audience",
        "AUTH0_CLIENT_ID": "test_auth0_client_id",
        "AUTH0_CLIENT_SECRET": "test_auth0_client_secret",
        "AUTH0_CALLBACK_URI": "test_auth0_callback_uri",
        "DATABASE_URI": "sqlite:///test-database.db",
        "TESTING": True
    }

    app = create_app(testing_config=config)
    app.config["db"].create_all()

    yield app

    app.config["db"].drop_all()
    with app.app_context():
        app.cache.clear()


@pytest.fixture
def client(app):
    yield app.test_client()
