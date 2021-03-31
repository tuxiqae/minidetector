import datetime

from sqlalchemy import Column, Integer, DateTime, String, UniqueConstraint
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()


class Entity(Base):
    __tablename__ = 'entity'
    id = Column(Integer, primary_key=True)
    timestamp = Column(DateTime, default=datetime.datetime.utcnow)
    mac = Column(String)
    ip = Column(String)

    __table_args__ = (UniqueConstraint('mac', 'ip', name='_mac_ip_uc'),)

    def __repr__(self) -> str:
        return f'<{self.__class__.__name__} id={self.id} MAC={self.mac} IP={self.ip}>'
