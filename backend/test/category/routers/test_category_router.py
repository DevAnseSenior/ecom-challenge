from fastapi.testclient import TestClient

from main import app

client = TestClient(app)


def test_must_list_categories():
    response = client.get('/categories')

    assert response.status_code == 200
    assert response.json() == [
        {'id': 1, 'description': 'Eletrônico'}
    ]


def test_must_create_category():
    new_category = {
        "description": "Eletrônico"
    }
    new_category_copy = new_category.copy()
    new_category_copy["id"] = 2

    response = client.post("/categories", json=new_category)
    assert response.status_code == 201
    assert response.json() == new_category_copy
