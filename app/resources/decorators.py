from functools import wraps
from flask_restful import abort
from flask import request
from app.utils.passwords import PasswordManager
from app.errors import ApiError, ResourceAlreadyExists, ResourceNotFoundError, PasswordToWeakError, AuthenticationError, OutOfUuidError, TargetNotReachableError

def requires_auth():
    def decorator(func):
        @wraps(func)
        def wrapper(self, *args, **kwargs):
            if not hasattr(self, "user_dal"):
                raise AttributeError("The attribute 'user_dal' is not defined on the resource.")
            user_dal = self.user_dal
            try:
                name, password = PasswordManager.get_auth_credentials(request.headers)
            except Exception as e:
                raise AuthenticationError(str(e)) from e
            if not user_dal.validate_auth(name, password):
                abort(401)
            return func(self, *args, **kwargs)
        return wrapper
    return decorator

def handle_error(default_exceptions: dict[Exception, int]={
    ApiError: 500,
    ResourceAlreadyExists: 400,
    ResourceNotFoundError: 404,
    PasswordToWeakError: 400,
    AuthenticationError: 401,
    TargetNotReachableError: 400,
    OutOfUuidError: 503
    }):
    errors = tuple(default_exceptions.keys())

    def get_http_code(exception):
        error_type = type(exception)
        while error_type is not object:
            if error_type in default_exceptions:
                return default_exceptions[error_type]
            error_type = error_type.__base__
        return 500

    def decorator(func):
        @wraps(func)
        def wrapper(self, *args, **kwargs):
            try:
                return func(self, *args, **kwargs)
            except errors as e: 
                abort(get_http_code(e), message=str(e))
        return wrapper
    return decorator

