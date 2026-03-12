from flask_jwt_extended import create_access_token
import pytest
from app.services.user_services import UserService
from werkzeug.security import check_password_hash
from werkzeug.security import check_password_hash
from app.exceptions.user_exceptions import (
    UsernameTakenError, EmailTakenError, SamePasswordError
)

def test_jwt_works(app):
    token = create_access_token(identity="test")
    assert token is not None
    
def test_create_user(app):
    user = UserService.create_user("adam", "adam@test.com", "pass123")
    assert user is not None
    assert user.email == "adam@test.com"


def test_create_user_duplicate(app):
    UserService.create_user("adam", "adam@test.com", "pass123")
    with pytest.raises(EmailTakenError):
        UserService.create_user("adam2", "adam@test.com", "pass123")


def test_update_username_service(app):
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

def test_update_user_password_service(app):
    user = UserService.create_user("anna", "anna@test.com", "pass123")
    user_id = user.id

    updated = UserService.update_user(
        user_id,
        {"password": "pass12"}
    )

    assert updated is True
    assert check_password_hash(UserService.get_user_by_id(user_id).password, "pass12") is True


def test_update_user_same_password_service(app):
    user = UserService.create_user("anna", "anna@test.com", "pass123")
    user_id = user.id

    with pytest.raises(SamePasswordError):
        UserService.update_user(
            user_id,
            {"password": "pass123"}
        )

    # password shouldn't change
    assert check_password_hash(UserService.get_user_by_id(user_id).password, "pass123") is True


def test_update_user_username_is_taken_service(app):
    user1 = UserService.create_user("anna", "anna@test.com", "pass123")
    user2 = UserService.create_user("panna", "panna@test.com", "pass123")
    user2_id = user2.id

    with pytest.raises(UsernameTakenError):
        UserService.update_user(
            user2_id,
            {"username": "anna"}
        )

    # username unchanged
    assert UserService.get_user_by_id(user2_id).username == "panna"


def test_update_user_email_is_taken_service(app):
    user1 = UserService.create_user("anna", "anna@test.com", "pass123")
    user2 = UserService.create_user("panna", "panna@test.com", "pass123")
    user2_id = user2.id

    with pytest.raises(EmailTakenError):
        UserService.update_user(
            user2_id,
            {"email": "anna@test.com"}
        )

    # email unchanged
    assert UserService.get_user_by_id(user2_id).email == "panna@test.com"


def test_update_user_multiple_fields_service(app):
    user = UserService.create_user("anna", "anna@test.com", "pass123")
    user_id = user.id

    updated = UserService.update_user(
        user_id,
        {
            "email": "panna@test.com",
            "username": "panna",
            "password": "pass1234"
        }
    )

    assert updated is True
    assert UserService.get_user_by_id(user_id).email == "panna@test.com"
    assert UserService.get_user_by_id(user_id).username == "panna"
    assert check_password_hash(UserService.get_user_by_id(user_id).password, "pass1234") is True
