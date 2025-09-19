from extensions import db
from clients.models import Client

def create_client(data):
    c = Client(**data)
    db.session.add(c)
    db.session.commit()
    return c

def update_client(cid, data):
    c = Client.query.filter_by(id=cid, is_deleted=False).first_or_404()
    for k, v in data.items():
        setattr(c, k, v)
    db.session.commit()
    return c

def delete_client(cid):
    c = Client.query.filter_by(id=cid, is_deleted=False).first_or_404()
    c.is_deleted = True
    db.session.commit()

def get_client(cid):
    return Client.query.filter_by(id=cid, is_deleted=False).first_or_404()

def list_clients(q=None, tag=None):
    query = Client.query.filter_by(is_deleted=False)
    if q:
        query = query.filter((Client.first_name.ilike(f"%{q}%")) | (Client.last_name.ilike(f"%{q}%")) | (Client.national_id.ilike(f"%{q}%")))
    if tag:
        query = query.filter(Client.tags.contains([tag]))
    return query.order_by(Client.created_at.desc()).all()
