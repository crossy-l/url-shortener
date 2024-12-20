from typing import List
from app.dal.url import UrlDAL, is_valid_url
from app.models.url import UrlModel
from app.utils.passwords import PasswordManager
from app.errors import UrlAlreadyExistsError, UrlNotFoundError, TargetNotReachableError, OutOfUuidError
from app.utils.uuids import generate_truncated_uuid
from sqlalchemy.orm import Session

class SQLiteUrlDAL(UrlDAL):
    def __init__(self, session: Session):
        self.session = session

    def get_url(self, id: str) -> UrlModel:
        url = self.session.query(UrlModel).filter_by(id=id).first()
        if not url:
            url = self.fetch_url_by_alias(id)
        if not url:
            raise UrlNotFoundError(id)
        return url

    def get_all_urls(self) -> List[UrlModel]:
        return self.session.query(UrlModel).all()
    
    def post_url(self) -> List[UrlModel]:
        args = UrlModel.parse_args()
        url = self.write_url(alias=args["alias"], target=args["target"], enforce_validity=args["enforce-validity"])
        return url
    
    def patch_url(self, id: str) -> UrlModel:
        args = UrlModel.parse_optional_args()
        url = self.get_url(id)
        self.update_url(url=url, alias=args["alias"], target=args["target"], enforce_validity=args["enforce-validity"])
        return url
    
    def delete_url(self, id: str) -> str:
        url = self.get_url(id)
        self.session.delete(url)
        self.session.commit()
        return f"Delete url '{id}'"
    
    
    def fetch_url_by_alias(self, alias) -> UrlModel:
        return self.session.query(UrlModel).filter_by(alias=alias).first()
    
    def increase_redirects(self, url: UrlModel):
        url.redirects += 1
        self.session.commit()

    def write_url(self, alias: str, target: str, enforce_validity: bool) -> UrlModel:      
        if alias is None or alias == "" :
            alias = self.generate_uuid()
        
        if self.url_exists(alias):
            raise UrlAlreadyExistsError(alias)
        if enforce_validity and not is_valid_url(target):
            raise TargetNotReachableError(target)
        
        new_url = UrlModel(alias=alias, target=target, enforce_validity=enforce_validity)

        self.session.add(new_url)
        self.session.commit()

        return new_url
    
    def update_url(self, url: UrlModel, alias: str, target: str, enforce_validity: bool):
        if alias == "":
            alias = self.generate_uuid()

        if alias is not None:
            other_url = self.fetch_url_by_alias(alias)
            if other_url is not None and other_url.id != url.id:
                raise UrlAlreadyExistsError(alias)
            
            url.alias = alias
        
        if enforce_validity is not None:
            url.enforce_validity = enforce_validity

        if target is not None:
            if url.enforce_validity:
                if not is_valid_url(target):
                    raise TargetNotReachableError(target)
            url.target = target
            url.redirects = 0
        
        self.session.commit()      

    def url_exists(self, alias: str) -> bool:
        return self.fetch_url_by_alias(alias)
    
    def generate_uuid(self) -> str:
        for i in range(0, 100):
            id = generate_truncated_uuid()
            if self.url_exists(id):
                continue
            return id
        raise OutOfUuidError()
