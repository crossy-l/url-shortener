# factory.py
from flask_restful import Resource
from dal import SQLiteUserDAL
from database import ApiDatabase, UserModel
from resources import Users

def create_users(database: ApiDatabase):
    return SQLiteUserDAL(database.session)

def create_users_resource(database: ApiDatabase):
    class UsersResource(Users):
        def __init__(self):
            super().__init__(create_users(database))
    return UsersResource
