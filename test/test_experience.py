from fastapi.testclient import TestClient
from pprint import pprint
import pytest

from app.app import app
from test.utils import generate_invalid

client = TestClient(app)

URI = 'api/experiences'


def create_experience(fields={}):
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

    for k, v in fields.items():
        body[k] = v

    response = client.post("api/experiences", json=body)
    return response.json()


@pytest.fixture(autouse=True)
def clear_db():
    # This runs before each test

    yield

    # Ant this runs after each test
    client.post('api/reset')


def test_experience_create_succesfully():
    body = create_experience()
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
    body = create_experience()
    response = client.post(URI, json=body)
    id = response.json()['id']
    expected_response = body.copy()
    expected_response['id'] = id
    expected_response['score'] = 0.0

    response = client.get(f"{URI}/{id}")
    data = response.json()
    assert response.status_code == 200
    assert expected_response == data


def test_search_experience_by_category():
    exp1 = create_experience({"title": "experience 1", "category": "Paseo"})
    exp2 = create_experience({"title": "experience 2", "category": "Gastronomía"})
    exp3 = create_experience({"title": "experience 3", "category": "Paseo"})
    exp4 = create_experience({"title": "experience 4", "category": "Aire Libre"})

    response = client.get(f"{URI}?category=Paseo")
    data = response.json()

    data_titles = map(lambda e: e['title'], data)

    assert len(data) == 2
    assert all(map(lambda e: e['title'] in data_titles, [exp1, exp3]))
    assert not any(map(lambda e: e['title'] in data_titles, [exp2, exp4]))


def test_search_experience_by_owner():
    exp1 = create_experience({"title": "experience 1", "owner": "omar"})
    exp2 = create_experience({"title": "experience 2", "owner": "juan"})
    exp3 = create_experience({"title": "experience 3", "owner": "omar"})
    exp4 = create_experience({"title": "experience 4", "owner": "gabriel"})

    response = client.get(f"{URI}?owner=omar")
    data = response.json()

    data_titles = map(lambda e: e['title'], data)

    assert len(data) == 2
    assert all(map(lambda e: e['title'] in data_titles, [exp1, exp3]))
    assert not any(map(lambda e: e['title'] in data_titles, [exp2, exp4]))


def test_search_experience_by_location():
    exp1 = create_experience(
        {
            "title": "experience 1",
            "location": {'description': 'location', 'lat': 24.0, 'lng': 24.0},
        }
    )
    exp2 = create_experience(
        {
            "title": "experience 2",
            "location": {'description': 'location', 'lat': 24.0, 'lng': 40.0},
        }
    )
    exp3 = create_experience(
        {
            "title": "experience 3",
            "location": {'description': 'location', 'lat': 24.0, 'lng': 23.0},
        }
    )
    exp4 = create_experience(
        {
            "title": "experience 4",
            "location": {'description': 'location', 'lat': -10.0, 'lng': 24.0},
        }
    )

    response = client.get(f"{URI}?lat=24&lng=23.5&dist=105000")
    data = response.json()

    data_titles = list(map(lambda e: e['title'], data))

    assert len(data) == 2
    assert all(map(lambda e: e['title'] in data_titles, [exp1, exp3]))
    assert not any(map(lambda e: e['title'] in data_titles, [exp2, exp4]))


def test_search_experience_without_filters_returns_everything():
    exp1 = create_experience(
        {"title": "experience 1", "owner": "omar", "category": "Paseo"}
    )
    exp2 = create_experience(
        {"title": "experience 2", "owner": "juan", "category": "Gastronomía"}
    )
    exp3 = create_experience(
        {"title": "experience 3", "owner": "Gastronomía", "category": "Paseo"}
    )
    exp4 = create_experience(
        {"title": "experience 4", "owner": "omar", "category": "Aire Libre"}
    )

    response = client.get(f"{URI}")
    data = response.json()

    data_titles = map(lambda e: e['title'], data)

    assert len(data) == 4
    assert all(map(lambda e: e['title'] in data_titles, [exp1, exp2, exp3, exp4]))


def test_search_experience_with_multiple_filters():
    exp1 = create_experience(
        {"title": "experience 1", "owner": "omar", "category": "Paseo"}
    )
    exp2 = create_experience(
        {"title": "experience 2", "owner": "juan", "category": "Gastronomía"}
    )
    exp3 = create_experience(
        {"title": "experience 3", "owner": "Gastronomía", "category": "Paseo"}
    )
    exp4 = create_experience(
        {"title": "experience 4", "owner": "omar", "category": "Aire Libre"}
    )

    response = client.get(f"{URI}?category=Paseo&owner=omar")
    data = response.json()

    data_titles = map(lambda e: e['title'], data)

    assert len(data) == 1
    assert all(map(lambda e: e['title'] in data_titles, [exp1]))
    assert not any(map(lambda e: e['title'] in data_titles, [exp2, exp3, exp4]))


def test_search_experience_with_limit_returns_given_amount():
    create_experience({"title": "experience 1", "owner": "omar", "category": "Paseo"})
    create_experience(
        {"title": "experience 2", "owner": "juan", "category": "Gastronomía"}
    )
    create_experience(
        {"title": "experience 3", "owner": "Gastronomía", "category": "Paseo"}
    )
    create_experience(
        {"title": "experience 4", "owner": "omar", "category": "Aire Libre"}
    )

    response = client.get(f"{URI}?limit=3")
    data = response.json()

    assert len(data) == 3
