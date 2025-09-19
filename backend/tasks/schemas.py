from marshmallow import Schema, fields, validate

class TaskIn(Schema):
    client_id = fields.Int(required=True)
    title = fields.Str(required=True)
    description = fields.Str(load_default=None, allow_none=True)
    priority = fields.Str(load_default="medium", validate=validate.OneOf(["low","medium","high"]))
    due_date = fields.Date(load_default=None, allow_none=True)
    assignee_id = fields.Int(load_default=None, allow_none=True)

class TaskOut(TaskIn):
    id = fields.Int()
    status = fields.Str()
    created_by = fields.Int()
    created_at = fields.DateTime()
    updated_at = fields.DateTime()

class TaskStatusIn(Schema):
    status = fields.Str(required=True, validate=validate.OneOf(["todo","doing","done"]))

class CommentIn(Schema):
    content = fields.Str(required=True)

class CommentOut(Schema):
    id = fields.Int()
    task_id = fields.Int()
    author_id = fields.Int()
    content = fields.Str()
    created_at = fields.DateTime()
