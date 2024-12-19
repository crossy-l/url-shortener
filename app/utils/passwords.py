import bcrypt
from base64 import b64decode

class PasswordManager:
    @staticmethod
    def get_auth_credentials(headers: dict[str, str]) -> tuple[str, str]:
        auth_header = headers.get("Authorization")

        if not auth_header:
            raise ValueError("Missing Authorization header")
        
        if not auth_header.startswith("Basic "):
            raise NotImplementedError("Only basic authentication available")
        
        try:
            auth_decoded = b64decode(auth_header[len("Basic "):]).decode("utf-8")
            username, password = auth_decoded.split(":", 1)
            return username, password
        except Exception as e:
            raise ValueError("Malformed Authorization header", e)

    @staticmethod
    def generate_salt() -> str:
        salt = bcrypt.gensalt()
        return salt.decode('utf-8')

    @staticmethod
    def hash_with_salt(password: str, salt: str) -> str:
        if not password or not salt:
            raise ValueError("Password and salt cannot be empty.")
        
        hashed = bcrypt.hashpw(password.encode('utf-8'), salt.encode('utf-8'))
        return hashed.decode('utf-8')
    
    @staticmethod
    def hash_password(password: str) -> tuple[str, str]:
        salt = PasswordManager.generate_salt()
        hashed = PasswordManager.hash_with_salt(password=password, salt=salt)
        return (hashed, salt)

    @staticmethod
    def verify_hashes(hashed_password: str, password: str) -> bool:
        if not password or not hashed_password:
            raise ValueError("Password and hashed password cannot be empty.")
        
        return bcrypt.checkpw(password.encode('utf-8'), hashed_password.encode('utf-8'))

