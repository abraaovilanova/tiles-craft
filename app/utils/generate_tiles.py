import subprocess
from minio import Minio
import tempfile
import shutil
import os

def download_from_minio(minio_client, bucket, object_name, dest_path):
    minio_client.fget_object(bucket, object_name, dest_path)

def upload_dir_to_minio(minio_client, bucket, source_dir, dest_prefix):
    for root, dirs, files in os.walk(source_dir):
        for file in files:
            local_path = os.path.join(root, file)
            relative_path = os.path.relpath(local_path, source_dir)
            minio_path = f"{dest_prefix}/{relative_path}"
            minio_client.fput_object(bucket, minio_path, local_path)

def generate_tiles_with_minio(minio_client, input_bucket, input_object, output_bucket, output_prefix):
    with tempfile.TemporaryDirectory() as tmpdir:
        raster_path = os.path.join(tmpdir, "input.tif")
        vrt_path = os.path.join(tmpdir, "converted.vrt")
        tiles_path = os.path.join(tmpdir, "tiles")

        print(f"Downloading {input_object} from bucket {input_bucket} to {raster_path}")

        # Baixa o raster
        download_from_minio(minio_client, input_bucket, input_object, raster_path)

        # Converte para 8-bit com gdal_translate
        subprocess.run([
            "gdal_translate", "-of", "VRT", "-ot", "Byte", "-scale",
            raster_path, vrt_path
        ], check=True)

        # Gera os tiles usando o arquivo convertido
        subprocess.run([
            "gdal2tiles.py", "-z", "0-5", vrt_path, tiles_path
        ], check=True)

        # Faz o upload dos tiles
        upload_dir_to_minio(minio_client, output_bucket, tiles_path, output_prefix)

