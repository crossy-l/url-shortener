from base64 import b64encode
import pytest
from flask import Flask
from app.database.database import ApiDatabase
from app.resources.users import Users
from app.resources.urls import Urls
from app.dal.sql.user import SQLiteUserDAL
from app.dal.sql.url import SQLiteUrlDAL
from flask_restful import Api

@pytest.fixture
def test_app(database):
    app = Flask(__name__)
    app.config["TESTING"] = True
    api = Api(app)

    user_dal = SQLiteUserDAL(database.session)
    user_dal.write_user(name="admin", password="Admin@1234")
    url_dal = SQLiteUrlDAL(database.session)

    api.add_resource(Users, '/users', resource_class_kwargs={'user_dal': user_dal})
    api.add_resource(Urls, '/urls', resource_class_kwargs={'user_dal': user_dal, 'url_dal': url_dal})
    return app

def encode_auth(username, password):
    """Helper to encode basic auth credentials."""
    credentials = f"{username}:{password}"
    return b64encode(credentials.encode("utf-8")).decode("utf-8")

@pytest.fixture
def header():
    return {"Authorization": f"Basic {encode_auth('admin', 'Admin@1234')}"}

def test_get_users(test_app, header):
    with test_app.test_client() as client:
        response = client.get("/users")
        assert response.status_code == 401
        response = client.get("/users", headers=header)
        assert response.status_code == 200

def test_post_users(test_app, header):
    json = {"name": "testuser", "password": "Test@1234"}
    with test_app.test_client() as client:
        response = client.post("/users", json=json)
        assert response.status_code == 401
        response = client.post("/users", json=json, headers=header)
        assert response.status_code == 201
        assert response.json["name"] == "testuser"

def test_post_url(test_app, header):
    json = {"alias": "testalias", "target": "http://example.com"}
    with test_app.test_client() as client:
        response = client.post("/urls", json=json)
        assert response.status_code == 401
        response = client.post("/urls", json=json, headers=header)
        assert response.status_code == 201
        assert response.json["alias"] == "testalias"
