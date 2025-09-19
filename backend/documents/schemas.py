from marshmallow import Schema, fields

class DocumentOut(Schema):
    id = fields.Int()
    client_id = fields.Int()
    filename = fields.Str()
    group_key = fields.Str()
    doc_type = fields.Str(allow_none=True)
    version = fields.Int()
    storage_path = fields.Str(allow_none=True)
    s3_key = fields.Str(allow_none=True)
    uploaded_by = fields.Int()
    created_at = fields.DateTime()
