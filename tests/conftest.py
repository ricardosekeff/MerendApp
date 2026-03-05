import pytest
from app import create_app
from app.extensions import db
from app.models.user import User
from flask_jwt_extended import create_access_token

@pytest.fixture
def app():
    """Fixture para criar a instância da aplicação Flask em modo de teste."""
    app = create_app("testing")
    
    with app.app_context():
        db.create_all()
        yield app
        db.session.remove()
        db.drop_all()

@pytest.fixture
def client(app):
    """Fixture para o cliente de teste do Flask."""
    return app.test_client()

@pytest.fixture
def runner(app):
    """Fixture para o runner de comandos CLI do Flask."""
    return app.test_cli_runner()

@pytest.fixture
def admin_user(app):
    """Cria um usuário administrador para testes."""
    with app.app_context():
        user = User(
            name="Admin Test",
            email="admin_test@merendapp.com.br",
            role="ADMIN_MASTER",
            active=True
        )
        user.set_password("password")
        db.session.add(user)
        db.session.commit()
        db.session.refresh(user)
        return user

@pytest.fixture
def auth_headers(admin_user):
    """Gera headers de autenticação JWT para o admin."""
    access_token = create_access_token(identity=str(admin_user.id), additional_claims={"role": "ADMIN_MASTER"})
    return {"Authorization": f"Bearer {access_token}"}
