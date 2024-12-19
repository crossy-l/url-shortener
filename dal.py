from functools import wraps
from typing import List
from database import UserModel
from flask_restful import request, abort
from passwords import PasswordManager

def is_weak_password(password: str) -> bool:
    return password.isspace() or len(password) < 8


class UserDAL:
    def get_all_users(self) -> List[UserModel]:
        raise NotImplementedError()
    
    def fetch_user_by_name(self, name) -> UserModel:
        raise NotImplementedError()
    
    def post_user(self) -> List[UserModel]:
        raise NotImplementedError()
    
    def validate_auth(self, name: str, password: str) -> bool:
        raise NotImplementedError()
    
    def user_exists(self, name: str) -> bool:
        raise NotImplementedError()

class SQLiteUserDAL(UserDAL):
    def __init__(self, session):
        self.session = session

    def get_all_users(self) -> List[UserModel]:
        return self.session.query(UserModel).all()
    
    def fetch_user_by_name(self, name) -> UserModel:
        return self.session.query(UserModel).filter_by(name=name).first()

    def post_user(self) -> List[UserModel]:
        args = UserModel.parse_args()
        self._write_user(name=args["name"], password=args["password"])
        return self.get_all_users()
    
    def _write_user(self, name: str, password: str):
        if self.user_exists(name):
            raise ValueError("User already exists. Maybe try a different username.")
        if is_weak_password(password):
            raise ValueError("Password too weak. Must be atleast 8 characters long.")

        password, salt = PasswordManager.hash_password(password)
        new_user = UserModel(name=name, password=password, salt=salt)

        self.session.add(new_user)
        self.session.commit()
    
    def validate_auth(self, name: str, password: str) -> bool:
        user = self.fetch_user_by_name(name)
        if not user:
            raise ValueError(f"User '{name}' doesn't exist'")
        return PasswordManager.verify_hashes(user.password, password)


    def user_exists(self, name: str) -> bool:
        return self.fetch_user_by_name(name)
