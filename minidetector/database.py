from sqlalchemy import create_engine
from sqlalchemy import Column, String, Integer
from sqlalchemy.orm import Session
from sqlalchemy.ext.declarative import declarative_base

from os import environ

try:
    db_string = "postgres://{}:{}@{}/{}".format(environ['POSTGRES_USER'],
                                                environ['POSTGRES_PASSWORD'],
                                                environ['POSTGRES_HOST'],
                                                environ['POSTGRES_DB'])

except KeyError:
    raise KeyError("Could not fetch one or more of following environment variables:"
                   " POSTGRES_USER, POSTGRES_PASSWORD, POSTGRES_HOST, POSTGRES_DB")

engine = create_engine(db_string, pool_size=10, max_overflow=20)
Base = declarative_base()


def create_tables():
    Base.metadata.create_all(engine)


def drop_tables():
    Base.metadata.drop_all(engine)


def create_session():
    return Session(bind=engine)


class Entity(Base):
    __tablename__ = 'entity'
    id = Column(Integer, primary_key=True)
    mac = Column(String)
    ip = Column(String)

    def __repr__(self):
        return f'<{self.__class__.__name__} id={self.id} MAC={self.mac} IP={self.ip}>'
