from marshmallow import Schema, fields, validate

class UserSchema(Schema):
    email = fields.Email(required=True)
    username = fields.String(required=True, validate=validate.Length(min=3))
    password = fields.String(required=True, validate=[
        validate.Length(min=12, error="Password must be at lest 12 character long"),
        validate.Regexp(r'[A-Z]', error="Password must contain at lest 1 uppercase letter"),
        # validate.Regexp(r'[0-9]', error="Password must contain at lest 1 number")
    ])
