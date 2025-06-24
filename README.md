# tiles-craft

O objetivo desse repositório é criar um pequeno servidor de tiles/raster/tiff para mapas.

Você sobe uma imagem tiff e o servidor gera uma pirâmede de zoom que pode ser consumida por um endpoit.

para rodar basta executar o docker compose 

```docker compose up --build```

o serviço web pode ser acessado na porta `localhost:8000` 