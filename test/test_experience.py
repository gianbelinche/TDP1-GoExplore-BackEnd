from fastapi.testclient import TestClient
from pprint import pprint
import pytest

from app.app import app
from test.utils import generate_invalid

client = TestClient(app)

URI = 'api/experiencies'


@pytest.fixture(autouse=True)
def clear_db():
    # This runs before each test

    yield

    # Ant this runs after each test
    client.post('api/reset')


def test_experience_create_succesfully():
    body = {
        'title': 'aTitle',
        'description': 'aDescription',
        'price': 0,
        'location': {
            'description': 'a location description',
            'lat': 23.4,
            'lng': 32.23,
        },
        'category': 'Gastronomía',
        'images': ['image1', 'image2', 'image3'],
        'preview_image': 'preview_image',
        'availability': ['2022-12-13', '2023-12-18'],
        'owner': 'anOwner',
    }
    response = client.post(URI, json=body)
    response_data = response.json()
    assert response.status_code == 201
    assert 'id' in response_data


def test_experience_create_with_wrong_body():
    body = {
        'title': 'aTitle',
        'description': 'aDescription',
        'price': 0,
        'location': {
            'description': 'a location description',
            'lat': 23.4,
            'lng': 32.23,
        },
        'category': 'Gastronomía',
        'images': ['image1', 'image2', 'image3'],
        'preview_image': 'preview_image',
        'availability': ['2022-12-13', '2023-12-18'],
        'owner': 'anOwner',
    }

    invalid_variations = {
        'title': [None, '', 'a'],
        'description': [None, '', 'a'],
        'price': [None, ''],
        'location': [
            None,
            '',
            3,
            {
                'description': 'a location description',
                'lng': 32.23,
            },
            {
                'description': 'a location description',
                'lng': 32.23,
                'lat': '',
            },
        ],
        'category': [None, '', 'NoExistente'],
        'images': [None, ''],
        'preview_image': [None, ''],
        'availability': [
            None,
            '',
            4,
            ['2022-12-13'],
            ['2022-12-13T23-03-22', '2023-12-18T23-03-22'],
            ['2021/01/01', '2021/01/02'],
        ],
        'owner': [None, ''],
    }

    invalid_bodies = generate_invalid(body, invalid_variations)

    # NOTE: If one of this tests fails, we don´t get enough information
    # we just know that the hole suit failed.

    for inv_body in invalid_bodies:
        response = client.post(URI, json=inv_body)
        try:
            assert response.status_code == 422
        except Exception:
            print("Failed body: \n")
            pprint(inv_body)
            raise


def test_get_experience_not_exists():
    response = client.get(URI + "/notexists")
    data = response.json()
    assert response.status_code == 404
    assert data['detail'] == "Experience not found"


def test_get_experience_exists():
    body = {
        'title': 'aTitle',
        'description': 'aDescription',
        'price': 0,
        'location': {
            'description': 'a location description',
            'lat': 23.4,
            'lng': 32.23,
        },
        'category': 'Gastronomía',
        'images': ['image1', 'image2', 'image3'],
        'preview_image': 'preview_image',
        'availability': ['2022-12-13', '2023-12-18'],
        'owner': 'anOwner',
    }
    response = client.post(URI, json=body)
    id = response.json()['id']
    expected_response = body.copy()
    expected_response['id'] = id

    response = client.get(f"{URI}/{id}")
    data = response.json()
    assert response.status_code == 200
    assert expected_response == data
