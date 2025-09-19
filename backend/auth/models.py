from extensions import db
from sqlalchemy import Enum, Index
from common_models import TimestampMixin, SoftDeleteMixin

ROLE_ENUM = Enum("owner", "assistant", name="user_role")

class User(db.Model, TimestampMixin, SoftDeleteMixin):
    __tablename__ = "users"
    id = db.Column(db.Integer, primary_key=True)
    first_name = db.Column(db.String(80), nullable=False)
    last_name  = db.Column(db.String(80), nullable=False)
    email      = db.Column(db.String(255), unique=True, index=True, nullable=False)
    password_hash = db.Column(db.String(255), nullable=False)
    role = db.Column(ROLE_ENUM, nullable=False, server_default="assistant")
    __table_args__ = (Index("ix_users_role", "role"),)
