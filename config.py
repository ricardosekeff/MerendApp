"""
MerendApp — Configurações da Aplicação.

Classes:
    Config             Configurações base (shared).
    DevelopmentConfig  Para ambiente de desenvolvimento local.
    TestingConfig      Para execução de testes automatizados.
    ProductionConfig   Para ambiente de produção.

Uso (Application Factory):
    app.config.from_object(config_by_env[os.getenv('APP_ENV', 'development')])
"""

import os
from datetime import timedelta


class Config:
    """Configurações base compartilhadas entre todos os ambientes."""

    # ── Flask ──────────────────────────────────────────────────────────────
    SECRET_KEY: str = os.environ.get("SECRET_KEY", "insecure-default-change-me")
    DEBUG: bool = False
    TESTING: bool = False

    # ── SQLAlchemy ─────────────────────────────────────────────────────────
    SQLALCHEMY_DATABASE_URI: str = os.environ.get(
        "DATABASE_URL",
        "postgresql://merendapp_user:changeme@localhost:5432/merendapp",
    )
    SQLALCHEMY_TRACK_MODIFICATIONS: bool = False
    SQLALCHEMY_ENGINE_OPTIONS: dict = {
        "pool_pre_ping": True,
        "pool_recycle": 300,
    }

    # ── JWT ────────────────────────────────────────────────────────────────
    JWT_SECRET_KEY: str = os.environ.get("JWT_SECRET_KEY", "insecure-jwt-secret")
    JWT_ACCESS_TOKEN_EXPIRES: timedelta = timedelta(
        seconds=int(os.environ.get("JWT_ACCESS_TOKEN_EXPIRES", 900))  # 15 min
    )
    JWT_REFRESH_TOKEN_EXPIRES: timedelta = timedelta(
        seconds=int(os.environ.get("JWT_REFRESH_TOKEN_EXPIRES", 604800))  # 7 dias
    )

    # ── Redis / Celery ─────────────────────────────────────────────────────
    REDIS_URL: str = os.environ.get("REDIS_URL", "redis://localhost:6379/0")
    CELERY_BROKER_URL: str = os.environ.get(
        "CELERY_BROKER_URL", "redis://localhost:6379/0"
    )
    CELERY_RESULT_BACKEND: str = os.environ.get(
        "CELERY_RESULT_BACKEND", "redis://localhost:6379/0"
    )

    # ── Flask-WTF ──────────────────────────────────────────────────────────
    WTF_CSRF_ENABLED: bool = True

    # ── App ────────────────────────────────────────────────────────────────
    APP_BASE_URL: str = os.environ.get("APP_BASE_URL", "http://localhost")
    DEFAULT_TOKEN_EXPIRY_MINUTES: int = int(
        os.environ.get("DEFAULT_TOKEN_EXPIRY_MINUTES", 30)
    )


class DevelopmentConfig(Config):
    """Ambiente de desenvolvimento local."""

    DEBUG: bool = True
    SQLALCHEMY_ECHO: bool = True  # Log de queries SQL no terminal


class TestingConfig(Config):
    """Ambiente de teste automatizado."""

    TESTING: bool = True
    DEBUG: bool = True

    # Banco em memória — zero dependência externa para CI
    SQLALCHEMY_DATABASE_URI: str = "sqlite:///:memory:"
    SQLALCHEMY_ENGINE_OPTIONS: dict = {}  # Desabilita pool options para SQLite

    # Desabilita CSRF para facilitar o test client
    WTF_CSRF_ENABLED: bool = False

    # Tokens com expiração muito curta para testes
    JWT_ACCESS_TOKEN_EXPIRES: timedelta = timedelta(seconds=10)
    JWT_REFRESH_TOKEN_EXPIRES: timedelta = timedelta(seconds=60)


class ProductionConfig(Config):
    """Ambiente de produção — nunca ativa DEBUG."""

    DEBUG: bool = False

    # Em produção, SECRET_KEY DEVE vir do ambiente. 
    # Usamos .get() para evitar erro no momento do import em outros ambientes.
    SECRET_KEY: str = os.environ.get("SECRET_KEY", "")
    JWT_SECRET_KEY: str = os.environ.get("JWT_SECRET_KEY", "")


# Mapeamento de string → classe de config (usado no create_app)
config_by_env: dict = {
    "development": DevelopmentConfig,
    "testing": TestingConfig,
    "production": ProductionConfig,
}
