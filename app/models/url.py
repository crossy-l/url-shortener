import uuid
from sqlalchemy import Column, Integer, String, Boolean, create_engine
from flask_restful import fields, reqparse
from app.database.database import Base

class UrlModel(Base):
    __tablename__ = "urls"
    __args = reqparse.RequestParser()
    __args.add_argument('alias', type=str, required=False, help="If not specified a random alias will be generated")
    __args.add_argument('target', type=str, required=True, help="Target cannot be blank")
    __args.add_argument('enforce-validity', type=bool, required=False, help="If the site needs to be reachable", default=True)
    __optional_args = reqparse.RequestParser()
    __optional_args.add_argument('alias', type=str, required=False, help="The alias to use")
    __optional_args.add_argument('target', type=str, required=False, help="The target to use")
    __optional_args.add_argument('enforce-validity', type=bool, required=False, help="If the site needs to be reachable")
    __url_fields = {
        'id': fields.String,
        'alias': fields.String,
        'target': fields.String,
        'enforce-validity': fields.Boolean(attribute="enforce_validity"),
        'redirects': fields.Integer
    }

    id = Column(String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    alias = Column(String(80), unique=True, nullable=False)
    target = Column(String(80), nullable=False)
    redirects = Column(Integer(), nullable=False, default=0)
    enforce_validity = Column(Boolean(True), nullable=False, default=True)

    @classmethod
    def parse_args(cls) -> reqparse.Namespace:
        return cls.__args.parse_args()
    
    @classmethod
    def parse_optional_args(cls) -> reqparse.Namespace:
        return cls.__optional_args.parse_args()

    @classmethod
    def fields(cls) -> dict[str, any]:
        return cls.__url_fields

    def __repr__(self): 
        return f"Url(alias={self.alias}, target={self.target}, enforce-validity={self.enforce_validity})"