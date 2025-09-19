from extensions import db
from audit.models import ActivityLog

def log(actor_id, action, client_id=None, detail=None):
    entry = ActivityLog(actor_id=actor_id, action=action, client_id=client_id, detail=detail or {})
    db.session.add(entry); db.session.commit(); return entry

def timeline_for_client(client_id, limit=200):
    return ActivityLog.query.filter_by(client_id=client_id).order_by(ActivityLog.created_at.desc()).limit(limit).all()
