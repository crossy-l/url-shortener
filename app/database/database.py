from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.orm import sessionmaker, declarative_base
from app.utils.args import ApiArguments

Base = declarative_base()
    
class ApiDatabase:
    def __init__(self, app: Flask, args: ApiArguments):
        self.app = app
        if args is not None:
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