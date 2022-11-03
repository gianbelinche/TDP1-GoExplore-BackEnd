from fastapi.testclient import TestClient
import pytest
from test.utils import generate_invalid

from app.app import app

client = TestClient(app)

URI = 'api/experiencies'


@pytest.fixture(autouse=True)
def clear_db():
    # This runs before each test

    yield

    # Ant this runs after each test
    client.post('api/reset')


@pytest.mark.skip(reason="Not implemented yet")
def test_get_experience_not_exists():
    response = client.get(URI + "/notexists")
    data = response.json()
    assert response.status_code == 404
    assert data['detail'] == "Experience not found"


def test_experience_create_succesfully():
    body = {
        'title': 'aTitle',
        'description': 'aDescription',
        'images': ['image1', 'image2', 'image3'],
        'preview_image': 'preview_image',
        'calendar': {'start_date': '2021-01-01', 'end_date': '2021-01-05', 'quota': 10},
        'owner': 'anOwner',
        'id': 'anId',
    }
    response = client.post(URI, json=body)

    data = response.json()
    assert response.status_code == 201
    assert body == data


def test_experience_create_with_missing_fields():
    body = {
        'description': 'aDescription',
        'images': ['image1', 'image2', 'image3'],
        'preview_image': 'preview_image',
        'calendar': {'start_date': '2021-01-01', 'end_date': '2021-01-05', 'quota': 10},
        'owner': 'anOwner',
        'id': 'anId',
    }
    response = client.post(URI, json=body)

    data = response.json()
    assert response.status_code == 422
    assert data["detail"][0]["type"] == "value_error.missing"


def test_experience_create_with_missing_calendar_fields():
    body = {
        'title': 'aTitle',
        'description': 'aDescription',
        'images': ['image1', 'image2', 'image3'],
        'preview_image': 'preview_image',
        'calendar': {},
        'owner': 'anOwner',
        'id': 'anId',
    }
    response = client.post(URI, json=body)

    data = response.json()
    assert response.status_code == 400
    assert data['detail'] == "Experience has incorrect calendar"


def test_experience_create_with_incorrect_number_of_calendar_fields():
    body = {
        'title': 'aTitle',
        'description': 'aDescription',
        'images': ['image1', 'image2', 'image3'],
        'preview_image': 'preview_image',
        'calendar': {
            'start_date': '2021-01-01',
            'end_date': '2021-01-05',
            'quota': 10,
            "another": "another",
        },
        'owner': 'anOwner',
        'id': 'anId',
    }
    response = client.post(URI, json=body)

    data = response.json()
    assert response.status_code == 400
    assert data['detail'] == "Experience has incorrect calendar"


def test_experience_create_with_incorrect_dates():
    body = {
        'title': 'aTitle',
        'description': 'aDescription',
        'images': ['image1', 'image2', 'image3'],
        'preview_image': 'preview_image',
        'calendar': {'start_date': '2021-01-01', 'end_date': '2020-01-05', 'quota': 10},
        'owner': 'anOwner',
        'id': 'anId',
    }
    response = client.post(URI, json=body)

    data = response.json()
    assert response.status_code == 400
    assert data['detail'] == "Experience has incorrect calendar"


def test_experience_create_with_equal_dates():
    body = {
        'title': 'aTitle',
        'description': 'aDescription',
        'images': ['image1', 'image2', 'image3'],
        'preview_image': 'preview_image',
        'calendar': {'start_date': '2021-01-01', 'end_date': '2021-01-01', 'quota': 10},
        'owner': 'anOwner',
        'id': 'anId',
    }
    response = client.post(URI, json=body)

    data = response.json()
    assert response.status_code == 201
    assert data == body


def test_experience_create_with_quota_less_than_0():
    body = {
        'title': 'aTitle',
        'description': 'aDescription',
        'images': ['image1', 'image2', 'image3'],
        'preview_image': 'preview_image',
        'calendar': {'start_date': '2021-01-01', 'end_date': '2021-01-05', 'quota': -1},
        'owner': 'anOwner',
        'id': 'anId',
    }
    response = client.post(URI, json=body)

    data = response.json()
    assert response.status_code == 400
    assert data['detail'] == "Experience has incorrect calendar"


def test_experience_create_with_incorrect_type_images():
    body = {
        'title': 'aTitle',
        'description': 'aDescription',
        'images': 'image1',
        'preview_image': 'preview_image',
        'calendar': {'start_date': '2021-01-01', 'end_date': '2021-01-05', 'quota': 10},
        'owner': 'anOwner',
        'id': 'anId',
    }
    response = client.post(URI, json=body)

    data = response.json()
    assert response.status_code == 422
    assert data["detail"][0]["type"] == "type_error.list"


def test_experience_create_with_empty_list_images():
    body = {
        'title': 'aTitle',
        'description': 'aDescription',
        'images': [],
        'preview_image': 'preview_image',
        'calendar': {'start_date': '2021-01-01', 'end_date': '2021-01-05', 'quota': 10},
        'owner': 'anOwner',
        'id': 'anId',
    }
    response = client.post(URI, json=body)

    data = response.json()
    assert response.status_code == 201
    assert data == body
