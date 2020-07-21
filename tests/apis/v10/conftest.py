from datetime import datetime

import pytest
import requests
from faker import Faker
from requests.auth import HTTPBasicAuth

from tests.apis.constants import DB_CONFIGS, TEST_USER_USERNAME, TEST_USER_PASSWORD, TEST_USER_EMAIL, BASE_URL
from wrappers.py_sql import PySQL


@pytest.fixture
def user():
    py_sql = PySQL(**DB_CONFIGS)
    py_sql.query = """
    SELECT id 
    FROM user
    WHERE username = %s
    """
    py_sql.params = [TEST_USER_USERNAME]
    user = py_sql.fetch_one()
    return user


@pytest.fixture
def test_user(user):
    if not user:
        data = {
            'username': TEST_USER_USERNAME,
            'email': TEST_USER_EMAIL,
            'password': TEST_USER_PASSWORD,
            'user_type': 1,
            'address': 'Sialkot'
        }
        url = BASE_URL.format('/v10/signup')
        authentication = HTTPBasicAuth('lpHaNdeS', 'KdaAdL$KKJ$Sgf!%ebWp')
        requests.post(url, data=data, auth=authentication)


@pytest.fixture()
def user_id():
    py_sql = PySQL(**DB_CONFIGS)
    py_sql.query = """
    SELECT id 
    FROM user
    WHERE username = %s
    """
    py_sql.params = [TEST_USER_USERNAME]
    user_data = py_sql.fetch_one()
    user_id = user_data.get('id')
    return user_id


@pytest.fixture
def user_dishes_ids(user_id):
    dishes_ids = []
    py_sql = PySQL(**DB_CONFIGS)
    py_sql.query = """
    SELECT id 
    FROM dish
    WHERE user_id = %s
    """
    py_sql.params = [user_id]
    _dishes_ids = py_sql.fetch_all()
    for dish_id in _dishes_ids:
        _dish_id = dish_id.get('id')
        dishes_ids.append(_dish_id)
    return dishes_ids


@pytest.fixture
def remove_dishes_ingredients(user_dishes_ids):
    if user_dishes_ids:
        py_sql = PySQL(**DB_CONFIGS)
        py_sql.query = """
        DELETE
        FROM ingredient
        WHERE dish_id in (%s)
        """
        py_sql.params = tuple(user_dishes_ids)
        py_sql.save_changes()


@pytest.fixture
def add_dishes(user_id):
    faker = Faker()
    py_sql = PySQL(**DB_CONFIGS)
    dish_limit = 5  # one dish is already added by case 1
    while dish_limit != 0:
        py_sql.query = """
        INSERT INTO dish(id, name, price, unit, image_url, small_image_url, created_date, updated_date, user_id)
        VALUES(%s, %s, %s, %s, %s, %s, %s, %s, %s)
        """
        py_sql.params = [
            0, faker.name(), 200, 'grams', '', '', datetime.now(), datetime.now(), user_id
        ]
        py_sql.save_changes()
        dish_limit -= 1


@pytest.fixture
def remove_dishes(user_id, remove_dishes_ingredients):
    py_sql = PySQL(**DB_CONFIGS)
    py_sql.query = """
    DELETE
    FROM dish
    WHERE user_id = %s
    """
    py_sql.params = [user_id]
    py_sql.save_changes()
