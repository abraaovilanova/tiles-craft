import logging
from pathlib import Path
from typing import TYPE_CHECKING
from minio import Minio
from minio.error import S3Error
import os

logger = logging.getLogger(__name__)

BUCKET_NAME = "meu-bucket"

def create_minio_client() -> Minio:
    return Minio(
        endpoint=os.getenv("MINIO_ENDPOINT", "localhost:9000"),
        access_key=os.getenv("MINIO_ACCESS_KEY", "minioadmin"),
        secret_key=os.getenv("MINIO_SECRET_KEY", "minioadmin"),
        secure=os.getenv("MINIO_SECURE", "false").lower() == "true"
    )
