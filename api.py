from flask import Flask
from flask_restful import Api
from args import arguments
from database import ApiDatabase
from factory import create_users_resource, create_users

class ApiApp:
    def __init__(self, name: str, args):
        self.app = Flask(name)
        self.app.config["CACHE_TYPE"] = "FileSystemCache"
        self.app.config["CACHE_DIR"] = args.cache_dir
        self.app.config["CACHE_DEFAULT_TIMEOUT"] = args.cache_timeout
        
        self.db = ApiDatabase(self.app, args)
        if args.recreate_db:
            self.db.drop_tables()
            self.db.create_tables()
            users = create_users(self.db)
            users._write_user("admin", "12345678")

        self.api = Api(self.app)
        self.api.add_resource(create_users_resource(self.db), '/users')

    def run(self):
        self.app.run()

if __name__ == "__main__":
    app = ApiApp(__name__, arguments)
    app.run()
