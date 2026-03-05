from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_jwt_extended import JWTManager
from flask_marshmallow import Marshmallow
from flask_login import LoginManager
from celery import Celery

# ── SQLAlchemy (ORM) ──────────────────────────────────────────────────
db = SQLAlchemy()

# ── Flask-Migrate (Alembic) ───────────────────────────────────────────
migrate = Migrate()

# ── Flask-JWT-Extended ───────────────────────────────────────────────
jwt = JWTManager()

# ── Flask-Marshmallow ────────────────────────────────────────────────
ma = Marshmallow()

# ── Flask-Login ──────────────────────────────────────────────────────
login_manager = LoginManager()

# ── Celery configuration ──────────────────────────────────────────────
def celery_init_app(app) -> Celery:
    class FlaskTask(Celery.Task): # Changed Task to Celery.Task
        def __call__(self, *args: object, **kwargs: object) -> object:
            with app.app_context():
                return self.run(*args, **kwargs)

    celery_app = Celery(app.name, task_cls=FlaskTask)
    celery_app.config_from_object(app.config["CELERY_BROKER_URL"]) # broker
    # O Celery 5.x usa lowercase para as configs, mas o Flask usa Upper.
    # Por praticidade para esse scaffold, carregaremos via o config dict.
    celery_app.conf.update(
        broker_url=app.config.get("CELERY_BROKER_URL"),
        result_backend=app.config.get("CELERY_RESULT_BACKEND"),
        task_ignore_result=True,
    )
    celery_app.set_default()
    app.extensions["celery"] = celery_app
    return celery_app

# Dummy instance for initial reference in imports
celery = Celery()
