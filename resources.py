from functools import wraps
from flask_restful import Resource, marshal_with, abort
from dal import UserDAL
from database import UserModel
from flask import request
from passwords import PasswordManager

def requires_auth():
    def decorator(func):
        @wraps(func)
        def wrapper(self, *args, **kwargs):
            if not hasattr(self, "user_dal"):
                raise AttributeError("The attribute 'user_dal' is not defined on the resource.")
            try:
                user_dal = self.user_dal
                name, password = PasswordManager.get_auth_credentials(request.headers)
                if not user_dal.validate_auth(name, password):
                    abort(401, message="Invalid password")
            except Exception as e:
                abort(401, message=f"Failed auth: {e}")
            return func(self, *args, **kwargs)
        return wrapper
    return decorator

class Users(Resource):
    def __init__(self, user_dal: UserDAL):
        self.user_dal = user_dal

    @requires_auth()
    @marshal_with(UserModel.fields())
    def get(self):
        users = self.user_dal.get_all_users()
        return users
    
    @requires_auth()
    @marshal_with(UserModel.fields())
    def post(self):
        try:
            users = self.user_dal.post_user()
            return users
        except ValueError as e:
            abort(400, message=f"{e}")