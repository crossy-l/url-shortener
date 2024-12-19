from app.dal.sql.user import SQLiteUserDAL
from app.database.database import ApiDatabase
from app.resources.users import Users, User

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
