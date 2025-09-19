from extensions import db
from documents.models import Document
from documents.storage_provider import get_storage

def save_document(file_storage, client_id, group_key, uploaded_by, version=1):
    sp = get_storage()
    res = sp.save(file_storage, client_id, group_key, version)
    d = Document(
        client_id=client_id,
        filename=res.filename,
        group_key=group_key,
        version=version,
        storage_path=res.storage_path,
        s3_key=res.s3_key,
        uploaded_by=uploaded_by,
    )
    db.session.add(d)
    db.session.commit()
    return d

def list_documents(client_id=None, group_key=None):
    from documents.models import Document
    q = Document.query.filter_by(is_deleted=False)
    if client_id: q = q.filter_by(client_id=client_id)
    if group_key: q = q.filter_by(group_key=group_key)
    return q.order_by(Document.created_at.desc()).all()
