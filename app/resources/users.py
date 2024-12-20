from flask_restful import Resource, marshal_with, abort
from app.dal.user import UserDAL
from app.dal.user import UserModel
from app.resources.decorators import requires_auth, handle_error

class Users(Resource):
    def __init__(self, user_dal: UserDAL):
        self.user_dal = user_dal

    @handle_error()
    @requires_auth()
    @marshal_with(UserModel.fields())
    def get(self) -> list[UserModel]:
        users = self.user_dal.get_all_users()
        return users
    
    @handle_error()
    @requires_auth()
    @marshal_with(UserModel.fields())
    def post(self) -> list[UserModel]:
        users = self.user_dal.post_user()
        return users, 201


class User(Resource):
    def __init__(self, user_dal: UserDAL):
        self.user_dal = user_dal

    @handle_error()
    @requires_auth()
    @marshal_with(UserModel.fields())
    def get(self, id: str) -> UserModel:
        user = self.user_dal.get_user(id)
        return user

    @handle_error()
    @requires_auth()
    @marshal_with(UserModel.fields())
    def patch(self, id: str) -> UserModel:
        user = self.user_dal.patch_user(id)
        return user

    @handle_error()
    @requires_auth()
    def delete(self, id: str) -> UserModel:
        message = self.user_dal.delete_user(id)
        return message, 200
