from flask_restful import Resource, marshal_with, abort
from app.dal.user import UserDAL
from app.dal.user import UserModel
from app.resources.decorators import requires_auth

class Users(Resource):
    def __init__(self, user_dal: UserDAL):
        self.user_dal = user_dal

    @requires_auth()
    @marshal_with(UserModel.fields())
    def get(self) -> list[UserModel]:
        users = self.user_dal.get_all_users()
        return users
    
    @requires_auth()
    @marshal_with(UserModel.fields())
    def post(self) -> list[UserModel]:
        try:
            users = self.user_dal.post_user()
            return users
        except ValueError as e:
            abort(400, message=f"{e}")

class User(Resource):
    def __init__(self, user_dal: UserDAL):
        self.user_dal = user_dal

    @requires_auth()
    @marshal_with(UserModel.fields())
    def get(self, id: str) -> UserModel:
        try:
            user = self.user_dal.get_user(id)
            return user
        except ValueError as e:
            abort(400, message=f"{e}")

    @requires_auth()
    @marshal_with(UserModel.fields())
    def patch(self, id: str) -> UserModel:
        try:
            user = self.user_dal.patch_user(id)
            return user
        except ValueError as e:
            abort(400, message=f"{e}")
