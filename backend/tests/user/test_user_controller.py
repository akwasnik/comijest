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

def test_admin_get_all_users(client, admin_headers):
    client.post("/api/users/create", json={
        "username": "kamil",
        "email": "kamil@test.com",
        "password": "Testpassword1!"
    })

    res = client.get("/api/users/", headers=admin_headers)
    assert res.status_code == 200
    assert len(res.get_json()) == 1


def test_admin_get_single_user(client, admin_headers, created_user):
    res = client.get(
        f"/api/users/{created_user}",
        headers=admin_headers
    )

    assert res.status_code == 200
    assert res.get_json()["id"] == created_user


def test_admin_update_user(client, admin_headers, created_user):
    res = client.put(
        f"/api/users/{created_user}",
        headers=admin_headers,
        json={"username": "newname"}
    )

    assert res.status_code == 200
    assert res.get_json()["message"] is True


def test_admin_delete_user(client, admin_headers, created_user):
    res = client.delete(
        f"/api/users/{created_user}",
        headers=admin_headers
    )

    assert res.status_code == 200

    res2 = client.get(
        f"/api/users/{created_user}",
        headers=admin_headers
    )
    assert res2.status_code == 404

# =========================
# USER – SELF ACTIONS
# =========================

def test_user_get_self(client, user_with_token):
    user_id, headers = user_with_token

    res = client.get(
        f"/api/users/{user_id}",
        headers=headers
    )

    assert res.status_code == 200



def test_user_update_self(client, user_with_token):
    user_id, headers = user_with_token

    res = client.put(
        f"/api/users/{user_id}",
        headers=headers,
        json={"username": "selfupdate"}
    )

    assert res.status_code == 200


# =========================
# VALIDATION / CONFLICTS
# =========================

def test_update_user_invalid_password(client, admin_headers, created_user):
    res = client.put(
        f"/api/users/{created_user}",
        headers=admin_headers,
        json={"password": "weak"}
    )

    assert res.status_code == 400
    assert "password" in res.get_json()["errors"]


def test_update_user_username_taken(client, admin_headers):
    r1 = client.post("/api/users/create", json={
        "username": "one",
        "email": "one@test.com",
        "password": "Testpassword1!"
    })
    r2 = client.post("/api/users/create", json={
        "username": "two",
        "email": "two@test.com",
        "password": "Testpassword1!"
    })

    user_id = r1.get_json()["id"]

    res = client.put(
        f"/api/users/{user_id}",
        headers=admin_headers,
        json={"username": "two"}
    )

    assert res.status_code == 409


def test_update_user_email_taken(client, admin_headers):
    r1 = client.post("/api/users/create", json={
        "username": "one",
        "email": "one@test.com",
        "password": "Testpassword1!"
    })
    r2 = client.post("/api/users/create", json={
        "username": "two",
        "email": "two@test.com",
        "password": "Testpassword1!"
    })

    user_id = r1.get_json()["id"]

    res = client.put(
        f"/api/users/{user_id}",
        headers=admin_headers,
        json={"email": "two@test.com"}
    )

    assert res.status_code == 409

def test_logout(client):
    res = client.post("/api/users/logout")
    assert res.status_code == 200
    assert res.get_json()["msg"] == "logout"

def test_user_get_me(client, user_with_token):
    user_id, headers = user_with_token

    res = client.get(
        "/api/users/me",
        headers=headers
    )

    assert res.status_code == 200

    data = res.get_json()
    assert data["id"] == user_id
    assert "password" not in data
    assert "email" in data
    assert "username" in data

def test_user_get_me_unauthorized(client):
    res = client.get("/api/users/me")

    assert res.status_code == 401


def test_user_get_me_user_deleted(client, user_with_token, admin_headers):
    user_id, headers = user_with_token

    # admin delete user
    client.delete(
        f"/api/users/{user_id}",
        headers=admin_headers
    )

    res = client.get(
        "/api/users/me",
        headers=headers
    )

    assert res.status_code == 404


def test_user_cannot_get_other_user(client, user_with_token):
    _, headers = user_with_token

    r = client.post("/api/users/create", json={
        "username": "other",
        "email": "other@test.com",
        "password": "Testpassword1!"
    })

    other_id = r.get_json()["id"]

    res = client.get(
        f"/api/users/{other_id}",
        headers=headers
    )

    assert res.status_code == 403
