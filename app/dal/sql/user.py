from typing import List
from app.dal.user import UserDAL, is_weak_password
from app.models.user import UserModel
from app.utils.passwords import PasswordManager
from app.errors import UserAlreadyExistsError, UserNotFoundError, PasswordToWeakError
from sqlalchemy.orm import Session

class SQLiteUserDAL(UserDAL):
    def __init__(self, session: Session):
        self.session = session

    def get_user(self, id: str) -> UserModel:
        user = self.session.query(UserModel).filter_by(id=id).first()
        if not user:
            user = self.fetch_user_by_name(name=id)
        if not user:
            raise UserNotFoundError(id)
        return user

    def get_all_users(self) -> List[UserModel]:
        return self.session.query(UserModel).all()
    
    def post_user(self) -> UserModel:
        args = UserModel.parse_args()
        user = self.write_user(name=args["name"], password=args["password"])
        return user
    
    def patch_user(self, id: str) -> UserModel:
        args = UserModel.parse_optional_args()
        user = self.get_user(id)
        self.update_user(user=user, name=args["name"], password=args["password"])
        return user

    def fetch_user_by_name(self, name) -> UserModel:
        return self.session.query(UserModel).filter_by(name=name).first()
    
    def delete_user(self, id: str) -> str:
        user = self.get_user(id)
        self.session.delete(user)
        self.session.commit()
        return f"Deleted user '{id}'"
        
    
    def write_user(self, name: str, password: str) -> UserModel:
        if self.user_exists(name):
            raise UserAlreadyExistsError(name)
        if is_weak_password(password):
            raise PasswordToWeakError()

        password, _ = PasswordManager.hash_password(password)
        new_user = UserModel(name=name, password=password)

        self.session.add(new_user)
        self.session.commit()
        return new_user

    def update_user(self, user: UserModel, name: str, password: str):
        if password is not None:
            if is_weak_password(password):
                raise PasswordToWeakError()

            password, salt = PasswordManager.hash_password(password)
            user.password = password
            user.salt = salt
        
        if name is not None:
            other_user = self.fetch_user_by_name(name)
            if other_user is not None and other_user.id != user.id:
                raise UserAlreadyExistsError(name)
            
            user.name = name

        self.session.commit()
    
    def validate_auth(self, name: str, password: str) -> bool:
        user = self.fetch_user_by_name(name)
        if not user:
            raise UserNotFoundError(name)
        return PasswordManager.verify_hashes(user.password, password)


    def user_exists(self, name: str) -> bool:
        return self.fetch_user_by_name(name)
