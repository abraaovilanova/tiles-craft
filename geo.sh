#!/bin/sh

# Caminho do arquivo GeoTIFF e do diretório de saída
GEOTIFF_PATH="MDE_26124se_v1.tif"
OUTPUT_DIR="/tmp/wms_tiles/mylayer"

# Níveis de zoom
ZOOM_LEVELS="0-5"

# Verifica se o arquivo GeoTIFF existe
if [ ! -f "$GEOTIFF_PATH" ]; then
  echo "Arquivo GeoTIFF não encontrado!"
  exit 1
fi

# Cria o diretório de saída se não existir
mkdir -p "$OUTPUT_DIR"

# Executa o gdal2tiles
echo "Gerando tiles com gdal2tiles..."
python3 /usr/bin/gdal2tiles.py -z "$ZOOM_LEVELS" -w none "$GEOTIFF_PATH" "$OUTPUT_DIR"

# Verifica se o comando foi bem-sucedido
if [ $? -eq 0 ]; then
  echo "Tiles gerados com sucesso em $OUTPUT_DIR"
else
  echo "Erro ao gerar os tiles."
  exit 1
fi