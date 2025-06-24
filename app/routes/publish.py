from fastapi import APIRouter, HTTPException
import os
from minio import Minio
from app.utils.generate_tiles import generate_tiles_with_minio  # ou caminho correto
from app.storage.minio_storage import create_minio_client

router = APIRouter()
@router.post("/publish-tile")
def publish_tile():
    # Parâmetros para a função
    input_bucket = "raster-bucket"
    input_object = "mde_29082se_v1.tif"

    output_bucket = "tiles-bucket"
    output_prefix = "tiles/meu_raster"
    try:
        minio_client = create_minio_client()
        generate_tiles_with_minio(
          minio_client, input_bucket=input_bucket,
          input_object=input_object,
          output_bucket=output_bucket,
          output_prefix=output_prefix
        )
        return {"status": "ok", "message": "Tiles gerados com sucesso!"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))