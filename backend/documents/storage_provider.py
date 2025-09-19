from __future__ import annotations
import os, mimetypes
from dataclasses import dataclass
from typing import Optional, Literal
from flask import current_app
from werkzeug.utils import secure_filename

try:
    import boto3
    from botocore.exceptions import ClientError  # type: ignore
except Exception:
    boto3 = None
    ClientError = Exception

DownloadMode = Literal["local", "url"]

@dataclass
class SaveResult:
    filename: str
    storage_path: Optional[str] = None
    s3_key: Optional[str] = None

class StorageProvider:
    def save(self, file_storage, client_id: int, group_key: str, version: int = 1) -> SaveResult: ...
    def get_download_target(self, *, storage_path: Optional[str], s3_key: Optional[str], expires: int = 600) -> tuple[DownloadMode, str]: ...
    def exists(self, *, storage_path: Optional[str] = None, s3_key: Optional[str] = None) -> bool: ...
    def delete(self, *, storage_path: Optional[str] = None, s3_key: Optional[str] = None) -> None: ...

class LocalStorageProvider(StorageProvider):
    def __init__(self, base_dir: Optional[str] = None) -> None:
        self.base_dir = base_dir or current_app.config.get("UPLOAD_DIR", "/uploads")
        os.makedirs(self.base_dir, exist_ok=True)

    def _dir_for(self, client_id: int, group_key: str, version: int) -> str:
        return os.path.join(self.base_dir, str(client_id), group_key, f"v{version}")

    def save(self, file_storage, client_id: int, group_key: str, version: int = 1) -> SaveResult:
        filename = secure_filename(file_storage.filename or "file.bin")
        target_dir = self._dir_for(client_id, group_key, version)
        os.makedirs(target_dir, exist_ok=True)
        path = os.path.join(target_dir, filename)
        file_storage.save(path)
        return SaveResult(filename=filename, storage_path=path)

    def get_download_target(self, *, storage_path: Optional[str], s3_key: Optional[str], expires: int = 600) -> tuple[DownloadMode, str]:
        if not storage_path or not os.path.exists(storage_path):
            raise FileNotFoundError("Archivo local no encontrado.")
        return ("local", storage_path)

    def exists(self, *, storage_path: Optional[str] = None, s3_key: Optional[str] = None) -> bool:
        return bool(storage_path and os.path.exists(storage_path))

    def delete(self, *, storage_path: Optional[str] = None, s3_key: Optional[str] = None) -> None:
        if storage_path and os.path.exists(storage_path):
            try: os.remove(storage_path)
            except OSError: pass

class S3StorageProvider(StorageProvider):
    def __init__(self, bucket: Optional[str] = None, region: Optional[str] = None, prefix: Optional[str] = None) -> None:
        if boto3 is None:
            raise RuntimeError("boto3 no disponible. Usa STORAGE_PROVIDER=local.")
        self.bucket = bucket or current_app.config.get("S3_BUCKET")
        if not self.bucket:
            raise RuntimeError("S3_BUCKET no configurado.")
        self.region = region or os.getenv("AWS_DEFAULT_REGION", "us-east-1")
        self.prefix = (prefix or current_app.config.get("S3_PREFIX", "uploads")).strip("/")
        self.client = boto3.client("s3", region_name=self.region)

    def _key_for(self, client_id: int, group_key: str, version: int, filename: str) -> str:
        filename = secure_filename(filename or "file.bin")
        return f"{self.prefix}/{client_id}/{group_key}/v{version}/{filename}"

    def save(self, file_storage, client_id: int, group_key: str, version: int = 1) -> SaveResult:
        filename = secure_filename(file_storage.filename or "file.bin")
        key = self._key_for(client_id, group_key, version, filename)
        content_type = mimetypes.guess_type(filename)[0] or "application/octet-stream"
        self.client.upload_fileobj(file_storage.stream, self.bucket, key, ExtraArgs={"ContentType": content_type})
        return SaveResult(filename=filename, s3_key=key)

    def get_download_target(self, *, storage_path: Optional[str], s3_key: Optional[str], expires: int = 600) -> tuple[DownloadMode, str]:
        if not s3_key:
            raise FileNotFoundError("El documento no tiene s3_key.")
        url = self.client.generate_presigned_url("get_object", Params={"Bucket": self.bucket, "Key": s3_key}, ExpiresIn=expires)
        return ("url", url)

    def exists(self, *, storage_path: Optional[str] = None, s3_key: Optional[str] = None) -> bool:
        if not s3_key: return False
        try:
            self.client.head_object(Bucket=self.bucket, Key=s3_key)
            return True
        except Exception:
            return False

    def delete(self, *, storage_path: Optional[str] = None, s3_key: Optional[str] = None) -> None:
        if s3_key:
            try: self.client.delete_object(Bucket=self.bucket, Key=s3_key)
            except Exception: pass

def get_storage():
    provider = (current_app.config.get("STORAGE_PROVIDER") or "local").lower()
    if provider == "s3":
        return S3StorageProvider(
            bucket=current_app.config.get("S3_BUCKET"),
            region=os.getenv("AWS_DEFAULT_REGION"),
            prefix=current_app.config.get("S3_PREFIX", "uploads"),
        )
    return LocalStorageProvider(base_dir=current_app.config.get("UPLOAD_DIR", "/uploads"))
