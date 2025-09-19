import os, sys
from flask import Flask, jsonify
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
if BASE_DIR not in sys.path:
    sys.path.insert(0, BASE_DIR)

from extensions import db, jwt, init_cors

from auth.routes import bp as auth_bp
from clients.routes import bp as clients_bp
from documents.routes import bp as docs_bp
from tasks.routes import bp as tasks_bp
from audit.routes import bp as audit_bp

def create_app():
    app = Flask(__name__)
    app.config.from_object("config")

    init_cors(app)
    db.init_app(app)
    jwt.init_app(app)

    app.register_blueprint(auth_bp, url_prefix="/auth")
    app.register_blueprint(clients_bp, url_prefix="/clients")
    app.register_blueprint(docs_bp, url_prefix="/documents")
    app.register_blueprint(tasks_bp, url_prefix="/tasks")
    app.register_blueprint(audit_bp, url_prefix="/audit")

    @app.get("/health")
    def health():
        return jsonify({"status": "ok", "storage": app.config.get("STORAGE_PROVIDER", "local")})

    return app

if __name__ == "__main__":
    app = create_app()
    app.run(host="0.0.0.0", port=5000)
