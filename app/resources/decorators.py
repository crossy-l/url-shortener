from functools import wraps
from flask_restful import abort
from flask import request
from app.utils.passwords import PasswordManager

def requires_auth():
    def decorator(func):
        @wraps(func)
        def wrapper(self, *args, **kwargs):
            if not hasattr(self, "user_dal"):
                raise AttributeError("The attribute 'user_dal' is not defined on the resource.")
            try:
                user_dal = self.user_dal
                name, password = PasswordManager.get_auth_credentials(request.headers)
                if not user_dal.validate_auth(name, password):
                    abort(401, message="Invalid password")
            except Exception as e:
                abort(401, message=f"Failed auth: {e}")
            return func(self, *args, **kwargs)
        return wrapper
    return decorator


