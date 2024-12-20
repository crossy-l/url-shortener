class ApiError(Exception):
    """Base class for all custom exceptions."""
    pass

class AuthenticationError(ApiError):
    def __init__(self, message: str = "Authentication invalid"):
            super().__init__(message)

class PasswordToWeakError(ApiError):
    def __init__(self, message: str = "Password too weak. Must be atleast 8 characters long."):
            super().__init__(message)

class ResourceAlreadyExists(ApiError):
    def __init__(self, resource_name: str, resource_id: str):
            message = f"{resource_name} with id '{resource_id}' already exists"
            super().__init__(message)

class ResourceNotFoundError(ApiError):
    def __init__(self, resource_name: str, resource_id: str):
        message = f"{resource_name} with id '{resource_id}' not found"
        super().__init__(message)

class UserNotFoundError(ResourceNotFoundError):
    def __init__(self, user_id: str):
        super().__init__(resource_name="User", resource_id=user_id)

class UserAlreadyExistsError(ResourceAlreadyExists):
    def __init__(self, user_id: str):
        super().__init__(resource_name="User", resource_id=user_id)

class UrlNotFoundError(ResourceNotFoundError):
    def __init__(self, url_id: str):
        super().__init__(resource_name="Url", resource_id=url_id)

class UrlAlreadyExistsError(ResourceAlreadyExists):
    def __init__(self, url_id: str):
        super().__init__(resource_name="Url", resource_id=url_id)

class TargetNotReachableError(ApiError):
    def __init__(self, target: str):
            super().__init__(f"The target site '{target}' cannot be reached")

class OutOfUuidError(ApiError):
    def __init__(self, message: str = "Failed to generate a unique id to use. You may try again"):
            super().__init__(message)