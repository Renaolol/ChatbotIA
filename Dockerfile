FROM python:3.11-slim

# Define configurações padrão do Python e pip
ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    PIP_NO_CACHE_DIR=1

WORKDIR /app

# Dependências do sistema necessárias para compilar/rodar libs usadas pelo projeto
RUN apt-get update && \
    apt-get install -y --no-install-recommends build-essential && \
    rm -rf /var/lib/apt/lists/*

# Instala dependências Python antes de copiar o restante do código para aproveitar cache
COPY requirements.txt .
RUN pip install --upgrade pip && pip install -r requirements.txt

# Copia todo o projeto
COPY . .

# Garante que as pastas usadas pelo app existam e tenham permissão correta
RUN mkdir -p data tmp/chromadb tmp && \
    adduser --disabled-password --gecos "" appuser && \
    chown -R appuser:appuser /app

USER appuser

EXPOSE 8501

CMD ["streamlit", "run", "streamlit_app.py", "--server.address=0.0.0.0", "--server.port=8501"]
