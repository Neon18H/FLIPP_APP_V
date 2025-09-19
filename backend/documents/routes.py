import mimetypes
from flask import Blueprint, request, send_file, jsonify
from flask_jwt_extended import get_jwt
from utils.auth import role_required
from documents.service import save_document, list_documents
from documents.schemas import DocumentOut
from documents.storage_provider import get_storage

bp = Blueprint("documents", __name__)
doc_out = DocumentOut()
doc_many = DocumentOut(many=True)

@bp.post("/upload")
@role_required("owner", "assistant")
def upload():
    file = request.files.get("file")
    client_id = request.form.get("client_id", type=int)
    group_key = request.form.get("group_key", default="otros")
    version  = request.form.get("version", default=1, type=int)
    if not file or client_id is None:
        return {"error": "file_and_client_id_required"}, 400
    user = get_jwt()
    d = save_document(file, client_id, group_key, uploaded_by=user["sub"], version=version)
    return doc_out.dump(d), 201

@bp.get("/")
@role_required("owner", "assistant")
def list_():
    client_id = request.args.get("client_id", type=int)
    group_key = request.args.get("group_key")
    items = list_documents(client_id, group_key)
    return jsonify(doc_many.dump(items))

@bp.get("/download/<int:doc_id>")
@role_required("owner", "assistant")
def download(doc_id):
    from documents.models import Document
    d = Document.query.get_or_404(doc_id)
    mode, target = get_storage().get_download_target(storage_path=d.storage_path, s3_key=d.s3_key)
    if mode == "local":
        mime = mimetypes.guess_type(d.filename)[0] or "application/octet-stream"
        return send_file(target, mimetype=mime, as_attachment=True, download_name=d.filename)
    return {"url": target}
