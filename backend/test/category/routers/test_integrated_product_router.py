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


def test_must_list_products():
    Base.metadata.drop_all(bind=engine)
    Base.metadata.create_all(bind=engine)

    client.post("/products", json={'description': 'Celular', 'quantity': 2})
    client.post("/products", json={'description': 'Ar-Condicionado', 'quantity': 10})

    response = client.get('/products')
    assert response.status_code == 200
    assert response.json() == [
        {'id': 1, 'description': 'Celular', 'quantity': 2},
        {'id': 2, 'description': 'Ar-Condicionado', 'quantity': 10}
    ]


def test_must_get_one_product():
    Base.metadata.drop_all(bind=engine)
    Base.metadata.create_all(bind=engine)

    response = client.post("/products", json={
        "description": "Celular",
        "quantity": 4
    })

    id_product = response.json()['id']

    response_get = client.get(f"/products/{id_product}")
    assert response_get.status_code == 200
    assert response_get.json()['description'] == "Celular"
    assert response_get.json()['quantity'] == 4


def test_must_return_not_found_for_not_exist_id():
    Base.metadata.drop_all(bind=engine)
    Base.metadata.create_all(bind=engine)

    response_get = client.get(f"/products/100")
    assert response_get.status_code == 404


def test_must_create_product():
    Base.metadata.drop_all(bind=engine)
    Base.metadata.create_all(bind=engine)

    new_product = {
        "description": "Ferramentas",
        "quantity": 12
    }
    new_product_copy = new_product.copy()
    new_product_copy["id"] = 1

    response = client.post("/products", json=new_product)
    assert response.status_code == 201
    assert response.json() == new_product_copy


def test_must_update_product():
    Base.metadata.drop_all(bind=engine)
    Base.metadata.create_all(bind=engine)

    response = client.post("/products", json={
        "description": "Ar-condicionado",
        "quantity": 24
    })

    id_product = response.json()['id']

    response_put = client.put(f"/products/{id_product}", json={
        "description": "Condicionador de Ar",
        "quantity": 12
    })
    assert response_put.status_code == 200
    assert response_put.json()['description'] == "Condicionador de Ar"
    assert response_put.json()['quantity'] == 12


def test_must_return_not_found_for_not_exist_id_on_update():
    Base.metadata.drop_all(bind=engine)
    Base.metadata.create_all(bind=engine)

    response_put = client.put(f"/products/100", json={
        "description": "Celular",
        "quantity": 21
    })

    assert response_put.status_code == 404


def test_must_delete_product():
    Base.metadata.drop_all(bind=engine)
    Base.metadata.create_all(bind=engine)

    response = client.post("/products", json={
        "description": "Celular",
        "quantity": 10
    })

    id_product = response.json()['id']

    response_put = client.delete(f"/products/{id_product}")
    assert response_put.status_code == 204


def test_must_return_not_found_for_not_exist_id_on_delete():
    Base.metadata.drop_all(bind=engine)
    Base.metadata.create_all(bind=engine)

    response_put = client.delete(f"/products/100")

    assert response_put.status_code == 404


def test_must_return_error_when_exceed_description():
    eg_desc = "B" * 256
    response = client.post('/products', json={
        "description": eg_desc,
        "quantity": 10
    })
    assert response.status_code == 422


def test_must_return_error_when_description_less_than_necessary():
    response = client.post('/products', json={
        "description": "01",
        "quantity": 10
    })
    assert response.status_code == 422
