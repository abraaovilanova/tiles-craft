from fastapi import APIRouter, HTTPException, Request, Query
from shapely.geometry import shape
import tempfile
import rasterio
from rasterio import mask  # Importação corrigida
import numpy as np
from app.storage.minio_storage import create_minio_client

router = APIRouter()

@router.post("/collect", response_model=dict)
async def collect_tile_info(request: Request, tile_name: str = Query(..., description="Nome do tile")):
    MINIO_BUCKET = "raw-tiles"
    RASTER_FILE = tile_name + '.tif'
    print(RASTER_FILE)
    # Processando o GeoJSON recebido na requisição
    try:
        geojson = await request.json()
        geom = shape(geojson["geometry"])
    except Exception as e:
        raise HTTPException(status_code=400, detail=f"GeoJSON inválido: {e}")

    # Cria o cliente MinIO
    minio_client = create_minio_client()

    # Baixa o raster do MinIO e processa
    try:
        with tempfile.NamedTemporaryFile(suffix=".tif", delete=False) as tmp:
            # Baixa o arquivo do MinIO
            response = minio_client.get_object(MINIO_BUCKET, RASTER_FILE)
            tmp.write(response.read())
            tmp_path = tmp.name
            response.close()

        # Agora, processa o raster com rasterio
        with rasterio.open(tmp_path) as src:
            # Se a geometria for um polígono
            if geom.geom_type == "Polygon":
                masked, _ = mask.mask(src, [geom], crop=True)  # Usando a função `mask.mask`
                valid = masked[0][masked[0] != src.nodata]
                print(valid)
                if valid.size == 0:
                    raise HTTPException(status_code=404, detail="Nenhum dado válido no polígono.")
                media = float(np.mean(valid))
                return {"tipo": "Polygon", "media": media}

            # Se a geometria for uma linha
            elif geom.geom_type == "LineString":
                coords = list(geom.coords)
                values = []
                for lon, lat in coords:
                    row, col = src.index(lon, lat)
                    try:
                        value = src.read(1)[row, col]
                        if value != src.nodata:
                            values.append(float(value))
                    except IndexError:
                        continue
                if not values:
                    raise HTTPException(status_code=404, detail="Nenhum valor válido na linha.")
                return {"tipo": "LineString", "valores": values}

            else:
                raise HTTPException(status_code=400, detail="A geometria deve ser Polygon ou LineString.")
    
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Erro ao baixar ou processar o raster: {e}")
