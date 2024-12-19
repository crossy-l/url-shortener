from typing import List
from app.models.user import UserModel

def is_weak_password(password: str) -> bool:
    return password.isspace() or len(password) < 8

class UserDAL:
    def get_user(self, id: str) -> UserModel:
        raise NotImplementedError()

    def get_all_users(self) -> List[UserModel]:
        raise NotImplementedError()
    
    def post_user(self) -> List[UserModel]:
        raise NotImplementedError()
    
    def patch_user(self, id: str) -> UserModel:
        raise NotImplementedError()
    
    
    def fetch_user_by_name(self, name) -> UserModel:
        raise NotImplementedError()
    
    def write_user(self):
        raise NotImplementedError()
    
    def validate_auth(self, name: str, password: str) -> bool:
        raise NotImplementedError()
    
    def user_exists(self, name: str) -> bool:
        raise NotImplementedError()
    