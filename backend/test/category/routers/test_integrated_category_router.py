from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from main import app
from shared.database import Base
from shared.dependencies import get_db

client = TestClient(app)

SQLALCHEMY_DATABASE_URL = "sqlite:///./test.db"

engine = create_engine(
    SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False}
)

TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


def override_get_db():
    db = TestingSessionLocal()
    try:
        yield db
    finally:
        db.close()


app.dependency_overrides[get_db] = override_get_db


def test_must_list_categories():
    Base.metadata.drop_all(bind=engine)
    Base.metadata.create_all(bind=engine)

    client.post("/categories", json={'description': 'Eletrônicos'})
    client.post("/categories", json={'description': 'Ferramentas'})

    response = client.get('/categories')
    assert response.status_code == 200
    assert response.json() == [
        {'id': 1, 'description': 'Eletrônicos'},
        {'id': 2, 'description': 'Ferramentas'}
    ]


def test_must_get_one_category():
    Base.metadata.drop_all(bind=engine)
    Base.metadata.create_all(bind=engine)

    response = client.post("/categories", json={
        "description": "Ferramentas"
    })

    id_category = response.json()['id']

    response_get = client.get(f"/categories/{id_category}")
    assert response_get.status_code == 200
    assert response_get.json()['description'] == "Ferramentas"


def test_must_return_not_found_for_not_exist_id():
    Base.metadata.drop_all(bind=engine)
    Base.metadata.create_all(bind=engine)

    response_get = client.get(f"/categories/100")
    assert response_get.status_code == 404


def test_must_create_category():
    Base.metadata.drop_all(bind=engine)
    Base.metadata.create_all(bind=engine)

    new_category = {
        "description": "Ferramentas"
    }
    new_category_copy = new_category.copy()
    new_category_copy["id"] = 1

    response = client.post("/categories", json=new_category)
    assert response.status_code == 201
    assert response.json() == new_category_copy


def test_must_update_category():
    Base.metadata.drop_all(bind=engine)
    Base.metadata.create_all(bind=engine)

    response = client.post("/categories", json={
        "description": "Ferramentas"
    })

    id_category = response.json()['id']

    response_put = client.put(f"/categories/{id_category}", json={
        "description": "Ferragens"
    })
    assert response_put.status_code == 200
    assert response_put.json()['description'] == "Ferragens"


def test_must_return_not_found_for_not_exist_id_on_update():
    Base.metadata.drop_all(bind=engine)
    Base.metadata.create_all(bind=engine)

    response_put = client.put(f"/categories/100", json={
        "description": "Ferragens"
    })

    assert response_put.status_code == 404


def test_must_delete_category():
    Base.metadata.drop_all(bind=engine)
    Base.metadata.create_all(bind=engine)

    response = client.post("/categories", json={
        "description": "Ferramentas"
    })

    id_category = response.json()['id']

    response_put = client.delete(f"/categories/{id_category}")
    assert response_put.status_code == 204


def test_must_return_not_found_for_not_exist_id_on_delete():
    Base.metadata.drop_all(bind=engine)
    Base.metadata.create_all(bind=engine)

    response_put = client.delete(f"/categories/100")

    assert response_put.status_code == 404


def test_must_return_error_when_exceed_description():
    response = client.post('/categories', json={
        "description": "0123456789012345678901234567890"
    })
    assert response.status_code == 422


def test_must_return_error_when_description_less_than_necessary():
    response = client.post('/categories', json={
        "description": "01"
    })
    assert response.status_code == 422
