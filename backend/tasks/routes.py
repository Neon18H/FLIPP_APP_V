from flask import Blueprint, request, jsonify
from flask_jwt_extended import get_jwt
from marshmallow import ValidationError
from utils.auth import role_required
from tasks.schemas import TaskIn, TaskOut, TaskStatusIn, CommentIn, CommentOut
from tasks.service import create_task, update_task, delete_task, list_tasks, get_task, change_status, add_comment, list_comments

bp = Blueprint("tasks", __name__)
t_in, t_out, t_many = TaskIn(), TaskOut(), TaskOut(many=True)
st_in = TaskStatusIn()
c_in, c_out, c_many = CommentIn(), CommentOut(), CommentOut(many=True)

@bp.get("/")
@role_required("owner", "assistant")
def list_():
    client_id = request.args.get("client_id", type=int)
    status = request.args.get("status")
    assignee_id = request.args.get("assigneeId")  # "me" o id
    q = request.args.get("q")
    items = list_tasks(client_id, assignee_id, status, q)
    return jsonify(t_many.dump(items))

@bp.get("/<int:tid>")
@role_required("owner", "assistant")
def retrieve(tid):
    return t_out.dump(get_task(tid))

@bp.post("/")
@role_required("owner")
def create():
    try:
        data = t_in.load(request.get_json() or {})
    except ValidationError as e:
        return {"errors": e.messages}, 400
    user = get_jwt()
    t = create_task(data, creator_id=user["sub"])
    return t_out.dump(t), 201

@bp.put("/<int:tid>")
@role_required("owner")
def update(tid):
    try:
        data = t_in.load(request.get_json() or {})
    except ValidationError as e:
        return {"errors": e.messages}, 400
    t = update_task(tid, data); return t_out.dump(t)

@bp.patch("/<int:tid>/status")
@role_required("owner", "assistant")
def status(tid):
    try:
        data = st_in.load(request.get_json() or {})
    except ValidationError as e:
        return {"errors": e.messages}, 400
    t = change_status(tid, data["status"]); return t_out.dump(t)

@bp.delete("/<int:tid>")
@role_required("owner")
def delete(tid):
    delete_task(tid); return {}, 204

@bp.get("/<int:tid>/comments")
@role_required("owner", "assistant")
def comments_list(tid):
    return jsonify(c_many.dump(list_comments(tid)))

@bp.post("/<int:tid>/comments")
@role_required("owner", "assistant")
def comments_add(tid):
    try:
        data = c_in.load(request.get_json() or {})
    except ValidationError as e:
        return {"errors": e.messages}, 400
    user = get_jwt()
    c = add_comment(tid, user["sub"], data["content"])
    return c_out.dump(c), 201
