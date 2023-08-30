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


def test_must_list_users():
    Base.metadata.drop_all(bind=engine)
    Base.metadata.create_all(bind=engine)

    client.post("/users/register", json={'username': 'testuser01', 'hashed_password': '43434', 'email': 'test01@test.com'})
    client.post("/users/register", json={'username': 'testuser02', 'hashed_password': '434324', 'email': 'test02@test.com'})

    response = client.get('/users')
    assert response.status_code == 200
    assert response.json()[0]["username"] == "testuser01"
    assert response.json()[0]["email"] == "test01@test.com"
    assert response.json()[1]["username"] == "testuser02"
    assert response.json()[1]["email"] == "test02@test.com"


def test_must_get_one_user():
    Base.metadata.drop_all(bind=engine)
    Base.metadata.create_all(bind=engine)

    response = client.post("/users/register", json={
        "username": "usertest",
        "hashed_password": "test",
        "email": "teste@teste.com"
    })

    id_user = response.json()['id']

    response_get = client.get(f"/users/{id_user}")
    assert response_get.status_code == 200
    assert response_get.json()['username'] == "usertest"
    assert response_get.json()['email'] == "teste@teste.com"


def test_must_return_not_found_for_not_exist_id():
    Base.metadata.drop_all(bind=engine)
    Base.metadata.create_all(bind=engine)

    response_get = client.get(f"/users/100")
    assert response_get.status_code == 404


def test_must_register_user():
    Base.metadata.drop_all(bind=engine)
    Base.metadata.create_all(bind=engine)

    new_user = {
        "username": "usertest",
        "hashed_password": "test",
        "email": "teste@teste.com"
    }
    new_user_copy = new_user.copy()
    new_user_copy["id"] = 1

    response = client.post("/users/register", json=new_user)
    assert response.status_code == 201
    assert response.json()["username"] == "usertest"
    assert response.json()["email"] == "teste@teste.com"


def test_must_update_user():
    Base.metadata.drop_all(bind=engine)
    Base.metadata.create_all(bind=engine)

    response = client.post("/users/register", json={
        "username": "testuser",
        "hashed_password": "4444",
        "email": "teste@test"
    })
    # print("0001-id", response.json()['id'])
    id_user = response.json()['id']

    response_put = client.put(f"/users/{id_user}", json={
        "username": "usertest",
        "hashed_password": "5034",
        "email": "test@test.com"
    })
    assert response_put.status_code == 200
    assert response_put.json()['username'] == "usertest"
    assert response_put.json()['email'] == "test@test.com"


def test_must_return_not_found_for_not_exist_id_on_update():
    Base.metadata.drop_all(bind=engine)
    Base.metadata.create_all(bind=engine)

    response_put = client.put(f"/users/100", json={
        "username": "usertest",
        "hashed_password": "5034",
        "email": "test@test.com"
    })

    assert response_put.status_code == 404


def test_must_delete_user():
    Base.metadata.drop_all(bind=engine)
    Base.metadata.create_all(bind=engine)

    response = client.post("/users/register", json={
        "username": "usertest",
        "hashed_password": "5034",
        "email": "test@test.com"
    })

    id_user = response.json()['id']

    response_put = client.delete(f"/users/{id_user}")
    assert response_put.status_code == 204


def test_must_return_not_found_for_not_exist_id_on_delete():
    Base.metadata.drop_all(bind=engine)
    Base.metadata.create_all(bind=engine)

    response_put = client.delete(f"/users/100")

    assert response_put.status_code == 404


def test_must_return_error_when_exceed_username():
    eg_desc = "B" * 256
    response = client.post('/users/register', json={
        "username": eg_desc,
        "hashed_password": "5034",
        "email": "test@test.com"
    })
    assert response.status_code == 422


def test_must_return_error_when_description_less_than_necessary():
    response = client.post('/users/register', json={
        "username": "ab"
    })
    assert response.status_code == 422
