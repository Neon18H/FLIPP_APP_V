from marshmallow import Schema, fields, validate

class ClientIn(Schema):
    first_name = fields.Str(required=True)
    last_name = fields.Str(required=True)
    national_id = fields.Str(required=True)
    email = fields.Email(load_default=None, allow_none=True)
    phone = fields.Str(load_default=None, allow_none=True)
    tags = fields.List(fields.Str(), load_default=[])

class ClientOut(ClientIn):
    id = fields.Int()
