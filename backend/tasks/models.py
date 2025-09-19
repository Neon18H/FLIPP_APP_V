from extensions import db
from sqlalchemy import Enum, Index
from common_models import TimestampMixin, SoftDeleteMixin

TASK_STATUS = Enum("todo", "doing", "done", name="task_status")
TASK_PRIORITY = Enum("low", "medium", "high", name="task_priority")

class Task(db.Model, TimestampMixin, SoftDeleteMixin):
    __tablename__ = "tasks"
    id = db.Column(db.Integer, primary_key=True)
    client_id = db.Column(db.Integer, db.ForeignKey("clients.id"), nullable=False, index=True)
    title = db.Column(db.String(200), nullable=False)
    description = db.Column(db.Text)
    status = db.Column(TASK_STATUS, nullable=False, server_default="todo")
    priority = db.Column(TASK_PRIORITY, nullable=False, server_default="medium")
    due_date = db.Column(db.Date)
    assignee_id = db.Column(db.Integer, db.ForeignKey("users.id"), index=True)
    created_by = db.Column(db.Integer, db.ForeignKey("users.id"), nullable=False, index=True)
    __table_args__ = (Index("ix_tasks_status_assignee", "status", "assignee_id"),)

class TaskComment(db.Model, TimestampMixin, SoftDeleteMixin):
    __tablename__ = "task_comments"
    id = db.Column(db.Integer, primary_key=True)
    task_id = db.Column(db.Integer, db.ForeignKey("tasks.id"), nullable=False, index=True)
    author_id = db.Column(db.Integer, db.ForeignKey("users.id"), nullable=False, index=True)
    content = db.Column(db.Text, nullable=False)
