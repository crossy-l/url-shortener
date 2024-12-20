from app.dal.sql.user import SQLiteUserDAL
from app.dal.sql.url import SQLiteUrlDAL
from app.database.database import ApiDatabase
from app.resources.users import Users, User
from app.resources.urls import Urls, Url
from app.resources.home import Home

def create_users(database: ApiDatabase):
    return SQLiteUserDAL(database.session)

def create_users_resource(database: ApiDatabase):
    class UsersResource(Users):
        def __init__(self):
            super().__init__(create_users(database))
    return UsersResource

def create_user_resource(database: ApiDatabase):
    class UserResource(User):
        def __init__(self):
            super().__init__(create_users(database))
    return UserResource



def create_urls(database: ApiDatabase):
    return SQLiteUrlDAL(database.session)

def create_urls_resource(database: ApiDatabase):
    class UrlsResource(Urls):
        def __init__(self):
            super().__init__(user_dal=create_users(database), url_dal=create_urls(database))
    return UrlsResource

def create_url_resource(database: ApiDatabase):
    class UrlResource(Url):
        def __init__(self):
            super().__init__(user_dal=create_users(database), url_dal=create_urls(database))
    return UrlResource



def create_home_resource(database: ApiDatabase):
    class HomeResource(Home):
        def __init__(self):
            super().__init__(url_dal=create_urls(database))
    return HomeResource