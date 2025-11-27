from ...services.user_services import UserService

def test_create_user(app):
    user = UserService.create_user("adam", "adam@test.com", "pass123")
    assert user is not None
    assert user.email == "adam@test.com"


def test_create_user_duplicate(app):
    UserService.create_user("adam", "adam@test.com", "pass123")
    duplicate = UserService.create_user("adam", "adam@test.com", "pass123")
    assert duplicate is None


def test_update_user_service(app):
    user = UserService.create_user("anna", "anna@test.com", "pass123")
    user_id = user.id

    updated = UserService.update_user(
        user_id,
        {"username": "ania"}
    )

    assert updated is True
    assert UserService.get_user_by_id(user_id).username == "ania"

def test_delete_user_service(app):
    user = UserService.create_user("ola", "ola@test.com", "pass123")
    user_id = user.id

    deleted = UserService.delete_user(user_id)
    assert deleted is True

    # ensure removed
    fetched = UserService.get_user_by_id(user_id)
    assert fetched is None
