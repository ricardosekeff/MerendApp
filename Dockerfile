# ============================================================
# Stage 1: Builder
# Instala dependências Python em um ambiente isolado
# ============================================================
FROM python:3.11-slim AS builder

WORKDIR /app

# Instala dependências de sistema necessárias para compilação
RUN apt-get update && apt-get install -y --no-install-recommends \
    gcc \
    libpq-dev \
    && rm -rf /var/lib/apt/lists/*

# Copia e instala dependências Python
COPY requirements.txt .
RUN pip install --upgrade pip && \
    pip install --no-cache-dir --prefix=/install -r requirements.txt


# ============================================================
# Stage 2: Production
# Imagem final limpa, apenas o necessário para rodar
# ============================================================
FROM python:3.11-slim AS production

WORKDIR /app

# Dependências de runtime do PostgreSQL
RUN apt-get update && apt-get install -y --no-install-recommends \
    libpq5 \
    && rm -rf /var/lib/apt/lists/*

# Copia as dependências instaladas do stage builder
COPY --from=builder /install /usr/local

# Cria usuário não-root por segurança
RUN addgroup --system appgroup && adduser --system --ingroup appgroup appuser

# Copia o código da aplicação
COPY --chown=appuser:appgroup . .

# Troca para usuário não-root
USER appuser

# Porta exposta pelo Gunicorn
EXPOSE 8000

# Health check para o Docker verificar se a app está respondendo
HEALTHCHECK --interval=30s --timeout=10s --start-period=10s --retries=3 \
    CMD python -c "import urllib.request; urllib.request.urlopen('http://localhost:8000/health')" || exit 1

# Comando padrão: Gunicorn com 4 workers
CMD ["gunicorn", \
     "--bind", "0.0.0.0:8000", \
     "--workers", "4", \
     "--worker-class", "sync", \
     "--timeout", "120", \
     "--access-logfile", "-", \
     "--error-logfile", "-", \
     "run:app"]
