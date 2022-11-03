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
