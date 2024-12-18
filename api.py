from flask import Flask
from flask_caching import Cache
from flask_limiter import Limiter
from flask_limiter.util import get_remote_address
from flask_restful import Resource, Api, reqparse, fields, marshal_with, abort
from args import ApiArguments, arguments
from database import ApiDatabase

class Users(Resource):
    @marshal_with(userFields)
    def get(self):
        users = UserModel.query.all() 
        return users 

class Api:
    def __init__(self, name: str, args: ApiArguments):
        self.app = Flask(name)
        self.app.config["CACHE_TYPE"] = "FileSystemCache"
        self.app.config["CACHE_DIR"] = args.cache_dir
        self.app.config["CACHE_DEFAULT_TIMEOUT"] = args.cache_timeout
        self.db = ApiDatabase(self.app, args)

        if args.recreate_db:
            self.db.drop_tables()
            self.db.create_tables()

    def run(self):
        self.app.run()

api = Api(__name__, arguments)

if __name__ == "__main__":
    api.run()
    