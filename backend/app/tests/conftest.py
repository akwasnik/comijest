import pytest
import mongomock
from ..app import create_app

@pytest.fixture
def app():
    app = create_app()

    app.mongo = mongomock.MongoClient().db_for_tests
    ctx = app.app_context()
    ctx.push()

    yield app  # <-- testy działają tutaj

    # Po testach zamykamy kontekst
    ctx.pop()
@pytest.fixture
def client(app):
    return app.test_client()
