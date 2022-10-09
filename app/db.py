from databases import Database
from ormar import ForeignKey, ModelMeta, Model
from ormar import Integer, String, Boolean, Date
from sqlalchemy import MetaData, create_engine
from json import dumps, loads
from datetime import datetime, date, time
from typing import Optional

from app.config import Config

from pymysql import install_as_MySQLdb
install_as_MySQLdb()

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
    phone: str = String(max_length=64, default=None, nullable=True)
    county: str = String(max_length=64, default=None, nullable=True)
    city_sector: str = String(max_length=64, default=None, nullable=True)
    online: bool = Boolean(default=False)
    offline: bool = Boolean(default=False)
    has_car: bool = Boolean(default=False)
    age: int = Integer(default=None, nullable=True)
    status: str = String(max_length=16, default=None, nullable=True)
    active: bool = Boolean(default=True)

    def __str__(self):
        return dumps(self, default=lambda o: o.__dict__)

    def toPrintableJSON(self):
        return dumps(self, default=lambda o: o.__dict__, indent=4)

    def __eq__(self, other) : 
        return self.__dict__ == other.__dict__

    def  __setitem__(self, key, value):
        return setattr(self, key, value)

    def to_dict(self):
        if isinstance(self, Lesson):
            dict = {
            "id": self.id,
            "email": self.email,
            "phone": self.phone,
            "county": self.county,
            "city_sector": self.city_sector,
            "online": self.online,
            "offline": self.offline,
            "has_car": self.has_car,
            "age": self.age,
            "status": self.status,
            "active": self.active
            }
            return dict
        else:
            type_name = self.__class__.__name__
            raise TypeError("Unexpected type {0}".format(type_name))

class Student(Model):
    class Meta(BaseMeta):
        tablename = "students"

    id: int = Integer(primary_key=True)
    email: str = String(max_length=128, unique=True, nullable=False)
    phone: str = String(max_length=64, default=None, nullable=True)
    age: int = Integer(default=None, nullable=True)
    grade: int = Integer(default=None, nullable=True)
    county: str = String(max_length=128, default=None, nullable=True)
    city_sector: str = String(max_length=64, default=None, nullable=True)
    online: bool = Boolean(default=False)
    offline: bool = Boolean(default=False)
    community: str = String(max_length=128, unique=True, nullable=True)
    active: bool = Boolean(default=True)

    def __str__(self):
        return dumps(self, default=lambda o: o.__dict__)

    def toPrintableJSON(self):
        return dumps(self, default=lambda o: o.__dict__, indent=4)

    def __eq__(self, other) : 
        return self.__dict__ == other.__dict__

    def to_dict(self):
        if isinstance(self, Lesson):
            dict = {
            "id": self.id,
            "email": self.email,
            "phone": self.phone,
            "age": self.age,
            "grade": self.grade,
            "county": self.county,
            "city_sector": self.city_sector,
            "online": self.online,
            "offline": self.offline,
            "community": self.community,
            "active": self.active
            }
            return dict
        else:
            type_name = self.__class__.__name__
            raise TypeError("Unexpected type {0}".format(type_name))

class Lesson(Model):
    class Meta(BaseMeta):
        tablename = "lessons"

    id: int = Integer(primary_key=True)
    volunteer: Optional[Volunteer] = ForeignKey(Volunteer, nullable=False, skip_reverse=True)
    student: Optional[Student] = ForeignKey(Student, nullable=True, skip_reverse=True)
    subject: str = String(max_length=64, default=None, nullable=True)
    week_day: str = String(max_length=64, default=None, nullable=True)
    time: str = String(max_length=64, default=None, nullable=True)
    remote: bool = Boolean(default=True)
    active: bool = Boolean(default=True)

    def __str__(self):
        return dumps(self, default=lambda o: o.__dict__)

    def toPrintableJSON(self):
        return dumps(self, default=lambda o: o.__dict__, indent=4)

    def __eq__(self, other) : 
        return self.__dict__ == other.__dict__

    def to_dict(self):
        if isinstance(self, Lesson):
            try:
                student_id = self.student.id
            except AttributeError:
                student_id = None
            return {
            "id": self.id,
            "volunteer_id": self.volunteer.id,
            "student_id": student_id,
            "subject": self.subject,
            "week_day": self.week_day,
            "time": self.time,
            "remote": self.remote,
            "active": self.active
            }
        else:
            type_name = self.__class__.__name__
            raise TypeError("Unexpected type {0}".format(type_name))

engine = create_engine(Config.DATABASE_URL)
metadata.create_all(engine)