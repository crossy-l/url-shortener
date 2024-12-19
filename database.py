import uuid
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import Column, Integer, String, create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from flask_restful import fields, reqparse
from args import ApiArguments

Base = declarative_base()

class UserModel(Base):
    __tablename__ = "users"
    __args = reqparse.RequestParser()
    __args.add_argument('name', type=str, required=True, help="Name cannot be blank")
    __args.add_argument('password', type=str, required=True, help="Password cannot be blank")
    __user_fields = {
        'id': fields.String,
        'name': fields.String,
        'password': fields.String,
        'salt': fields.String
    }

    id = Column(String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    name = Column(String(80), unique=True, nullable=False)
    password = Column(String(60), nullable=False)
    salt = Column(String(60), nullable=False)

    @classmethod
    def parse_args(cls) -> reqparse.Namespace:
        return cls.__args.parse_args()
    
    @classmethod
    def fields(cls) -> dict[str, any]:
        return cls.__user_fields

    def __repr__(self): 
        return f"User(name={self.name}, password={self.password})"
    
class ApiDatabase:
    def __init__(self, app: Flask, args: ApiArguments):
        self.app = app
        self.app.config['SQLALCHEMY_DATABASE_URI'] = args.sqlite_db_path
        self.db = SQLAlchemy(self.app)

        with self.app.app_context():
            self.engine = self.db.engine
            self.Session = sessionmaker(bind=self.engine)
            self.session = self.Session()

    def create_tables(self):
        Base.metadata.create_all(self.engine)

    def drop_tables(self):
        Base.metadata.drop_all(self.engine)