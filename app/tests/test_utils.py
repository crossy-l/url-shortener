from app.utils.uuids import generate_truncated_uuid
from app.utils.passwords import PasswordManager

def test_generate_truncated_uuid():
    uuid = generate_truncated_uuid()
    assert len(uuid) == 8
    uuid = generate_truncated_uuid(length=50)
    assert len(uuid) == 32

def test_password_manager():
    password = "Test@1234"
    hashed, salt = PasswordManager.hash_password(password)
    assert PasswordManager.verify_hashes(hashed, password)
