# from flask import Blueprint
# from ..controllers.user_controllers import UserController

# user_bp = Blueprint("users", __name__)


# @user_bp.post("/create")
# def create_user():
#     return UserController.create()


# @user_bp.get("/")
# def list_users():
#     return UserController.get_all()


# @user_bp.get("/<user_id>")
# def get_user(user_id):
#     return UserController.get_one_by_id(user_id)


# @user_bp.put("/<user_id>")
# def update_user(user_id):
#     return UserController.update_user(user_id)

# @user_bp.delete("/<user_id>")
# def delete_user(user_id):
#     return UserController.delete_user(user_id)

from flask import Blueprint
from ..controllers.user_controllers import UserController

user_bp = Blueprint("users", __name__)

user_bp.post("/create")(UserController.create)
user_bp.get("/")(UserController.get_all)
user_bp.get("/<user_id>")(UserController.get_one)
user_bp.put("/<user_id>")(UserController.update)
user_bp.delete("/<user_id>")(UserController.delete)
