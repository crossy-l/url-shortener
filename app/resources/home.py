from flask_restful import Resource
from flask import redirect
from app.dal.url import UrlDAL
from app.resources.decorators import requires_auth, handle_error

class Home(Resource):
    def __init__(self, url_dal: UrlDAL):
        self.url_dal = url_dal

    @handle_error()
    def get(self, alias: str):
        url = self.url_dal.get_url(alias)
        self.url_dal.increase_redirects(url)
        return redirect(url.target)