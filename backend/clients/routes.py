from flask import Blueprint, request, jsonify
from marshmallow import ValidationError
from utils.auth import role_required
from clients.schemas import ClientIn, ClientOut
from clients.service import create_client, update_client, delete_client, get_client, list_clients

bp = Blueprint("clients", __name__)
cin, cout, cout_many = ClientIn(), ClientOut(), ClientOut(many=True)

@bp.get("/")
@role_required("owner", "assistant")
def list_():
    q = request.args.get("q")
    tag = request.args.get("tag")
    items = list_clients(q=q, tag=tag)
    return jsonify(cout_many.dump(items))

@bp.get("/<int:cid>")
@role_required("owner", "assistant")
def retrieve(cid):
    c = get_client(cid)
    return cout.dump(c)

@bp.post("/")
@role_required("owner")
def create():
    try:
        data = cin.load(request.get_json() or {})
    except ValidationError as e:
        return {"errors": e.messages}, 400
    c = create_client(data)
    return cout.dump(c), 201

@bp.put("/<int:cid>")
@role_required("owner")
def update(cid):
    try:
        data = cin.load(request.get_json() or {})
    except ValidationError as e:
        return {"errors": e.messages}, 400
    c = update_client(cid, data)
    return cout.dump(c)

@bp.delete("/<int:cid>")
@role_required("owner")
def delete(cid):
    delete_client(cid)
    return {}, 204
