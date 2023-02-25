from fastapi.testclient import TestClient
import pytest

from app.app import app

client = TestClient(app)


def favourites_uri(id: str):
    return f"api/users/{id}/favourites"


def delete_favourites_uri(user_id: str, experience_id: str):
    return f"api/users/{user_id}/favourites/{experience_id}"


def create_user():
    body = {
        'first_name': 'first_name',
        'last_name': 'last_name',
        'email': 'email@mail.com',
        'password': "1234",
        'host': False,
        'identification_number': '40400400',
        'phone_number': '1180808080',
        "birth_date": "1990-01-01",
    }
    response = client.post("api/users", json=body)
    return response.json()


def create_experience():
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

    response = client.post("api/experiences", json=body)
    return response.json()


@pytest.fixture(autouse=True)
def clear_db():
    # This runs before each test

    yield

    # Ant this runs after each test
    client.post('api/reset')


def test_user_not_exists():
    response = client.get(favourites_uri('notexists'))
    data = response.json()
    assert response.status_code == 400
    assert data['detail'] == "User not found"


def test_user_without_favourites():
    # Create user
    user = create_user()
    user_id = user['id']

    # Get user favourites
    response = client.get(favourites_uri(user_id))
    data = response.json()
    assert response.status_code == 200
    assert data == []


def test_create_favourite_succesfully():
    # Create user
    user = create_user()
    user_id = user['id']

    # Create experience
    experience = create_experience()
    experience_id = experience['id']

    # Create favourite

    favourite = {'experience_id': experience_id}

    response = client.post(favourites_uri(user_id), json=favourite)

    assert response.status_code == 201
    assert response.json() == favourite


def test_user_with_one_favourite():
    # Create user
    user = create_user()
    user_id = user['id']

    # Create experience
    experience = create_experience()
    experience_id = experience['id']

    # Create favourite
    favourite = {'experience_id': experience_id}
    client.post(favourites_uri(user_id), json=favourite)

    # Get user favourites
    response = client.get(favourites_uri(user_id))
    data = response.json()

    assert response.status_code == 200
    assert data == [experience]


def test_user_with_multiple_favourites():
    # Create user
    user = create_user()
    user_id = user['id']

    # Create first experience
    experience_1 = create_experience()
    experience_id = experience_1['id']

    # Create first favourite
    favourite = {'experience_id': experience_id}
    client.post(favourites_uri(user_id), json=favourite)

    # Create second experience
    experience_2 = create_experience()
    experience_id = experience_2['id']

    # Create second favourite
    favourite = {'experience_id': experience_id}
    client.post(favourites_uri(user_id), json=favourite)

    # Get user favourites
    response = client.get(favourites_uri(user_id))
    data = response.json()

    assert response.status_code == 200
    assert len(data) == 2
    assert experience_1 in data
    assert experience_2 in data


def test_create_favourite_user_not_exists():
    # Create experience
    experience = create_experience()
    experience_id = experience['id']

    # Create favourite
    favourite = {'experience_id': experience_id}
    response = client.post(favourites_uri('notexists'), json=favourite)
    data = response.json()

    assert response.status_code == 400
    assert data['detail'] == 'User not found'


def test_create_favourite_experience_not_exists():
    # Create user
    user = create_user()
    user_id = user['id']

    # Create favourite
    favourite = {'experience_id': 'notexists'}
    response = client.post(favourites_uri(user_id), json=favourite)
    data = response.json()

    assert response.status_code == 400
    assert data['detail'] == 'Experience not found'


def test_delete_favourite_returns_empty_array():
    # Create user
    user = create_user()
    user_id = user['id']

    # Create experience
    experience = create_experience()
    experience_id = experience['id']

    # Create favourite
    favourite = {'experience_id': experience_id}
    client.post(favourites_uri(user_id), json=favourite)

    # Delete favourite
    delete_response = client.delete(
        delete_favourites_uri(user_id=user_id, experience_id=experience_id)
    )

    # Get user favourites
    get_response = client.get(favourites_uri(user_id))
    data = get_response.json()

    assert delete_response.status_code == 200
    assert get_response.status_code == 200
    assert data == []


def test_delete_favourite_user_with_multiple_favourites():
    # Create user
    user = create_user()
    user_id = user['id']

    # Create first experience
    experience_1 = create_experience()
    experience_id = experience_1['id']

    # Create first favourite
    favourite = {'experience_id': experience_id}
    client.post(favourites_uri(user_id), json=favourite)

    # Create second experience
    experience_2 = create_experience()
    experience_id = experience_2['id']

    # Create second favourite
    favourite = {'experience_id': experience_id}
    client.post(favourites_uri(user_id), json=favourite)

    # Delete favourite
    client.delete(
        delete_favourites_uri(user_id=user_id, experience_id=experience_1['id'])
    )

    # Get user favourites
    response = client.get(favourites_uri(user_id))
    data = response.json()

    assert response.status_code == 200
    assert len(data) == 1
    assert experience_1 not in data
    assert experience_2 in data


def test_delete_favourite_user_not_exist():
    user_id = 'not-exists'
    experience_id = 'not-exists'

    response = client.delete(
        delete_favourites_uri(user_id=user_id, experience_id=experience_id)
    )

    data = response.json()

    assert response.status_code == 400
    assert data['detail'] == 'User not found'


def test_delete_favourite_favourite_not_exist_is_ignored():
    user = create_user()
    user_id = user['id']
    experience_id = 'not-exists'

    response = client.delete(
        delete_favourites_uri(user_id=user_id, experience_id=experience_id)
    )

    # Get user favourites
    favourites_response = client.get(favourites_uri(user_id))
    favourites = favourites_response.json()

    assert response.status_code == 200
    assert favourites == []
