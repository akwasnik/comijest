import pytest
import mongomock
from app import create_app
from werkzeug.security import generate_password_hash


@pytest.fixture
def app():
    app = create_app(testing=True)
    app.mongo = mongomock.MongoClient().db_for_tests

    ctx = app.app_context()
    ctx.push()
    yield app
    ctx.pop()


@pytest.fixture
def client(app):
    return app.test_client()


# ---------- USER CLIENT (cookies) ----------

@pytest.fixture
def user_client(client):
    client.post("/api/users/create", json={
        "username": "normaluser",
        "email": "user@test.com",
        "password": "Testpassword1!"
    })

    res = client.post("/api/users/login", json={
        "email": "user@test.com",
        "password": "Testpassword1!"
    })

    assert res.status_code == 200
    return client


# ---------- ADMIN CLIENT (cookies) ----------

@pytest.fixture
def admin_client(client):
    # insert admin directly
    client.application.mongo.users.insert_one({
        "username": "admin",
        "email": "admin@test.com",
        "password": generate_password_hash("Adminpassword1!"),
        "role": "admin"
    })

    res = client.post("/api/users/login", json={
        "email": "admin@test.com",
        "password": "Adminpassword1!"
    })

    assert res.status_code == 200
    return client
