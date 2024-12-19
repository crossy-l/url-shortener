from typing import List
from app.dal.user import UserDAL, is_weak_password
from app.models.user import UserModel
from app.utils.passwords import PasswordManager

class SQLiteUserDAL(UserDAL):
    def __init__(self, session):
        self.session = session

    def get_user(self, id: str) -> UserModel:
        user = self.session.query(UserModel).filter_by(id=id).first()
        if not user:
            user = self.fetch_user_by_name(name=id)
        if not user:
            raise ValueError(f"No user found with '{id}'")            
        return user

    def get_all_users(self) -> List[UserModel]:
        return self.session.query(UserModel).all()
    
    def post_user(self) -> List[UserModel]:
        args = UserModel.parse_args()
        self.write_user(name=args["name"], password=args["password"])
        return self.get_all_users()
    
    def patch_user(self, id: str) -> UserModel:
        args = UserModel.parse_args()

        user = self.get_user(id)
        self.update_user(user=user, name=args["name"], password=args["password"])
        return user

    def fetch_user_by_name(self, name) -> UserModel:
        return self.session.query(UserModel).filter_by(name=name).first()
    
    def write_user(self, name: str, password: str):
        if self.user_exists(name):
            raise ValueError("User already exists. Maybe try a different username.")
        if is_weak_password(password):
            raise ValueError("Password too weak. Must be atleast 8 characters long.")

        password, salt = PasswordManager.hash_password(password)
        new_user = UserModel(name=name, password=password, salt=salt)

        self.session.add(new_user)
        self.session.commit()

    def update_user(self, user: UserModel, name: str, password: str):
        if password != "":
            if is_weak_password(password):
                raise ValueError("Password too weak. Must be atleast 8 characters long.")

            password, salt = PasswordManager.hash_password(password)
            user.password = password
            user.salt = salt
        
        if name != "":
            other_user = self.fetch_user_by_name(name)
            if other_user is not None and other_user.id != user.id:
                raise ValueError(f"User with the new name '{name}' already exists")
            
            user.name = name

        self.session.commit()
    
    def validate_auth(self, name: str, password: str) -> bool:
        user = self.fetch_user_by_name(name)
        if not user:
            raise ValueError(f"User '{name}' doesn't exist'")
        return PasswordManager.verify_hashes(user.password, password)


    def user_exists(self, name: str) -> bool:
        return self.fetch_user_by_name(name)
