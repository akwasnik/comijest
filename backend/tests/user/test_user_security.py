# =========================
# ADMIN TESTS
# =========================

def test_admin_can_list_users(admin_client):
    res = admin_client.get("/api/users/")
    assert res.status_code == 200


def test_admin_can_get_user(admin_client, client):
    r = client.post("/api/users/create", json={
        "username": "test",
        "email": "test@test.com",
        "password": "Testpassword1!"
    })
    user_id = r.get_json()["id"]

    res = admin_client.get(f"/api/users/{user_id}")
    assert res.status_code == 200


def test_admin_can_update_user(admin_client, client):
    r = client.post("/api/users/create", json={
        "username": "edit",
        "email": "edit@test.com",
        "password": "Testpassword1!"
    })
    user_id = r.get_json()["id"]

    res = admin_client.put(
        f"/api/users/{user_id}",
        json={"username": "newname"}
    )
    assert res.status_code == 200


def test_admin_can_delete_user(admin_client, client):
    r = client.post("/api/users/create", json={
        "username": "del",
        "email": "del@test.com",
        "password": "Testpassword1!"
    })
    user_id = r.get_json()["id"]

    res = admin_client.delete(f"/api/users/{user_id}")
    assert res.status_code == 200


# =========================
# USER TESTS (POSITIVE)
# =========================

def test_user_can_get_me(user_client):
    res = user_client.get("/api/users/me")
    assert res.status_code == 200


def test_user_can_update_self(user_client):
    res = user_client.put(
        "/api/users/me",
        json={"username": "selfupdate"}
    )
    assert res.status_code == 200


# =========================
# USER TESTS (NEGATIVE)
# =========================

def test_user_cannot_list_users(user_client):
    res = user_client.get("/api/users/")
    assert res.status_code == 403


def test_user_cannot_get_other_user(user_client, client):
    r = client.post("/api/users/create", json={
        "username": "other",
        "email": "other@test.com",
        "password": "Testpassword1!"
    })
    other_id = r.get_json()["id"]

    res = user_client.get(f"/api/users/{other_id}")
    assert res.status_code == 403


def test_user_cannot_update_other_user(user_client, client):
    r = client.post("/api/users/create", json={
        "username": "other2",
        "email": "other2@test.com",
        "password": "Testpassword1!"
    })
    other_id = r.get_json()["id"]

    res = user_client.put(
        f"/api/users/{other_id}",
        json={"username": "hack"}
    )
    assert res.status_code == 403


def test_user_cannot_delete_any_user(user_client, client):
    r = client.post("/api/users/create", json={
        "username": "other3",
        "email": "other3@test.com",
        "password": "Testpassword1!"
    })
    other_id = r.get_json()["id"]

    res = user_client.delete(f"/api/users/{other_id}")
    assert res.status_code == 403


# =========================
# AUTH REQUIRED
# =========================

def test_no_cookie_cannot_access_protected_endpoint(client):
    res = client.get("/api/users/")
    assert res.status_code in (401, 422)


# =========================
# REFRESH TOKEN
# =========================

def test_refresh_success(user_client):
    res = user_client.post("/api/users/refresh")
    assert res.status_code == 200


def test_refresh_with_access_cookie_fails(user_client):
    user_client.delete_cookie("refresh_token")

    res = user_client.post("/api/users/refresh")

    assert res.status_code in (401, 422)
