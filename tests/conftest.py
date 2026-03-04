import pytest
from app import create_app
from app.extensions import db

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
