from flask_jwt_extended import decode_token


def test_login_success(client):
    client.post("/api/users/create", json={
        "username": "loginuser",
        "email": "login@test.com",
        "password": "Testpassword1!"
    })

    res = client.post("/api/users/login", json={
        "email": "login@test.com",
        "password": "Testpassword1!"
    })

    assert res.status_code == 200

    data = res.get_json()
    assert "access_token" in data
    assert "refresh_token" in data


def test_login_invalid_password(client):
    client.post("/api/users/create", json={
        "username": "loginuser",
        "email": "login@test.com",
        "password": "Testpassword1!"
    })

    res = client.post("/api/users/login", json={
        "email": "login@test.com",
        "password": "WrongPassword1!"
    })

    assert res.status_code == 401


def test_login_rate_limit(client):
    client.post("/api/users/create", json={
        "username": "loginuser",
        "email": "login@test.com",
        "password": "Testpassword1!"
    })

    for _ in range(5):
        client.post("/api/users/login", json={
            "email": "login@test.com",
            "password": "WrongPassword1!"
        })

    res = client.post("/api/users/login", json={
        "email": "login@test.com",
        "password": "WrongPassword1!"
    })

    assert res.status_code == 429
