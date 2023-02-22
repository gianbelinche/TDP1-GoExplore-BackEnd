from fastapi.testclient import TestClient
from pprint import pprint
import pytest
from test.utils import generate_invalid

from app.app import app

client = TestClient(app)

URI = 'api/bookings'
USERS_URI = 'api/users'
EXPERIENCIES_URI = 'api/experiences'
RESERVED_URI = "bookings_reserved"
RECEIVED_URI = "bookings_received"


def create_user(fields={}):
    body = {
        'first_name': 'first_name',
        'last_name': 'last_name',
        'email': 'email@mail.com',
        'host': False,
        'password': "1234",
        "birth_date": "1990-01-01",
    }

    for k, v in fields.items():
        body[k] = v

    response = client.post("api/users", json=body)
    return response.json()


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
        'category': 'Food',
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


def test_booking_create_succesfully():

    user = create_user({'email': 'email@mail.com'})
    reserver = create_user({'email': 'reserver@mail.com'})
    experience = create_experience({'owner': user['id']})

    booking_body = {
        "experience_id": experience['id'],
        "reserver_id": reserver['id'],
        "date": "2022-12-13",
        "owner_id": user['id'],
    }

    response = client.post(URI, json=booking_body)
    response_data = response.json()

    assert response.status_code == 201
    assert 'id' in response_data
    booking_body["id"] = response_data["id"]
    assert response_data == booking_body


def test_booking_create_with_missing_data():

    user = create_user({'email': 'email@mail.com'})
    reserver = create_user({'email': 'reserver@mail.com'})
    experience = create_experience({'owner': user['id']})

    booking_body = {
        "experience_id": experience['id'],
        "reserver_id": reserver['id'],
        "date": "2022-12-13",
        "owner_id": user['id'],
    }

    invalid_variations = {
        'experience_id': [None, '', 'aa'],
        'reserver_id': [None, '', 'aa'],
        'date': [None, '', 'aa'],
        'owner_id': [None, '', 'aa'],
    }

    invalid_bodies = generate_invalid(booking_body, invalid_variations)

    for inv_body in invalid_bodies:
        response = client.post(URI, json=inv_body)
        try:
            assert response.status_code == 422
        except Exception:
            print("Failed body: \n")
            pprint(inv_body)
            raise


def test_booking_create_duplicated():
    user = create_user({'email': 'email@mail.com'})
    reserver = create_user({'email': 'reserver@mail.com'})
    experience = create_experience({'owner': user['id']})

    booking_body = {
        "experience_id": experience['id'],
        "reserver_id": reserver['id'],
        "date": "2022-12-13",
        "owner_id": user['id'],
    }

    client.post(URI, json=booking_body)
    response = client.post(URI, json=booking_body)
    response_data = response.json()

    assert response.status_code == 400
    assert response_data['detail'] == "Booking already exists"


def test_booking_create_with_2_reservers():

    user = create_user({'email': 'email@mail.com'})
    reserver1 = create_user({'email': 'reserver@mail.com'})
    reserver2 = create_user({'email': 'reserver2@mail.com'})
    experience = create_experience({'owner': user['id']})

    booking_body1 = {
        "experience_id": experience['id'],
        "reserver_id": reserver1['id'],
        "date": "2022-12-13",
        "owner_id": user['id'],
    }

    booking_body2 = {
        "experience_id": experience['id'],
        "reserver_id": reserver2['id'],
        "date": "2022-12-13",
        "owner_id": user['id'],
    }

    response1 = client.post(URI, json=booking_body1)
    response2 = client.post(URI, json=booking_body2)
    response_data1 = response1.json()
    response_data2 = response2.json()

    assert response1.status_code == 201
    assert 'id' in response_data1
    booking_body1["id"] = response_data1["id"]
    assert response_data1 == booking_body1

    assert response2.status_code == 201
    assert 'id' in response_data2
    booking_body2["id"] = response_data2["id"]
    assert response_data2 == booking_body2


def test_booking_create_2_same_user_different_date():
    user = create_user({'email': 'email@mail.com'})
    reserver = create_user({'email': 'reserver@mail.com'})
    experience = create_experience({'owner': user['id']})

    booking_body1 = {
        "experience_id": experience['id'],
        "reserver_id": reserver['id'],
        "date": "2022-12-13",
        "owner_id": user['id'],
    }

    booking_body2 = {
        "experience_id": experience['id'],
        "reserver_id": reserver['id'],
        "date": "2022-12-14",
        "owner_id": user['id'],
    }

    response1 = client.post(URI, json=booking_body1)
    response2 = client.post(URI, json=booking_body2)
    response_data1 = response1.json()
    response_data2 = response2.json()

    assert response1.status_code == 201
    assert 'id' in response_data1
    booking_body1["id"] = response_data1["id"]
    assert response_data1 == booking_body1

    assert response2.status_code == 201
    assert 'id' in response_data2
    booking_body2["id"] = response_data2["id"]
    assert response_data2 == booking_body2


def test_booking_get_by_reserver_empty():
    reserver = create_user()
    reserver_id = reserver['id']

    response = client.get(USERS_URI + f"/{reserver_id}/" + RESERVED_URI)
    assert response.status_code == 200
    assert response.json() == []


def test_booking_get_by_reserver_one():
    user = create_user({'email': 'email@mail.com'})
    reserver = create_user({'email': 'reserver@mail.com'})
    experience = create_experience({'owner': user['id']})

    booking_body = {
        "experience_id": experience['id'],
        "reserver_id": reserver['id'],
        "date": "2022-12-13",
        "owner_id": user['id'],
    }

    client.post(URI, json=booking_body)
    reserver_id = reserver['id']

    response = client.get(USERS_URI + f"/{reserver_id}/" + RESERVED_URI)
    assert response.status_code == 200
    data = response.json()
    assert len(data) == 1
    booking_body["id"] = data[0]["id"]
    assert data[0] == booking_body


def test_booking_get_by_reserver_two():
    user = create_user({'email': 'email@mail.com'})
    reserver = create_user({'email': 'reserver@mail.com'})
    experience = create_experience({'owner': user['id']})

    booking_body1 = {
        "experience_id": experience['id'],
        "reserver_id": reserver['id'],
        "date": "2022-12-13",
        "owner_id": user['id'],
    }

    booking_body2 = {
        "experience_id": experience['id'],
        "reserver_id": reserver['id'],
        "date": "2022-12-14",
        "owner_id": user['id'],
    }
    reserver_id = reserver['id']

    client.post(URI, json=booking_body1)
    client.post(URI, json=booking_body2)

    response = client.get(USERS_URI + f"/{reserver_id}/" + RESERVED_URI)

    assert response.status_code == 200
    data = response.json()
    assert len(data) == 2
    booking_body1["id"] = data[0]["id"]
    booking_body2["id"] = data[1]["id"]
    assert data[0] == booking_body1
    assert data[1] == booking_body2


def test_booking_get_by_owner_empty():
    owner = create_user()
    owner_id = owner['id']

    response = client.get(USERS_URI + f"/{owner_id}/" + RECEIVED_URI)
    assert response.status_code == 200
    assert response.json() == []


def test_booking_get_by_owner_one():
    user = create_user({'email': 'email@mail.com'})
    reserver = create_user({'email': 'reserver@mail.com'})
    experience = create_experience({'owner': user['id']})

    booking_body = {
        "experience_id": experience['id'],
        "reserver_id": reserver['id'],
        "date": "2022-12-13",
        "owner_id": user['id'],
    }
    user_id = user['id']

    client.post(URI, json=booking_body)
    response = client.get(USERS_URI + f"/{user_id}/" + RECEIVED_URI)
    assert response.status_code == 200
    data = response.json()
    assert len(data) == 1
    booking_body["id"] = data[0]["id"]
    assert data[0] == booking_body


def test_booking_get_by_owner_two():
    user = create_user({'email': 'email@mail.com'})
    reserver1 = create_user({'email': 'reserver1@mail.com'})
    reserver2 = create_user({'email': 'reserver2@mail.com'})
    experience = create_experience({'owner': user['id']})

    booking_body1 = {
        "experience_id": experience['id'],
        "reserver_id": reserver1['id'],
        "date": "2022-12-13",
        "owner_id": user['id'],
    }
    booking_body2 = {
        "experience_id": experience['id'],
        "reserver_id": reserver2['id'],
        "date": "2022-12-13",
        "owner_id": user['id'],
    }
    client.post(URI, json=booking_body1)
    client.post(URI, json=booking_body2)

    user_id = user['id']

    response = client.get(USERS_URI + f"/{user_id}/" + RECEIVED_URI)
    data = response.json()

    booking_body1["id"] = data[0]["id"]
    booking_body2["id"] = data[1]["id"]

    assert response.status_code == 200
    assert len(data) == 2
    assert data[0] == booking_body1
    assert data[1] == booking_body2
