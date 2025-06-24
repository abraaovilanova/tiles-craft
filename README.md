# tiles-craft

O objetivo desse repositório é criar um pequeno servidor de tiles/raster/tiff para mapas.

Você pode fazer um upload de um arquivo `.tiff` e o tiles-craft gera uma pirâmede de zoom que pode ser consumida por um endpoit.

o tiles-craft tem u mserviço web que você pode fazer todas as operaçãoes pela interface.

o tiles-craft também tem uma api para você fazer todas as operações via requiset http;

## Como executar o projeto:
para rodar basta executar o docker compose 

```docker compose up --build```

o serviço web pode ser acessado na porta `localhost:8000` 

para rodar a pirâmide de zoom:

How to run this code:
build: `docker build -t gdal2tiles-container .`
run `docker run --rm -v $(pwd)/input-tiles:/app/input-tiles -v $(pwd)/output-tiles:/app/output-tiles gdal2tiles-container`

to run the application web:  `uvicorn app.main:app --reload` 

## Ferramentas utilizadas
- python
- Minio
- fast api
- gdal
- leaflet (web)

