from flask_restful import Resource, marshal_with, abort
from app.dal.user import UserDAL
from app.dal.url import UrlDAL, UrlModel
from app.resources.decorators import requires_auth, handle_error

class Urls(Resource):
    def __init__(self, user_dal: UserDAL, url_dal: UrlDAL):
        self.user_dal = user_dal
        self.url_dal = url_dal

    @handle_error()
    @requires_auth()
    @marshal_with(UrlModel.fields())
    def get(self) -> list[UrlModel]:
        urls = self.url_dal.get_all_urls()
        return urls
    
    @handle_error()
    @requires_auth()
    @marshal_with(UrlModel.fields())
    def post(self) -> list[UrlModel]:
        users = self.url_dal.post_url()
        return users, 201


class Url(Resource):
    def __init__(self, user_dal: UserDAL, url_dal: UrlDAL):
        self.user_dal = user_dal
        self.url_dal = url_dal

    @handle_error()
    @marshal_with(UrlModel.fields())
    def get(self, id: str) -> UrlModel:
        user = self.url_dal.get_url(id)
        return user

    @handle_error()
    @requires_auth()
    @marshal_with(UrlModel.fields())
    def patch(self, id: str) -> UrlModel:
        user = self.url_dal.patch_url(id)
        return user

    @handle_error()
    @requires_auth()
    def delete(self, id: str) -> UrlModel:
        message = self.url_dal.delete_url(id)
        return message, 200
