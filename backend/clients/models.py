from extensions import db
from sqlalchemy import Index
from common_models import TimestampMixin, SoftDeleteMixin

class Client(db.Model, TimestampMixin, SoftDeleteMixin):
    __tablename__ = "clients"
    id = db.Column(db.Integer, primary_key=True)
    first_name = db.Column(db.String(120), nullable=False)
    last_name  = db.Column(db.String(120), nullable=False)
    national_id = db.Column(db.String(50), index=True, nullable=False)
    email = db.Column(db.String(255))
    phone = db.Column(db.String(50))
    tags = db.Column(db.ARRAY(db.String), server_default="{}")
    __table_args__ = (Index("ix_clients_name", "first_name", "last_name"),)
