# --- Stage 1: Builder ---
# Instala dependências do sistema e Python
FROM python:3.10-slim-bullseye as builder

WORKDIR /app

# Variáveis de ambiente recomendadas
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

# Instala dependências do sistema necessárias para compilar libs Python
RUN apt-get update && \
    apt-get install -y --no-install-recommends \
        build-essential \
        libpq-dev \
        default-libmysqlclient-dev \
        gcc && \
    rm -rf /var/lib/apt/lists/*

# Copia e instala dependências Python (usando wheels para cache)
COPY requirements.txt .
RUN pip wheel --no-cache-dir --wheel-dir /wheels -r requirements.txt

# --- Stage 2: Runtime ---
# Imagem final, mais leve
FROM python:3.10-slim-bullseye

WORKDIR /app

ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1
ENV DJANGO_SETTINGS_MODULE=config.settings # Ajuste se necessário

# Instala apenas as bibliotecas de runtime necessárias
RUN apt-get update && \
    apt-get install -y --no-install-recommends \
        libpq5 \
        default-mysql-client && \
    rm -rf /var/lib/apt/lists/*

# Cria usuário não-root
RUN useradd -ms /bin/bash appuser
# Cria diretório para static/media e dá permissão (opcional, mas bom se usar)
RUN mkdir -p /app/staticfiles /app/mediafiles && chown -R appuser:appuser /app

# Copia dependências pré-compiladas (wheels) e instala
COPY --from=builder /wheels /wheels
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt --find-links=/wheels

# Copia o código da aplicação
COPY . .
# Muda dono dos arquivos para o usuário não-root
RUN chown -R appuser:appuser /app

# Muda para o usuário não-root
USER appuser

# Copia e dá permissão ao entrypoint script
COPY entrypoint.sh /entrypoint.sh
RUN chmod +x /entrypoint.sh

# Define o entrypoint
ENTRYPOINT ["/entrypoint.sh"]

# Comando padrão (pode ser sobrescrito no docker-compose)
# Ex: gunicorn config.wsgi:application --bind 0.0.0.0:8000
CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]
