import os
SQLALCHEMY_DATABASE_URI = os.getenv("DATABASE_URL", "postgresql://app:app@db:5432/appdb")
SQLALCHEMY_TRACK_MODIFICATIONS = False
JWT_SECRET_KEY = os.getenv("JWT_SECRET_KEY", "devsecret")
PROPAGATE_EXCEPTIONS = True
STORAGE_PROVIDER = os.getenv("STORAGE_PROVIDER", "local")  # local | s3
UPLOAD_DIR = os.getenv("UPLOAD_DIR", "/uploads")
MAX_CONTENT_LENGTH = 50 * 1024 * 1024
ALLOWED_MIME_TYPES = {"application/pdf", "image/jpeg", "image/png"}
