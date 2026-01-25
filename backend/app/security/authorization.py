from functools import wraps
from flask import jsonify
from flask_jwt_extended import (
    verify_jwt_in_request,
    get_jwt,
    get_jwt_identity,
)
from .persmission import ROLE_PERMISSIONS


def has_permission(permission):
    claims = get_jwt()
    role = claims.get("role")
    return permission in ROLE_PERMISSIONS.get(role, set())


def has_any_permission(permissions):
    claims = get_jwt()
    role = claims.get("role")
    role_permissions = ROLE_PERMISSIONS.get(role, set())
    return any(p in role_permissions for p in permissions)


def permission_required_any(permissions):
    def wrapper(fn):
        @wraps(fn)
        def inner(*args, **kwargs):
            verify_jwt_in_request()

            if not has_any_permission(permissions):
                return jsonify({"msg": "forbidden"}), 403
            return fn(*args, **kwargs)
        return inner
    return wrapper


def permission_required(permission):
    def wrapper(fn):
        @wraps(fn)
        def inner(*args, **kwargs):
            verify_jwt_in_request()

            if not has_permission(permission):
                return jsonify({"msg": "forbidden"}), 403
            return fn(*args, **kwargs)
        return inner
    return wrapper


def can_access_user(target_user_id):
    verify_jwt_in_request()

    claims = get_jwt()
    role = claims.get("role")
    identity = get_jwt_identity()

    return role == "admin" or identity == target_user_id
