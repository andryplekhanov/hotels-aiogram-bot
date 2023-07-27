from datetime import datetime

from sqlalchemy import Column, Integer, String, DateTime, BigInteger, ForeignKey
from sqlalchemy.ext.declarative import declarative_base


Base = declarative_base()


class User(Base):
    __tablename__ = 'user'

    id = Column(BigInteger, autoincrement=False, primary_key=True, unique=True, index=True)
    connection_date = Column(DateTime, default=datetime.now, nullable=False)

    def __repr__(self):
        return f'{self.id}'


class Request(Base):
    __tablename__ = 'request'

    id = Column(Integer, primary_key=True, autoincrement=True, index=True)
    user_id = Column(BigInteger, ForeignKey('user.id', ondelete='CASCADE'), nullable=False, index=True)
    command = Column(String, nullable=False)
    date = Column(DateTime, default=datetime.now, nullable=False)
    city_name = Column(String, nullable=False)

    def __repr__(self):
        return f'{self.date}: {self.command} - {self.city_name}'


class Result(Base):
    __tablename__ = 'result'

    id = Column(Integer, primary_key=True, autoincrement=True, index=True)
    request_id = Column(Integer, ForeignKey('request.id', ondelete='CASCADE'), nullable=False, index=True)
    hotel_id = Column(String, nullable=False)
    hotel_name = Column(String, nullable=False)
    result_str = Column(String, nullable=False)

    def __repr__(self):
        return f'{self.hotel_name}'
