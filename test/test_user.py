from fastapi.testclient import TestClient
from unittest import TestCase
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
    TestCase().assertEqual(response.status_code, 404)
    TestCase().assertEqual(data['detail'], "User not found")


def test_user_create_succesfully():
    body = {
        'id': 'anId',
        'first_name': 'first_name',
        'last_name': 'last_name',
        'email': 'email@mail.com'
    }
    response = client.post(URI, json=body)

    data = response.json()
    TestCase().assertEqual(response.status_code, 201)
    TestCase().assertDictEqual(body, data)


def test_user_create_existing_user_fails():
    body = {
        'id': 'anId',
        'first_name': 'first_name',
        'last_name': 'last_name',
        'email': 'email@mail.com'
    }
    # Created first time
    client.post(URI, json=body)
    # Try to create again
    response = client.post(URI, json=body)

    data = response.json()
    TestCase().assertEqual(response.status_code, 400)
    TestCase().assertEqual(data['detail'], "User already exists")


@pytest.mark.skip(reason="Work in progress")
def test_user_create_wrong_body():
    body = {
        'id': 'anId',
        'first_name': 'first_name',
        'last_name': 'last_name',
        'email': 'email@mail.com'
    }
    invalid_variations = {
        'id': [None, ''],
        'first_name': [None, '', 'aa'],
        'last_name': [None, '', 'aa'],
        'email': [None, '', 'email', 'a', 'email.com'],
    }

    invalid_bodies = generate_invalid(body, invalid_variations)

    for inv_body in invalid_bodies:
        response = client.post(URI, json=inv_body)
        TestCase().assertEqual(response.status_code, 422)


def test_user_create_and_retrieve_successfully():
    uid = 'anId'
    body = {
        'id': 'anId',
        'first_name': 'first_name',
        'last_name': 'last_name',
        'email': 'email@mail.com'
    }
    client.post(URI, json=body)
    response = client.get(URI + f"/{uid}")
    data = response.json()
    TestCase().assertDictEqual(body, data)
