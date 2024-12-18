from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import Column, Integer, String, create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from flask_restful import Resource, Api, reqparse, fields, marshal_with, abort
from args import ApiArguments, arguments

Base = declarative_base()

class UserModel(Base):
    __tablename__ = "users"
    id = Column(Integer, primary_key=True)
    name = Column(String(80), unique=True, nullable=False)
    password = Column(String(80), nullable=False)

    def __repr__(self): 
        return f"User(name = {self.name}, password = {self.password})"
    
USER_FIELDS = {
    'id':fields.Integer,
    'name':fields.String,
    'password':fields.String,
}

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

