import sys
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "../..")))

import pytest
from flask import Flask
from app.database.database import ApiDatabase

@pytest.fixture
def app():
    app = Flask(__name__)
    app.config["TESTING"] = True
    app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///:memory:"
    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
    return app

@pytest.fixture
def database(app):
    db = ApiDatabase(app, None)
    db.create_tables()
    yield db
    db.drop_tables()

@pytest.fixture
def session(database):
    return database.session
