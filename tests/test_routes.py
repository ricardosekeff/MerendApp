import json

def test_health_endpoint(client):
    """Testa o endpoint de health check global (/health)."""
    response = client.get("/health")
    assert response.status_code == 200
    data = json.loads(response.data)
    assert data["status"] == "ok"
    assert "env" in data

def test_api_v1_health(client):
    """Testa o endpoint de health check do blueprint da API (/api/v1/health)."""
    response = client.get("/api/v1/health")
    assert response.status_code == 200
    data = json.loads(response.data)
    assert data["status"] == "ok"
    assert data["service"] == "api"

def test_root_redirect_unauthorized(client):
    """Testa se a raiz (/) redireciona para o login quando não autenticado."""
    response = client.get("/")
    assert response.status_code == 302
    assert "/login" in response.location

def test_login_page_renders(client):
    """Testa se a página de login renderiza corretamente."""
    response = client.get("/login")
    assert response.status_code == 200
    assert b"MerendApp" in response.data
    assert b"ENTRAR NO SISTEMA" in response.data

def test_api_404_json(client):
    """Testa se rotas inexistentes na API retornam JSON."""
    response = client.get("/api/v1/rota-que-nao-existe")
    assert response.status_code == 404
    data = json.loads(response.data)
    assert "error" in data
    assert data["error"] == "Not Found"
