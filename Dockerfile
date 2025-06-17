# --- Stage 1: Builder ---
    FROM python:3.10-slim-bullseye AS builder

    WORKDIR /app
    
    ENV PYTHONDONTWRITEBYTECODE 1
    ENV PYTHONUNBUFFERED 1
    
    RUN apt-get update && \
        apt-get install -y --no-install-recommends \
            build-essential \
            libpq-dev \
            default-libmysqlclient-dev \
            gcc \
            pkg-config && \
        rm -rf /var/lib/apt/lists/*
    
    COPY requirements.txt .
    RUN pip wheel --no-cache-dir --wheel-dir /wheels -r requirements.txt
    
    # --- Stage 2: Runtime ---
    FROM python:3.10-slim-bullseye
    
    WORKDIR /app
    
    ENV PYTHONDONTWRITEBYTECODE 1
    ENV PYTHONUNBUFFERED 1
    ENV DJANGO_SETTINGS_MODULE=config.settings
    
    RUN apt-get update && \
        apt-get install -y --no-install-recommends \
            libpq5 \
            default-mysql-client && \
        rm -rf /var/lib/apt/lists/*
    
    # Copia o entrypoint primeiro E TORNA EXECUTÁVEL COMO ROOT
    COPY entrypoint.sh /entrypoint.sh
    RUN chmod +x /entrypoint.sh 
    
    # Cria usuário não-root
    RUN useradd -ms /bin/bash appuser
    RUN mkdir -p /app/staticfiles /app/mediafiles && chown -R appuser:appuser /app
    
    COPY --from=builder /wheels /wheels
    COPY requirements.txt .
    RUN pip install --no-cache-dir -r requirements.txt --find-links=/wheels
    
    COPY . .
    RUN chown -R appuser:appuser /app
    
    # Muda para o usuário não-root
    USER appuser
    
    # Define o entrypoint (o arquivo já é executável)
    ENTRYPOINT ["/entrypoint.sh"]
    
    CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]
    