# =========================
# CREATE (PUBLIC)
# =========================

def test_user_create_endpoint(client):
    res = client.post("/api/users/create", json={
        "username": "testuser",
        "email": "test@test.com",
        "password": "Testpassword1!"
    })

    assert res.status_code == 201
    assert "id" in res.get_json()


def test_user_create_duplicate_email(client):
    client.post("/api/users/create", json={
        "username": "user1",
        "email": "dup@test.com",
        "password": "Testpassword1!"
    })

    res = client.post("/api/users/create", json={
        "username": "user2",
        "email": "dup@test.com",
        "password": "Testpassword1!"
    })

    assert res.status_code == 409


def test_user_create_invalid_password(client):
    res = client.post("/api/users/create", json={
        "username": "user",
        "email": "bad@test.com",
        "password": "weak"
    })

    assert res.status_code == 400
    assert "password" in res.get_json()["errors"]


# =========================
# ADMIN – CONTROLLER LOGIC
# =========================

def test_admin_get_all_users(admin_client):
    admin_client.post("/api/users/create", json={
        "username": "kamil",
        "email": "kamil@test.com",
        "password": "Testpassword1!"
    })

    res = admin_client.get("/api/users/")
    assert res.status_code == 200
    assert len(res.get_json()) >= 1


def test_admin_get_single_user(admin_client, client):
    r = client.post("/api/users/create", json={
        "username": "test",
        "email": "one@test.com",
        "password": "Testpassword1!"
    })
    user_id = r.get_json()["id"]

    res = admin_client.get(f"/api/users/{user_id}")
    assert res.status_code == 200
    assert res.get_json()["id"] == user_id


def test_admin_update_user(admin_client, client):
    r = client.post("/api/users/create", json={
        "username": "toedit",
        "email": "edit@test.com",
        "password": "Testpassword1!"
    })
    user_id = r.get_json()["id"]

    res = admin_client.put(
        f"/api/users/{user_id}",
        json={"username": "newname"}
    )

    assert res.status_code == 200


def test_admin_delete_user(admin_client, client):
    r = client.post("/api/users/create", json={
        "username": "todelete",
        "email": "del@test.com",
        "password": "Testpassword1!"
    })
    user_id = r.get_json()["id"]

    res = admin_client.delete(f"/api/users/{user_id}")
    assert res.status_code == 200

    res2 = admin_client.get(f"/api/users/{user_id}")
    assert res2.status_code == 404


# =========================
# USER – SELF ACTIONS
# =========================

def test_user_get_me(user_client):
    res = user_client.get("/api/users/me")
    assert res.status_code == 200
    assert "password" not in res.get_json()


def test_user_cannot_get_other_user(user_client, client):
    r = client.post("/api/users/create", json={
        "username": "other",
        "email": "other@test.com",
        "password": "Testpassword1!"
    })
    other_id = r.get_json()["id"]

    res = user_client.get(f"/api/users/{other_id}")
    assert res.status_code == 403


# =========================
# LOGOUT / AUTH
# =========================

def test_logout(user_client):
    res = user_client.post("/api/users/logout")
    assert res.status_code == 200
    assert res.get_json()["msg"] == "logout"

    # cookie cleared → auth required
    res2 = user_client.get("/api/users/me")
    assert res2.status_code == 401
