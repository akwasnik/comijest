import re
from marshmallow import Schema, fields, ValidationError, validate

SPECIAL_CHARS = r"!@#$^&*()_\-+=\[\]{};:,.?/"

def validate_password(pw):
    if pw is None:
        raise ValidationError("Password is required")

    if not isinstance(pw, str):
        raise ValidationError("Password must be a string")

    errors = []

    if len(pw) < 12:
        errors.append("Password must be at least 12 characters long")
    if not re.search(r"[A-Z]", pw):
        errors.append("Password must contain at least 1 uppercase letter")
    if not re.search(r"[a-z]", pw):
        errors.append("Password must contain at least 1 lowercase letter")
    if not re.search(r"\d", pw):
        errors.append("Password must contain at least 1 digit")
    if not re.search(rf"[{re.escape(SPECIAL_CHARS)}]", pw):
        errors.append("Password must contain at least 1 special character")
    if re.search(r"\s", pw):
        errors.append("Password cannot contain whitespace")

    if errors:
        raise ValidationError(errors)

class UserSchema(Schema):
    email = fields.Email(required=True)
    username = fields.String(required=True, validate=validate.Length(min=3, error="Username too short"))
    password = fields.String(required=True, validate=validate_password)

class UpdateUserSchema(Schema):
    email = fields.Email()
    username = fields.String(validate=validate.Length(min=3, error="Username too short"))
    password = fields.String(validate=validate_password)