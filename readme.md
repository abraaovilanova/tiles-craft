para rodar a pirâmide de zoom:

build: `docker build -t gdal2tiles-container .`
run `docker run --rm -v $(pwd)/input-tiles:/app/input-tiles -v $(pwd)/output-tiles:/app/output-tiles gdal2tiles-container`

to run the application web:  `uvicorn app.main:app --reload` 