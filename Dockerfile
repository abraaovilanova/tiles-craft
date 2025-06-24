# # Usando uma imagem base com Python 3
# FROM python:3.12-slim

# # Definir diretório de trabalho
# WORKDIR /app

# # Instalar dependências do sistema para o GDAL
# RUN apt-get update && apt-get install -y \
#     gdal-bin \
#     libgdal-dev \
#     build-essential \
#     && rm -rf /var/lib/apt/lists/*

# # Instalar a biblioteca gdal2tiles
# RUN pip install --no-cache-dir gdal2tiles

# # Copiar o script Python para dentro do contêiner
# COPY generate_tiles.py /app/generate_tiles.py

# # Definir o comando para rodar o script
# CMD ["python", "/app/generate_tiles.py"]

# # Imagem base com Python
# FROM python:3.12-slim

# # Define diretório de trabalho
# WORKDIR /app

# # Instala utilitários do sistema necessários para pg_isready
# RUN apt-get update && apt-get install -y postgresql-client && apt-get clean

# # Copia arquivos de dependência
# COPY requirements.txt* ./

# # Instala dependências com pip
# RUN pip install --upgrade pip && \
#     if [ -f requirements.txt ]; then pip install -r requirements.txt; fi

# # Copia o restante do código
# COPY . .

# # Copia o script de inicialização e dá permissão
# COPY start.sh /app/start.sh
# RUN chmod +x /app/start.sh

# # Expõe a porta
# EXPOSE 8000

# ENV PYTHONPATH=/app

# # Executa o script ao iniciar o container
# CMD ["./start.sh"]

FROM python:3.12-slim

WORKDIR /app

# Instala GDAL + PostgreSQL client + dependências básicas
RUN apt-get update && apt-get install -y \
    gdal-bin \
    libgdal-dev \
    build-essential \
    postgresql-client \
    && rm -rf /var/lib/apt/lists/*

# Copia e instala dependências do Python
COPY requirements.txt ./
RUN pip install --upgrade pip && pip install -r requirements.txt

# Copia o restante do código, incluindo generate_tiles.py
COPY . .

# Torna o script de inicialização executável
COPY start.sh /app/start.sh
RUN chmod +x /app/start.sh

EXPOSE 8000
ENV PYTHONPATH=/app

CMD ["./start.sh"]