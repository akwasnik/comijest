from flask import Blueprint
from flask_jwt_extended import jwt_required
from ..security.authorization import permission_required
from ..controllers.user_controllers import UserController
from ..extensions import limiter
user_bp = Blueprint("users", __name__)

user_bp.post("/create", endpoint="create_user")((UserController.create))

user_bp.get("/", endpoint="get_users")(
    permission_required("user:list")(UserController.get_all)
)

user_bp.get(
    "/<user_id>", 
    endpoint="get_user"
)(
    permission_required("user:read")(
    jwt_required()(UserController.get_one))
)

user_bp.put(
    "/<user_id>", 
    endpoint="update_user"
)(
    permission_required("user:update")(
    jwt_required()(UserController.update)
    )
)
user_bp.delete(
    "/<user_id>",
    endpoint="delete_user"
)(
    permission_required("user:delete")(
        jwt_required()(UserController.delete)
    )
)


user_bp.post(
    "/login",
    endpoint="login"
)(
    limiter.limit("5 per minute")(UserController.login)
)

user_bp.post(
    "/refresh",
    endpoint="refresh"
)(
    limiter.limit("10 per minute")(
        jwt_required(refresh=True)(UserController.refresh)
    )
)

user_bp.post("/logout", endpoint='logout')(UserController.logout)
