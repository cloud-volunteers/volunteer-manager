from databases import Database
from ormar import ModelMeta, Model
from ormar import Integer, String, Boolean
from sqlalchemy import MetaData, create_engine
from json import dumps

from common.config import Config

database = Database(Config.DATABASE_URL)
metadata = MetaData()


class BaseMeta(ModelMeta):
    metadata = metadata
    database = database


class User(Model):
    class Meta(BaseMeta):
        tablename = "users"

    id: int = Integer(primary_key=True)
    email: str = String(max_length=128, unique=True, nullable=False)
    active: bool = Boolean(default=True)

    def toPrintableJSON(self):
        return dumps(self, default=lambda o: o.__dict__, indent=4)


engine = create_engine(Config.DATABASE_URL)
metadata.create_all(engine)