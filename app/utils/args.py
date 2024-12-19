import argparse
import os
import sys

class ApiArguments:
    def __init__(self, cache_dir: str, cache_timeout: int, recreate_db: bool, sqlite_path: str):
        self.recreate_db = recreate_db
        self.cache_dir = cache_dir
        self.cache_timeout = cache_timeout
        self.sqlite_db_path = sqlite_path

    @classmethod
    def from_cli_args(cls, args: argparse.Namespace):
        cache_dir = args.cache_dir if os.path.isabs(args.cache_dir) else os.path.join("instance", args.cache_dir)
        recreate_db = args.recreate_db if os.path.exists(os.path.join("instance", args.sql_db_path)) else True

        try:
            if not os.path.exists(cache_dir):
                os.makedirs(cache_dir, exist_ok=True)
            if not os.access(cache_dir, os.R_OK | os.W_OK):
                raise PermissionError(f"The directory '{cache_dir}' is not readable and writable.")
        except Exception as e:
            print(f"Error: Unable to use the cache directory '{cache_dir}'. {e}", file=sys.stderr)
            sys.exit(1)

        if args.cache_timeout < 1:
            print(f"Cache timeout '{args.cache_timeout}' cannot be less than 1 second.")
            sys.exit(1)

        return cls(cache_dir=cache_dir,
                   cache_timeout=args.cache_timeout,
                   recreate_db=recreate_db,
                   sqlite_path=f"sqlite:///{args.sql_db_path}"
                )

_parser = argparse.ArgumentParser("api.py")
_parser.add_argument(
    "--recreate-db",
    action="store_true",
    help="If set, the database will be recreated."
)
_parser.add_argument(
    "--cache-dir",
    type=str,
    default="cache",
    help="Path to the cache directory for Flask. Defaults to 'cache'. Will be created if it does not exist."
)
_parser.add_argument(
    "--sql-db-path",
    type=str,
    default="database.db",
    help="Path to the sqlite database. Defaults to 'database.db'"
)
_parser.add_argument(
    "--cache-timeout",
    type=int,
    default=24 * 60 * 60,
    help="The time it takes for cache elements to get removed. Default is 24 hours."
)

arguments = ApiArguments.from_cli_args(_parser.parse_args())