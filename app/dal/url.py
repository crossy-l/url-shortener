import requests
from typing import List
from app.models.url import UrlModel

def is_valid_url(url: str) -> bool:
    try:
        requests.get(url, timeout=3)
    except requests.exceptions.RequestException as e:
        return False
    return True

class UrlDAL:
    def get_url(self, id: str) -> UrlModel:
        raise NotImplementedError()

    def get_all_urls(self) -> List[UrlModel]:
        raise NotImplementedError()
    
    def post_url(self) -> List[UrlModel]:
        raise NotImplementedError()
    
    def patch_url(self, id: str) -> UrlModel:
        raise NotImplementedError()
    
    def delete_url(self, id: str) -> str:
        raise NotImplementedError()
    
    def increase_redirects(self, url: UrlModel):
        raise NotImplementedError()
    
    def fetch_url_by_alias(self, name) -> UrlModel:
        raise NotImplementedError()
    
    def url_exists(self, name: str) -> bool:
        raise NotImplementedError()
    
    def generate_uuid(self) -> str:
        raise NotImplementedError()
    