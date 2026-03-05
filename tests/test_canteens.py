import json
import pytest
from app.models.canteen import Canteen
from app.models.school import School

@pytest.fixture
def test_school(app):
    """Cria uma escola para vincular cantinas nos testes."""
    with app.app_context():
        school = School(name="Escola Vinculo", cnpj="99.888.777/0001-66")
        db.session.add(school)
        db.session.commit()
        db.session.refresh(school)
        return school

def test_list_canteens_api(client, auth_headers):
    """Testa a listagem de cantinas via API."""
    response = client.get("/api/v1/canteens", headers=auth_headers)
    assert response.status_code == 200
    assert isinstance(json.loads(response.data), list)

def test_create_canteen_api(client, auth_headers, test_school):
    """Testa a criação de uma cantina via API vinculada a uma escola."""
    data = {
        "name": "Cantina API Test"
    }
    response = client.post(f"/api/v1/schools/{test_school.id}/canteens", 
                           data=json.dumps(data),
                           content_type="application/json",
                           headers=auth_headers)
    assert response.status_code == 201
    res_data = json.loads(response.data)
    assert res_data["name"] == "Cantina API Test"
    assert str(res_data["school_id"]) == str(test_school.id)

def test_list_canteens_web_authorized(client, admin_user):
    """Testa a listagem de cantinas via Web após login."""
    with client.session_transaction() as sess:
        sess['_user_id'] = str(admin_user.id)
    
    response = client.get("/admin/canteens")
    assert response.status_code == 200
    assert b"Cantinas" in response.data

def test_create_canteen_web(client, admin_user, test_school):
    """Testa a criação de uma cantina via formulário Web."""
    with client.session_transaction() as sess:
        sess['_user_id'] = str(admin_user.id)
        
    data = {
        "name": "Cantina Web Test",
        "school_id": str(test_school.id)
    }
    response = client.post("/admin/canteens/new", data=data, follow_redirects=True)
    assert response.status_code == 200
    assert b"Cantina" in response.data
    assert b"Web Test" in response.data

from app.extensions import db # Import db for the fixture
