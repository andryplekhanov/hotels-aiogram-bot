from datetime import datetime

from sqlalchemy import Integer, String, DateTime, BigInteger, ForeignKey
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import mapped_column

Base = declarative_base()


class User(Base):
    __tablename__ = 'user'

    id = mapped_column(BigInteger, autoincrement=False, primary_key=True, unique=True, index=True)
    connection_date = mapped_column(DateTime, default=datetime.now, nullable=False)

    def __repr__(self):
        return f'{self.id}'


class Request(Base):
    __tablename__ = 'request'

    id = mapped_column(Integer, primary_key=True, autoincrement=True, index=True)
    user_id = mapped_column(BigInteger, ForeignKey('user.id', ondelete='CASCADE'), nullable=False, index=True)
    command = mapped_column(String, nullable=False)
    date = mapped_column(DateTime, default=datetime.now, nullable=False)
    city_name = mapped_column(String, nullable=False)

    def __repr__(self):
        return f'{self.date}: {self.command} - {self.city_name}'


class Result(Base):
    __tablename__ = 'result'

    id = mapped_column(Integer, primary_key=True, autoincrement=True, index=True)
    request_id = mapped_column(Integer, ForeignKey('request.id', ondelete='CASCADE'), nullable=False, index=True)
    hotel_id = mapped_column(String, nullable=False)
    hotel_name = mapped_column(String, nullable=False)
    result_str = mapped_column(String, nullable=False)

    def __repr__(self):
        return f'{self.hotel_name}'
