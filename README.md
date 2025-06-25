# tiles-craft

O objetivo desse repositório é criar um pequeno servidor de tiles/raster/tiff para mapas.

Você pode fazer um upload de um arquivo `.tiff` e o tiles-craft gera uma pirâmede de zoom que pode ser consumida por um endpoit.

o tiles-craft tem u mserviço web que você pode fazer todas as operaçãoes pela interface.

o tiles-craft também tem uma api para você fazer todas as operações via requiset http;

## Como executar o projeto:
para rodar basta executar o docker compose 

```docker compose up --build```

o serviço web pode ser acessado na porta `localhost:8000` 

## Ferramentas utilizadas
- python
- Minio
- fast api
- gdal
- leaflet (web)

# 🗺️ Tile Craft API

API construída com **FastAPI**, **SQLAlchemy** e **MinIO** para gerenciamento, geração e publicação de tiles raster.

## 📦 Funcionalidades

- 🔍 **Consultar Tiles** (`GET /tiles/` e `GET /tiles/{tile_id}`)
- ➕ **Criar Tiles** (`POST /tiles/`)
- ✏️ **Atualizar Tiles** (`PUT /tiles/{tile_id}`)
- ❌ **Deletar Tiles** (`DELETE /tiles/{tile_id}`)
- ⚙️ **Verificação de Saúde** (`GET /health`)
- 🚀 **Publicar Tile** (`POST /publish-tile`)  
  Gera tiles com `GDAL`, envia para o MinIO e atualiza o status no banco de dados.

## 🧪 Endpoints

| Método | Rota                  | Descrição                              |
|--------|------------------------|----------------------------------------|
| GET    | `/health`              | Verifica conexão com o banco           |
| GET    | `/tiles/`              | Lista todos os tiles                   |
| GET    | `/tiles/{tile_id}`     | Retorna detalhes de um tile            |
| POST   | `/tiles/`              | Cria um novo tile                      |
| PUT    | `/tiles/{tile_id}`     | Atualiza o nome de um tile             |
| DELETE | `/tiles/{tile_id}`     | Remove um tile                         |
| POST   | `/publish-tile`        | Gera os tiles raster e publica no MinIO|

## 🛠️ Tecnologias

- [FastAPI](https://fastapi.tiangolo.com/)
- [SQLAlchemy](https://www.sqlalchemy.org/)
- [MinIO](https://min.io/)
- [GDAL](https://gdal.org/)

## 📁 Estrutura Simplificada

