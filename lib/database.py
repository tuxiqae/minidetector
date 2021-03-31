import typing
import datetime
from os import environ

from sqlalchemy import create_engine, Column, String, Integer, select, UniqueConstraint, func, DateTime, desc
from sqlalchemy.orm import Session
from sqlalchemy.ext.declarative import declarative_base

try:
    db_string: str = "postgres://{}:{}@{}:{}/{}".format(environ['POSTGRES_USER'],
                                                        environ['POSTGRES_PASSWORD'],
                                                        environ['POSTGRES_HOST'],
                                                        environ['POSTGRES_PORT'],
                                                        environ['POSTGRES_DB'])

except KeyError:
    raise KeyError("Could not fetch one or more of following environment variables:"
                   " POSTGRES_USER, POSTGRES_PASSWORD, POSTGRES_HOST, POSTGRES_PORT, POSTGRES_DB")

engine = create_engine(db_string, pool_size=10, max_overflow=20)
Base = declarative_base()


def create_tables() -> None:
    Base.metadata.create_all(engine)


def drop_tables() -> None:
    Base.metadata.drop_all(engine)


def create_session() -> Session:
    return Session(bind=engine)


def load_db_entries() -> typing.Set[typing.Tuple[str, str]]:
    query = select([Entity.ip, Entity.mac])
    return set((i, m) for i, m in engine.connect().execute(query).fetchall())


def fetch_entities(db: Session):
    return db.query(Entity.mac, Entity.ip)


def fetch_routers(db: Session):
    return db.query(Entity.mac).group_by(Entity.mac).having(func.count(Entity.mac) > 3)


def fetch_lastseen(db: Session):
    return db.query(Entity.mac, Entity.ip).order_by(desc(Entity.timestamp))


class Entity(Base):
    __tablename__ = 'entity'
    id = Column(Integer, primary_key=True)
    timestamp = Column(DateTime, default=datetime.datetime.utcnow)
    mac = Column(String)
    ip = Column(String)

    __table_args__ = (UniqueConstraint('mac', 'ip', name='_mac_ip_uc'),)

    def __repr__(self) -> str:
        return f'<{self.__class__.__name__} id={self.id} MAC={self.mac} IP={self.ip}>'
