from werkzeug.security import check_password_hash, generate_password_hash
from auth.models import User
from extensions import db

def create_user(first_name, last_name, email, password, role="assistant"):
    u = User(first_name=first_name, last_name=last_name, email=email,
             password_hash=generate_password_hash(password), role=role)
    db.session.add(u)
    db.session.commit()
    return u

def authenticate(email, password):
    user = User.query.filter_by(email=email, is_deleted=False).first()
    if user and check_password_hash(user.password_hash, password):
        return user
    return None
