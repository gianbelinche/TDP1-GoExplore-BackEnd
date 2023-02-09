from fastapi.testclient import TestClient
import pytest
from test.utils import generate_invalid

from app.app import app

client = TestClient(app)

URI = 'api/session'


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
    body_session = {
        'email': 'email@mail.com',
        'password': "1234",
    }
    body_user = {
        'first_name': 'first_name',
        'last_name': 'last_name',
        'email': 'email@mail.com',
        "password": "1234",
        "birth_date": "1990-01-01",
    }
    client.post('api/users', json=body_user)
    response = client.post(URI, json=body_session)
    assert response.status_code == 200


def test_post_session_invalid_password_fails():
    body_session = {
        'email': 'email@mail.com',
        'password': "12345",
    }
    body_user = {
        'first_name': 'first_name',
        'last_name': 'last_name',
        'email': 'email@mail.com',
        "password": "1234",
        "birth_date": "1990-01-01",
    }
    client.post('api/users', json=body_user)
    response = client.post(URI, json=body_session)
    assert response.status_code == 400
    assert response.json()["detail"] == "Incorrect Password"
