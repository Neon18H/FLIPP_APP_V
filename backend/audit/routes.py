from flask import Blueprint, jsonify
from utils.auth import role_required
from audit.service import timeline_for_client

bp = Blueprint("audit", __name__)

@bp.get("/client/<int:cid>/timeline")
@role_required("owner", "assistant")
def timeline(cid):
    logs = timeline_for_client(cid)
    return jsonify([{
        "id": l.id, "client_id": l.client_id, "action": l.action,
        "detail": l.detail, "created_at": l.created_at.isoformat() if l.created_at else None
    } for l in logs])
