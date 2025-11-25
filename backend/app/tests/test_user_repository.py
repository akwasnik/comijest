from ..repositories.user_repository import UserRepository
from ..models.user import User


def test_create_and_find_user(app):
    user = User("john", "john@test.com", "hashed_password")

    inserted_id = UserRepository.create(user)
    assert inserted_id is not None

    found = UserRepository.find_by_id(inserted_id)
    assert found is not None
    assert found.username == "john"
    assert found.email == "john@test.com"


def test_update_user(app):
    user = User("john", "john@test.com", "pass123")
    user_id = UserRepository.create(user)

    update_data = {"username": "johnny"}

    updated = UserRepository.update(user_id, update_data)
    assert updated is True

    result = UserRepository.find_by_id(user_id)
    assert result.username == "johnny"

def test_delete_user(app):
    user = User("mark", "mark@test.com", "pass123")
    user_id = UserRepository.create(user)

    deleted = UserRepository.delete(user_id)
    assert deleted is True

    result = UserRepository.find_by_id(user_id)
    assert result is None
