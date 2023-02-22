from fastapi.testclient import TestClient
import pytest
from test.utils import generate_invalid

from app.app import app

client = TestClient(app)

URI = 'api/users'


@pytest.fixture(autouse=True)
def clear_db():
    # This runs before each test

    yield

    # Ant this runs after each test
    client.post('api/reset')


def test_get_user_not_exists():
    response = client.get(URI + "/notexists")
    data = response.json()
    assert response.status_code == 404
    assert data['detail'] == "User not found"


def test_user_create_succesfully():
    body = {
        'first_name': 'first_name',
        'last_name': 'last_name',
        'email': 'email@mail.com',
        'host': False,
        'password': "1234",
        "birth_date": "1990-01-01",
    }
    response = client.post(URI, json=body)

    data = response.json()
    body["id"] = data["id"]
    body["cards"] = []
    assert response.status_code == 201
    assert body == data


def test_user_create_existing_user_fails():
    body = {
        'first_name': 'first_name',
        'last_name': 'last_name',
        'email': 'email@mail.com',
        'host': False,
        'password': "1234",
        "birth_date": "1990-01-01",
    }
    # Created first time
    client.post(URI, json=body)
    # Try to create again
    response = client.post(URI, json=body)

    data = response.json()
    assert response.status_code == 400
    assert data['detail'] == "User already exists"


def test_user_create_wrong_body():
    body = {
        'first_name': 'first_name',
        'last_name': 'last_name',
        'email': 'email@mail.com',
        'host': False,
        'password': "1234",
        "birth_date": "1990-01-01",
    }
    invalid_variations = {
        'first_name': [None, '', 'aa'],
        'last_name': [None, '', 'aa'],
        'email': [None, '', 'email', 'a', 'email.com'],
        'password': [None, '', 'a', 'aa'],
        'birth_date': [None, '', 'a', 'aa'],
    }

    invalid_bodies = generate_invalid(body, invalid_variations)

    # NOTE: If one of this tests fails, we don´t get enough information
    # we just know that the hole suit failed.

    for inv_body in invalid_bodies:
        response = client.post(URI, json=inv_body)
        assert response.status_code == 422


def test_user_create_and_retrieve_successfully():
    body = {
        'first_name': 'first_name',
        'last_name': 'last_name',
        'email': 'email@mail.com',
        'host': False,
        'password': "1234",
        "birth_date": "1990-01-01",
    }
    id = client.post(URI, json=body).json()["id"]
    response = client.get(URI + f"/{id}")
    data = response.json()
    body["id"] = id
    body["cards"] = []
    assert body == data


def test_user_create_existing_user_with_other_fields_different_fails():
    body = {
        'first_name': 'another_first_name',
        'last_name': 'another_last_name',
        'email': 'email@mail.com',
        'host': False,
        'password': "another_1234",
        "birth_date": "1991-01-01",
    }
    # Created first time
    client.post(URI, json=body)
    # Try to create again
    response = client.post(URI, json=body)

    data = response.json()
    assert response.status_code == 400
    assert data['detail'] == "User already exists"


def test_user_create_user_with_extra_fields_ignores_it():
    body = {
        'first_name': 'another_first_name',
        'last_name': 'another_last_name',
        'email': 'email@mail.com',
        'password': "another_1234",
        'host': False,
        "birth_date": "1991-01-01",
        "extra_field": "extra_field",
    }
    # Created first time
    response = client.post(URI, json=body)
    data = response.json()
    body["id"] = data["id"]
    body["cards"] = []
    body.pop("extra_field")
    assert response.status_code == 201
    assert data == body


def test_user_add_card_succesfully():
    body = {
        'first_name': 'first_name',
        'last_name': 'last_name',
        'email': 'email@mail.com',
        'host': False,
        'password': "1234",
        "birth_date": "1990-01-01",
    }
    id = client.post(URI, json=body).json()["id"]

    card_body = {
        "number": "1234-5678-9012-3456",
        "expiry_date": "2021-01-01",
        "security_code": "123",
    }
    response = client.post(URI + "/" + id + "/card", json=card_body)
    data = response.json()
    assert response.status_code == 201
    assert data["cards"] == [card_body]


def test_user_add_card_and_retreive_succesfully():
    body = {
        'first_name': 'first_name',
        'last_name': 'last_name',
        'email': 'email@mail.com',
        'host': False,
        'password': "1234",
        "birth_date": "1990-01-01",
    }
    id = client.post(URI, json=body).json()["id"]

    card_body = {
        "number": "1234-5678-9012-3456",
        "expiry_date": "2021-01-01",
        "security_code": "123",
    }
    client.post(URI + "/" + id + "/card", json=card_body)
    response = client.get(URI + "/" + id)
    data = response.json()
    assert response.status_code == 200
    assert data["cards"] == [card_body]


def test_user_add_two_cards_and_retreive_succesfully():
    body = {
        'first_name': 'first_name',
        'last_name': 'last_name',
        'email': 'email@mail.com',
        'host': False,
        'password': "1234",
        "birth_date": "1990-01-01",
    }
    id = client.post(URI, json=body).json()["id"]

    card_body = {
        "number": "1234-5678-9012-3456",
        "expiry_date": "2021-01-01",
        "security_code": "123",
    }
    card_body2 = {
        "number": "2234-5678-9012-3456",
        "expiry_date": "2022-01-01",
        "security_code": "122",
    }
    client.post(URI + "/" + id + "/card", json=card_body)
    client.post(URI + "/" + id + "/card", json=card_body2)
    response = client.get(URI + "/" + id)
    data = response.json()
    assert response.status_code == 200
    assert data["cards"] == [card_body, card_body2]


def test_user_add_invalid_card():
    body = {
        'first_name': 'first_name',
        'last_name': 'last_name',
        'email': 'email@mail.com',
        'host': False,
        'password': "1234",
        "birth_date": "1990-01-01",
    }
    id = client.post(URI, json=body).json()["id"]

    card_body = {
        "number": "1234-5678-9012-3456",
        "expiry_date": "2021-01-01",
        "security_code": "123",
    }

    invalid_variations = {
        "number": [None, '', 'aa'],
        "expiry_date": [None, '', 'aa'],
        "security_code": [None, '', 'aa'],
    }

    invalid_bodies = generate_invalid(card_body, invalid_variations)

    # NOTE: If one of this tests fails, we don´t get enough information
    # we just know that the hole suit failed.

    for inv_body in invalid_bodies:
        response = client.post(URI + "/" + id + "/card", json=inv_body)
        assert response.status_code == 422
