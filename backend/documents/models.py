from extensions import db
from sqlalchemy import Index, Enum, UniqueConstraint
from common_models import TimestampMixin, SoftDeleteMixin

DOC_TYPE_ENUM = Enum("rut", "contrato", "factura", "otros", name="document_type")

class Document(db.Model, TimestampMixin, SoftDeleteMixin):
    __tablename__ = "documents"
    id = db.Column(db.Integer, primary_key=True)
    client_id = db.Column(db.Integer, db.ForeignKey("clients.id"), nullable=False, index=True)
    filename = db.Column(db.String(255), nullable=False)
    group_key = db.Column(db.String(100), nullable=False)
    doc_type = db.Column(DOC_TYPE_ENUM, nullable=True)
    version = db.Column(db.Integer, nullable=False, default=1)
    storage_path = db.Column(db.String(512), nullable=True)
    s3_key = db.Column(db.String(512), nullable=True)
    uploaded_by = db.Column(db.Integer, db.ForeignKey("users.id"), nullable=False, index=True)
    __table_args__ = (
        Index("ix_documents_client_version", "client_id", "group_key", "version"),
        UniqueConstraint("client_id", "group_key", "version", "filename", name="uq_doc_ver_name"),
    )
