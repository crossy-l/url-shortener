from app.dal.sql.user import SQLiteUserDAL
from app.dal.sql.url import SQLiteUrlDAL
from app.errors import UserNotFoundError, UrlNotFoundError

def test_write_user(session):
    user_dal = SQLiteUserDAL(session)
    user = user_dal.write_user(name="testuser", password="Test@1234")
    assert user.name == "testuser"
    assert user_dal.get_user(user.id).name == "testuser"

def test_user_not_found_error(session):
    user_dal = SQLiteUserDAL(session)
    try:
        user_dal.get_user("nonexistent")
    except UserNotFoundError as e:
        assert str(e) == "User with id 'nonexistent' not found"

def test_write_url(session):
    url_dal = SQLiteUrlDAL(session)
    url = url_dal.write_url(alias="testalias", target="http://example.com", enforce_validity=False)
    assert url.alias == "testalias"
    assert url_dal.get_url(url.alias).target == "http://example.com"

def test_url_not_found_error(session):
    url_dal = SQLiteUrlDAL(session)
    try:
        url_dal.get_url("nonexistent")
    except UrlNotFoundError as e:
        assert str(e) == "Url with id 'nonexistent' not found"
