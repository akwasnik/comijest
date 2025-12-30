import pytest
from flask_jwt_extended import create_access_token

ROLE_PERMISSIONS = {
    "admin": {
        "user:read",
        "user:write",
        "user:delete",
        "user:list",
    },
    "user": {
        "user:read_self",
        "user:update_self",
    },
}

# =========================
# FIXTURES
# =========================

@pytest.fixture
def admin_headers():
    token = create_access_token(
        identity="admin-id",
        additional_claims={
            "role": "admin",
            "permissions": list(ROLE_PERMISSIONS["admin"])
        }
    )
    return {"Authorization": f"Bearer {token}"}


@pytest.fixture
def user_headers():
    token = create_access_token(
        identity="user-id",
        additional_claims={
            "role": "user",
            "permissions": list(ROLE_PERMISSIONS["user"])
        }
    )
    return {"Authorization": f"Bearer {token}"}


@pytest.fixture
def created_user(client):
    res = client.post("/api/users/create", json={
        "username": "testuser",
        "email": "test@test.com",
        "password": "Testpassword1!"
    })
    return res.get_json()["id"]


# =========================
# ADMIN TESTS
# =========================

def test_admin_can_list_users(client, admin_headers):
    res = client.get("/api/users/", headers=admin_headers)
    assert res.status_code == 200


def test_admin_can_get_user(client, admin_headers, created_user):
    res = client.get(f"/api/users/{created_user}", headers=admin_headers)
    assert res.status_code == 200


def test_admin_can_update_user(client, admin_headers, created_user):
    res = client.put(
        f"/api/users/{created_user}",
        headers=admin_headers,
        json={"username": "newname"}
    )
    assert res.status_code == 200


def test_admin_can_delete_user(client, admin_headers, created_user):
    res = client.delete(
        f"/api/users/{created_user}",
        headers=admin_headers
    )
    assert res.status_code == 200


# =========================
# USER TESTS (POSITIVE)
# =========================

def test_user_can_get_self(client, user_headers):
    # identity = user-id
    res = client.get("/api/users/user-id", headers=user_headers)
    assert res.status_code == 200


def test_user_can_update_self(client, user_headers):
    res = client.put(
        "/api/users/user-id",
        headers=user_headers,
        json={"username": "selfupdate"}
    )
    assert res.status_code == 200


# =========================
# USER TESTS (NEGATIVE)
# =========================

def test_user_cannot_list_users(client, user_headers):
    res = client.get("/api/users/", headers=user_headers)
    assert res.status_code == 403


def test_user_cannot_get_other_user(client, user_headers, created_user):
    res = client.get(
        f"/api/users/{created_user}",
        headers=user_headers
    )
    assert res.status_code == 403


def test_user_cannot_update_other_user(client, user_headers, created_user):
    res = client.put(
        f"/api/users/{created_user}",
        headers=user_headers,
        json={"username": "hack"}
    )
    assert res.status_code == 403


def test_user_cannot_delete_any_user(client, user_headers, created_user):
    res = client.delete(
        f"/api/users/{created_user}",
        headers=user_headers
    )
    assert res.status_code == 403


# =========================
# AUTH REQUIRED
# =========================

def test_no_token_cannot_access_protected_endpoint(client):
    res = client.get("/api/users/")
    assert res.status_code in (401, 422)
