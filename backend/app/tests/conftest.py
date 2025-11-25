import pytest
import mongomock
from app import create_app

@pytest.fixture
def app():
    app = create_app()

    app.mongo = mongomock.MongoClient().db_for_tests

    yield app


@pytest.fixture
def client(app):
    return app.test_client()
