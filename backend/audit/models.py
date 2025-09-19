from extensions import db
from sqlalchemy import Index, Enum
from common_models import TimestampMixin

ACTION_ENUM = Enum(
    "CLIENT_CREATE","CLIENT_UPDATE","CLIENT_DELETE",
    "DOC_UPLOAD","DOC_DELETE","DOC_VERSION",
    "TASK_CREATE","TASK_ASSIGN","TASK_STATUS_CHANGE","TASK_COMMENT",
    name="activity_action"
)

class ActivityLog(db.Model, TimestampMixin):
    __tablename__ = "activity_logs"
    id = db.Column(db.Integer, primary_key=True)
    actor_id = db.Column(db.Integer, db.ForeignKey("users.id"), nullable=False, index=True)
    client_id = db.Column(db.Integer, db.ForeignKey("clients.id"), nullable=True, index=True)
    action = db.Column(ACTION_ENUM, nullable=False)
    detail = db.Column(db.JSON, nullable=True)
    __table_args__ = (Index("ix_activitylogs_client_time", "client_id", "created_at"),)
