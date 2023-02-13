from fastapi.testclient import TestClient
import pytest
from test.utils import generate_invalid

from app.app import app

client = TestClient(app)

URI = 'api/bookings'
USERS_URI = 'api/users'
EXPERIENCIES_URI = 'api/experiencies'


@pytest.fixture(autouse=True)
def clear_db():
    # This runs before each test

    yield

    # Ant this runs after each test
    client.post('api/reset')


# def test_get_user_not_exists():
#    response = client.get(URI + "/notexists")
#    data = response.json()
#    assert response.status_code == 404
#    assert data['detail'] == "User not found"


def test_booking_create_succesfully():
    user_body = {
        'first_name': 'first_name',
        'last_name': 'last_name',
        'email': 'email@mail.com',
        'password': "1234",
        "birth_date": "1990-01-01",
    }
    user_id = client.post(USERS_URI, json=user_body).json()["id"]
    reserver_body = {
        'first_name': 'first_name',
        'last_name': 'last_name',
        'email': 'reserver@mail.com',
        'password': "1234",
        "birth_date": "1990-01-01",
    }
    reserver_id = client.post(USERS_URI, json=reserver_body).json()["id"]
    exp_body = {
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
        'owner': user_id,
    }
    experience_id = client.post(EXPERIENCIES_URI, json=exp_body).json()["id"]
    booking_body = {
        "experience_id": experience_id,
        "reserver_id": reserver_id,
        "date": "2022-12-13",
        "owner_id": user_id,
    }
    response = client.post(URI, json=booking_body)
    response_data = response.json()
    assert response.status_code == 201
    assert 'id' in response_data
    booking_body["id"] = response_data["id"]
    assert response_data == booking_body


def test_booking_create_with_missing_data():
    user_body = {
        'first_name': 'first_name',
        'last_name': 'last_name',
        'email': 'email@mail.com',
        'password': "1234",
        "birth_date": "1990-01-01",
    }
    user_id = client.post(USERS_URI, json=user_body).json()["id"]
    reserver_body = {
        'first_name': 'first_name',
        'last_name': 'last_name',
        'email': 'reserver@mail.com',
        'password': "1234",
        "birth_date": "1990-01-01",
    }
    reserver_id = client.post(USERS_URI, json=reserver_body).json()["id"]
    exp_body = {
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
        'owner': user_id,
    }
    experience_id = client.post(EXPERIENCIES_URI, json=exp_body).json()["id"]
    booking_body = {
        "experience_id": experience_id,
        "reserver_id": reserver_id,
        "date": "2022-12-13",
        "owner_id": user_id,
    }
    invalid_variations = {
        'experience_id': [None, '', 'aa'],
        'reserver_id': [None, '', 'aa'],
        'date': [None, '', 'aa'],
        'owner_id': [None, '', 'aa'],
    }

    invalid_bodies = generate_invalid(booking_body, invalid_variations)

    # NOTE: If one of this tests fails, we don´t get enough information
    # we just know that the hole suit failed.

    for inv_body in invalid_bodies:
        response = client.post(URI, json=inv_body)
        assert response.status_code == 422


def test_booking_create_succesfully_twice():
    user_body = {
        'first_name': 'first_name',
        'last_name': 'last_name',
        'email': 'email@mail.com',
        'password': "1234",
        "birth_date": "1990-01-01",
    }
    user_id = client.post(USERS_URI, json=user_body).json()["id"]
    reserver_body = {
        'first_name': 'first_name',
        'last_name': 'last_name',
        'email': 'reserver@mail.com',
        'password': "1234",
        "birth_date": "1990-01-01",
    }
    reserver_id = client.post(USERS_URI, json=reserver_body).json()["id"]
    exp_body = {
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
        'owner': user_id,
    }
    experience_id = client.post(EXPERIENCIES_URI, json=exp_body).json()["id"]
    booking_body = {
        "experience_id": experience_id,
        "reserver_id": reserver_id,
        "date": "2022-12-13",
        "owner_id": user_id,
    }
    response = client.post(URI, json=booking_body)
    response_data = response.json()
    assert response.status_code == 201
    assert 'id' in response_data
    booking_body["id"] = response_data["id"]
    assert response_data == booking_body

    user_body2 = {
        'first_name': 'first_name',
        'last_name': 'last_name',
        'email': 'email2@mail.com',
        'password': "1234",
        "birth_date": "1990-01-01",
    }
    user_id2 = client.post(USERS_URI, json=user_body2).json()["id"]
    reserver_body2 = {
        'first_name': 'first_name',
        'last_name': 'last_name',
        'email': 'reserver2@mail.com',
        'password': "1234",
        "birth_date": "1990-01-01",
    }
    reserver_id2 = client.post(USERS_URI, json=reserver_body2).json()["id"]
    exp_body2 = {
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
        'owner': user_id2,
    }
    experience_id2 = client.post(EXPERIENCIES_URI, json=exp_body2).json()["id"]
    booking_body2 = {
        "experience_id": experience_id2,
        "reserver_id": reserver_id2,
        "date": "2022-12-13",
        "owner_id": user_id2,
    }
    response = client.post(URI, json=booking_body2)
    response_data = response.json()
    assert response.status_code == 201
    assert 'id' in response_data
    booking_body2["id"] = response_data["id"]
    assert response_data == booking_body2


def test_booking_create_duplicated():
    user_body = {
        'first_name': 'first_name',
        'last_name': 'last_name',
        'email': 'email@mail.com',
        'password': "1234",
        "birth_date": "1990-01-01",
    }
    user_id = client.post(USERS_URI, json=user_body).json()["id"]
    reserver_body = {
        'first_name': 'first_name',
        'last_name': 'last_name',
        'email': 'reserver@mail.com',
        'password': "1234",
        "birth_date": "1990-01-01",
    }
    reserver_id = client.post(USERS_URI, json=reserver_body).json()["id"]
    exp_body = {
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
        'owner': user_id,
    }
    experience_id = client.post(EXPERIENCIES_URI, json=exp_body).json()["id"]
    booking_body = {
        "experience_id": experience_id,
        "reserver_id": reserver_id,
        "date": "2022-12-13",
        "owner_id": user_id,
    }
    client.post(URI, json=booking_body)
    response = client.post(URI, json=booking_body)
    data = response.json()
    assert response.status_code == 400
    assert data['detail'] == "Booking already exists"


def test_booking_create_with_2_reservers():
    user_body = {
        'first_name': 'first_name',
        'last_name': 'last_name',
        'email': 'email@mail.com',
        'password': "1234",
        "birth_date": "1990-01-01",
    }
    user_id = client.post(USERS_URI, json=user_body).json()["id"]
    reserver_body1 = {
        'first_name': 'first_name',
        'last_name': 'last_name',
        'email': 'reserver@mail.com',
        'password': "1234",
        "birth_date": "1990-01-01",
    }
    reserver_id1 = client.post(USERS_URI, json=reserver_body1).json()["id"]
    reserver_body2 = {
        'first_name': 'first_name',
        'last_name': 'last_name',
        'email': 'reserver2@mail.com',
        'password': "1234",
        "birth_date": "1990-01-01",
    }
    reserver_id2 = client.post(USERS_URI, json=reserver_body2).json()["id"]
    exp_body = {
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
        'owner': user_id,
    }
    experience_id = client.post(EXPERIENCIES_URI, json=exp_body).json()["id"]
    booking_body1 = {
        "experience_id": experience_id,
        "reserver_id": reserver_id1,
        "date": "2022-12-13",
        "owner_id": user_id,
    }
    booking_body2 = {
        "experience_id": experience_id,
        "reserver_id": reserver_id2,
        "date": "2022-12-13",
        "owner_id": user_id,
    }
    response = client.post(URI, json=booking_body1)
    response_data = response.json()
    assert response.status_code == 201
    assert 'id' in response_data
    booking_body1["id"] = response_data["id"]
    assert response_data == booking_body1

    response = client.post(URI, json=booking_body2)
    response_data = response.json()
    assert response.status_code == 201
    assert 'id' in response_data
    booking_body2["id"] = response_data["id"]
    assert response_data == booking_body2
