from flask import Blueprint, request
from flask_jwt_extended import create_access_token
from marshmallow import ValidationError
from auth.schemas import LoginSchema, UserOut
from auth.service import authenticate, create_user

bp = Blueprint("auth", __name__)
login_schema = LoginSchema()
user_out = UserOut()

@bp.post("/login")
def login():
    try:
        data = login_schema.load(request.get_json() or {})
    except ValidationError as e:
        return {"errors": e.messages}, 400
    user = authenticate(data["email"], data["password"])
    if not user:
        return {"error": "invalid_credentials"}, 401
    token = create_access_token(identity=user.id, additional_claims={"role": user.role, "email": user.email})
    return {"access_token": token, "user": user_out.dump(user)}

@bp.post("/seed-owner")
def seed_owner():
    payload = request.get_json() or {}
    u = create_user(payload.get("first_name","Sara"), payload.get("last_name","Owner"),
                    payload.get("email","owner@example.com"), payload.get("password","owner123"), role="owner")
    return {"user": user_out.dump(u)}, 201
