import os
from flask import Flask
from config import config_by_env
from app.extensions import db, migrate, jwt, ma, login_manager, celery_init_app

def create_app(config_name=None):
    """
    Application Factory para o MerendApp.
    Inicializa Flask, extensões, Blueprints e global handlers.
    """
    if config_name is None:
        config_name = os.getenv("APP_ENV", "development")

    app = Flask(__name__)
    
    # Carrega configurações
    app.config.from_object(config_by_env[config_name])

    # Inicializa extensões
    db.init_app(app)
    migrate.init_app(app, db)
    jwt.init_app(app)
    ma.init_app(app)
    login_manager.init_app(app)
    login_manager.login_view = "web.login"
    login_manager.login_message_category = "info"
    
    from app.models.user import User
    import uuid
    @login_manager.user_loader
    def load_user(user_id):
        try:
            return db.session.get(User, uuid.UUID(user_id))
        except (ValueError, TypeError):
            return None
    
    # Inicializa Celery (se configurado)
    celery_init_app(app)

    from app.api.errors import register_error_handlers
    from app.utils.tenant_utils import resolve_tenant
    
    register_error_handlers(app)
    
    @app.before_request
    def handle_tenant():
        resolve_tenant()

    # Registro de Blueprints
    from app.api import api_bp
    from app.web import web_bp

    app.register_blueprint(api_bp, url_prefix="/api/v1")
    app.register_blueprint(web_bp, url_prefix="/")

    @app.route("/health")
    def health():
        return {"status": "ok", "env": config_name}, 200

    return app
