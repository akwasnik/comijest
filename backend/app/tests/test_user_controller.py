def test_user_create_endpoint(client):
    response = client.post("/users/create", json={
        "username": "testuser",
        "email": "test@test.com",
        "password": "123"
    })

    assert response.status_code == 201
    data = response.get_json()
    assert "id" in data


def test_user_get_all_endpoint(client):
    client.post("/users/create", json={
        "username": "kamil",
        "email": "kamil@test.com",
        "password": "abc"
    })

    response = client.get("/users/")
    assert response.status_code == 200

    data = response.get_json()
    assert len(data) == 1

def test_update_user_endpoint(client):
    create_res = client.post("/users/create", json={
        "username": "oldname",
        "email": "old@test.com",
        "password": "123"
    })
    user_id = create_res.get_json()["id"]

    update_res = client.put(f"/users/{user_id}", json={
        "username": "newname"
    })

    assert update_res.status_code == 200
    updated = update_res.get_json()
    assert updated["username"] == "newname"

def test_delete_user_endpoint(client):
    create_res = client.post("/users/create", json={
        "username": "delete_me",
        "email": "del@test.com",
        "password": "123"
    })
    user_id = create_res.get_json()["id"]

    delete_res = client.delete(f"/users/{user_id}")
    assert delete_res.status_code == 200

    get_res = client.get(f"/users/{user_id}")
    assert get_res.status_code == 404
