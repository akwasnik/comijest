import pytest
import mongomock
from flask_jwt_extended import create_access_token
from app import create_app

ROLE_PERMISSIONS = {
    "admin": {
        "user:read",
        "user:update"
        "user:delete",
        "user:list",
    },
    "user": {
        "user:read_self",
        "user:update_self",
    },
}


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


@pytest.fixture
def admin_headers(app):
    token = create_access_token(
        identity="admin-id",
        additional_claims={
            "role": "admin",
            "permissions": list(ROLE_PERMISSIONS["admin"]),
        },
    )
    return {"Authorization": f"Bearer {token}"}


@pytest.fixture
def user_headers(app):
    token = create_access_token(
        identity="user-id",
        additional_claims={
            "role": "user",
            "permissions": list(ROLE_PERMISSIONS["user"]),
        },
    )
    return {"Authorization": f"Bearer {token}"}


@pytest.fixture
def created_user(client):
    res = client.post(
        "/api/users/create",
        json={
            "username": "testuser",
            "email": "test@test.com",
            "password": "Testpassword1!",
        },
    )
    return res.get_json()["id"]

@pytest.fixture
def user_with_token(client):
    res = client.post("/api/users/create", json={
        "username": "normaluser",
        "email": "user@test.com",
        "password": "Testpassword1!"
    })
    user_id = res.get_json()["id"]

    token = create_access_token(
        identity=user_id,
        additional_claims={
            "role": "user",
            "permissions": ["user:read_self", "user:update_self"]
        }
    )

    headers = {"Authorization": f"Bearer {token}"}
    return user_id, headers