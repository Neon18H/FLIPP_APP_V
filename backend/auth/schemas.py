from marshmallow import Schema, fields, validate

class LoginSchema(Schema):
    email = fields.Email(required=True)
    password = fields.String(required=True, validate=validate.Length(min=6))

class UserOut(Schema):
    id = fields.Int()
    first_name = fields.Str()
    last_name = fields.Str()
    email = fields.Email()
    role = fields.Str()

class RegisterSchema(Schema):
    first_name = fields.Str(required=True)
    last_name  = fields.Str(required=True)
    email      = fields.Email(required=True)
    password   = fields.String(required=True, validate=validate.Length(min=6))
    # opcional: el owner puede definir role; por seguridad, default assistant
    role       = fields.String(load_default="assistant", validate=validate.OneOf(["assistant", "owner"]))