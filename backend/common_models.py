from sqlalchemy import func
from extensions import db

class TimestampMixin:
    created_at = db.Column(db.DateTime, nullable=False, server_default=func.now())
    updated_at = db.Column(db.DateTime, onupdate=func.now())

class SoftDeleteMixin:
    is_deleted = db.Column(db.Boolean, nullable=False, server_default=db.text("false"))
