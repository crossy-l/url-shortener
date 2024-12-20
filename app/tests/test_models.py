from app.models.user import UserModel
from app.models.url import UrlModel

def test_user_model_repr():
    user = UserModel(name="testuser", password="hashed", salt="salt")
    assert repr(user) == "User(name=testuser, password=hashed, salt=salt)"

def test_url_model_repr():
    url = UrlModel(alias="testalias", target="http://example.com", enforce_validity=False)
    assert repr(url) == "Url(alias=testalias, target=http://example.com, enforce-validity=False)"
