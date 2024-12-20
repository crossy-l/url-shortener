from flask import Flask
from flask_limiter import Limiter
from flask_limiter.util import get_remote_address
from flask_restful import Api
from app.utils.args import ApiArguments, parse_arguments
from app.database.database import ApiDatabase
from app.factory import create_users_resource, create_user_resource, create_users, create_url_resource, create_urls_resource, create_home_resource

class ApiApp:
    def __init__(self, name: str, args: ApiArguments):
        self.app = Flask(name)
        self.app.config["CACHE_TYPE"] = "FileSystemCache"
        self.app.config["CACHE_DIR"] = args.cache_dir
        self.app.config["CACHE_DEFAULT_TIMEOUT"] = args.cache_timeout

        self.limiter = Limiter(
            get_remote_address,
            app=self.app,
            default_limits=args.limits,
            storage_uri="memory://"
        )
        
        self.db = ApiDatabase(self.app, args)
        if args.recreate_db:
            self.db.drop_tables()
            self.db.create_tables()
            users = create_users(self.db)
            users.write_user("admin", "12345678")

        self.api = Api(self.app)
        self.api.add_resource(create_users_resource(self.db), '/users/')
        self.api.add_resource(create_user_resource(self.db), '/user/<string:id>')
        self.api.add_resource(create_urls_resource(self.db), '/urls/')
        self.api.add_resource(create_url_resource(self.db), '/url/<string:id>')
        self.api.add_resource(create_home_resource(self.db), '/<string:alias>')

    def run(self):
        self.app.run()

gunicorn_app = ApiApp(__name__, ApiArguments.from_defaults()).app

if __name__ == "__main__":
    app = ApiApp(__name__, parse_arguments())
    app.run()
