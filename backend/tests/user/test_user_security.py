import pytest
from flask_jwt_extended import create_access_token


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

def test_user_can_get_self(client, user_with_token):
    user_id, headers = user_with_token

    res = client.get(f"/api/users/{user_id}", headers=headers)
    assert res.status_code == 200


def test_user_can_update_self(client, user_with_token):
    user_id, headers = user_with_token

    res = client.put(
        f"/api/users/{user_id}",
        headers=headers,
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

def test_refresh_success(client):
    client.post("/api/users/create", json={
        "username": "refreshuser",
        "email": "refresh@test.com",
        "password": "Testpassword1!"
    })

    login = client.post("/api/users/login", json={
        "email": "refresh@test.com",
        "password": "Testpassword1!"
    }).get_json()

    refresh_token = login["refresh_token"]

    res = client.post(
        "/api/users/refresh",
        headers={"Authorization": f"Bearer {refresh_token}"}
    )

    assert res.status_code == 200
    data = res.get_json()
    assert "access_token" in data


def test_refresh_with_access_token_fails(client, user_tokens):
    res = client.post(
        "/api/users/refresh",
        headers=user_tokens["access_headers"]
    )

    assert res.status_code in (401, 422)