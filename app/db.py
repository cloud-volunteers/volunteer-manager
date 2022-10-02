from databases import Database
from ormar import ModelMeta, Model
from ormar import Integer, String, Boolean
from sqlalchemy import MetaData, create_engine
from json import dumps

from app.config import Config

database = Database(Config.DATABASE_URL)
metadata = MetaData()


class BaseMeta(ModelMeta):
    metadata = metadata
    database = database


class Volunteer(Model):
    class Meta(BaseMeta):
        tablename = "volunteers"

    id: int = Integer(primary_key=True)
    email: str = String(max_length=128, unique=True, nullable=False)
    active: bool = Boolean(default=True)
    county: str = String(max_length=128, default=None, nullable=True)
    online: bool = Boolean(default=False)
    offline: bool = Boolean(default=False)
    age: int = Integer(default=None, nullable=True)

    def __str__(self):
        return dumps(self, default=lambda o: o.__dict__)

    def toPrintableJSON(self):
        return dumps(self, default=lambda o: o.__dict__, indent=4)

    def __eq__(self, other) : 
        return self.__dict__ == other.__dict__

engine = create_engine(Config.DATABASE_URL)
metadata.create_all(engine)