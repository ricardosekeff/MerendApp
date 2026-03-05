import json
import pytest
from app.models.school import School

def test_list_schools_api(client, auth_headers):
    """Testa a listagem de escolas via API."""
    response = client.get("/api/v1/schools", headers=auth_headers)
    assert response.status_code == 200
    assert isinstance(json.loads(response.data), list)

def test_create_school_api(client, auth_headers):
    """Testa a criação de uma escola via API."""
    data = {
        "name": "Escola de Teste API",
        "cnpj": "12.345.678/0001-99",
        "phone": "1199999999",
        "address": "Rua de Teste, 123",
        "city": "São Paulo",
        "state": "SP"
    }
    response = client.post("/api/v1/schools", 
                           data=json.dumps(data),
                           content_type="application/json",
                           headers=auth_headers)
    assert response.status_code == 201
    res_data = json.loads(response.data)
    assert res_data["name"] == "Escola de Teste API"
    assert "id" in res_data

def test_list_schools_web_unauthorized(client):
    """Testa se acesso à web sem login redireciona para login."""
    response = client.get("/admin/schools")
    assert response.status_code == 302
    assert "/login" in response.location

def test_list_schools_web_authorized(client, admin_user):
    """Testa a listagem de escolas via Web após login."""
    # Simula login manual (Session)
    with client.session_transaction() as sess:
        sess['_user_id'] = str(admin_user.id)
    
    response = client.get("/admin/schools")
    print(response.data.decode('utf-8'))
    assert response.status_code == 200
    assert b"Escolas" in response.data

def test_create_school_web(client, admin_user):
    """Testa a criação de uma escola via formulário Web."""
    with client.session_transaction() as sess:
        sess['_user_id'] = str(admin_user.id)
        
    data = {
        "name": "Escola Web Test",
        "cnpj": "11.222.333/0001-44",
        "phone": "1122223333",
        "address": "Av Web, 456",
        "city": "Rio de Janeiro",
        "state": "RJ"
    }
    response = client.post("/admin/schools/new", data=data, follow_redirects=True)
    assert response.status_code == 200
    assert b"Escola criada com sucesso!" in response.data
    assert b"Escola Web Test" in response.data
