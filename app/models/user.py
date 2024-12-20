import uuid
from sqlalchemy import Column, String
from flask_restful import fields, reqparse
from app.database.database import Base

class UserModel(Base):
    __tablename__ = "users"
    __args = reqparse.RequestParser()
    __args.add_argument('name', type=str, required=True, help="Name cannot be blank")
    __args.add_argument('password', type=str, required=True, help="Password cannot be blank")
    __optional_args = reqparse.RequestParser()
    __optional_args.add_argument('name', type=str, required=False, help="Optional name to use")
    __optional_args.add_argument('password', type=str, required=False, help="Optional password to use")
    __user_fields = {
        'id': fields.String,
        'name': fields.String,
        # 'password': fields.String, Should not be served
        # 'salt': fields.String
    }

    id = Column(String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    name = Column(String(80), unique=True, nullable=False)
    password = Column(String(60), nullable=False)

    @classmethod
    def parse_args(cls) -> reqparse.Namespace:
        return cls.__args.parse_args()
    
    @classmethod
    def parse_optional_args(cls) -> reqparse.Namespace:
        return cls.__optional_args.parse_args()

    @classmethod
    def fields(cls) -> dict[str, any]:
        return cls.__user_fields

    def __repr__(self): 
        return f"User(name={self.name}, password={self.password}, salt={self.salt})"