def test_login_success_sets_cookies(client):
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

    cookies = res.headers.getlist("Set-Cookie")

    assert any("access_token_cookie=" in c for c in cookies)

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

    cookies = res.headers.getlist("Set-Cookie")
    assert cookies == []  # no cookies if error

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


def test_login_cookie_allows_access(client):
    client.post("/api/users/create", json={
        "username": "loginuser",
        "email": "login@test.com",
        "password": "Testpassword1!"
    })

    client.post("/api/users/login", json={
        "email": "login@test.com",
        "password": "Testpassword1!"
    })

    res = client.get("/api/users/me")
    assert res.status_code == 200
