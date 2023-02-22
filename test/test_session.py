from fastapi.testclient import TestClient
import pytest
from test.utils import generate_invalid

from app.app import app

client = TestClient(app)

URI = 'api/session'


def create_user(fields={}):
    body = {
        'first_name': 'first_name',
        'last_name': 'last_name',
        'email': 'email@mail.com',
        'password': "1234",
        'host': False,
        "birth_date": "1990-01-01",
    }

    for k, v in fields.items():
        body[k] = v
    response = client.post("api/users", json=body)
    return response.json()


@pytest.fixture(autouse=True)
def clear_db():
    # This runs before each test

    yield

    # Ant this runs after each test
    client.post('api/reset')


def test_post_session_incorrect_fails():
    body = {
        'email': 'email@mail.com',
        'password': "1234",
    }
    response = client.post(URI, json=body)
    assert response.status_code == 400
    assert response.json()["detail"] == "User not found"


def test_post_session_correct_pass_succesfully():
    user_email = 'user@email.com'
    user_password = '1234pass'
    user = create_user({'email': user_email, 'password': user_password})

    body_session = {
        'email': user_email,
        'password': user_password,
    }

    response = client.post(URI, json=body_session)
    data = response.json()

    assert response.status_code == 200
    assert data['id'] == user['id']


def test_post_session_invalid_password_fails():
    user_email = 'user@email.com'
    user_password = '1234pass'
    create_user({'email': user_email, 'password': user_password})

    body_session = {
        'email': user_email,
        'password': 'wrong-password',
    }

    response = client.post(URI, json=body_session)
    data = response.json()
    assert response.status_code == 400
    assert data["detail"] == "Incorrect Password"
