from flask import Blueprint
from flask_jwt_extended import jwt_required

from ..utils.is_admin import admin_required
from ..controllers.user_controllers import UserController

user_bp = Blueprint("users", __name__)

user_bp.post("/create", endpoint="create_user")(
    admin_required()(UserController.create)
)

user_bp.get("/", endpoint="get_users")(
    admin_required()(UserController.get_all)
)

user_bp.get("/<user_id>", endpoint="get_user")(
    jwt_required()(UserController.get_one)
)

user_bp.put("/<user_id>", endpoint="update_user")(
    admin_required()(UserController.update)
)

user_bp.delete("/<user_id>", endpoint="delete_user")(
    admin_required()(UserController.delete)
)

user_bp.post("/login", endpoint="login")(
    UserController.login
)

user_bp.post("/refresh", endpoint="refresh")(
    jwt_required(refresh=True)(UserController.refresh)
)

user_bp.post("/logout", endpoint='logout')(UserController.logout)
