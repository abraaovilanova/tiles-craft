from fastapi import APIRouter, HTTPException, Depends
from sqlalchemy.orm import Session
from app.config.db import get_db
from app.schema.tile import Tile as TileSchema
from app.models.tile import Tile as TileModel
from app.utils.generate_tiles import generate_tiles_with_minio
from app.storage.minio_storage import create_minio_client

router = APIRouter()

@router.post("/publish-tile")
def publish_tile(tile: TileSchema, db: Session = Depends(get_db)):
    default_file_extension = "tif"
    input_bucket = "raw-tiles"
    input_object = f'{tile.name}.{default_file_extension}'

    output_bucket = "published-tiles"
    output_prefix = tile.name

    try:
        minio_client = create_minio_client()

        if not minio_client.bucket_exists(output_bucket):
            minio_client.make_bucket(output_bucket)

        generate_tiles_with_minio(
            minio_client,
            input_bucket=input_bucket,
            input_object=input_object,
            output_bucket=output_bucket,
            output_prefix=output_prefix
        )

        # Atualizar status no banco
        db_tile = db.query(TileModel).filter(TileModel.name == tile.name).first()
        if not db_tile:
            raise HTTPException(status_code=404, detail="Tile não encontrado")

        db_tile.status = "published"
        db.commit()

        return {"status": "ok", "message": "Tiles gerados e status atualizado com sucesso!"}
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=500, detail=str(e))
