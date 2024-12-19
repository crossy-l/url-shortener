from flask import Flask
from flask_restful import Api
from app.utils.args import arguments
from app.database.database import ApiDatabase
from app.factory import create_users_resource, create_user_resource, create_users

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
            users.write_user("admin", "12345678")

        self.api = Api(self.app)
        self.api.add_resource(create_users_resource(self.db), '/users/')
        self.api.add_resource(create_user_resource(self.db), '/user/<string:id>')

    def run(self):
        self.app.run()

if __name__ == "__main__":
    app = ApiApp(__name__, arguments)
    app.run()
