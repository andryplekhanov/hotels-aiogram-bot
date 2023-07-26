from datetime import datetime

from sqlalchemy import Column, Integer, String, DateTime, BigInteger, ForeignKey
from sqlalchemy.ext.declarative import declarative_base


Base = declarative_base()


class User(Base):
    __tablename__ = 'Users'

    id = Column(Integer, autoincrement=True, primary_key=True, index=True)
    connection_date = Column(DateTime, default=datetime.now, nullable=False)
    tg_id = Column(BigInteger, nullable=False, unique=True)

    def __repr__(self):
        return f'{self.tg_id}'


class Request(Base):
    __tablename__ = 'Request'

    id = Column(Integer, primary_key=True, autoincrement=True, index=True)
    user_id = Column(BigInteger, ForeignKey('user.id', ondelete='CASCADE'), nullable=False, index=True)
    command = Column(String, nullable=False)
    date = Column(DateTime, default=datetime.now, nullable=False)
    city_name = Column(String, nullable=False)

    def __repr__(self):
        return f'{self.date}: {self.command} - {self.city_name}'


class Result(Base):
    __tablename__ = 'Result'

    id = Column(Integer, primary_key=True, autoincrement=True, index=True)
    request_id = Column(Integer, ForeignKey('request.id', ondelete='CASCADE'), nullable=False, index=True)
    hotel_id = Column(String, nullable=False)
    hotel_name = Column(String, nullable=False)
    price_per_night = Column(String, nullable=False)
    total_price = Column(String, nullable=False)
    distance_city_center = Column(String, nullable=False)
    hotel_neighbourhood = Column(String, nullable=False)
    amount_nights = Column(Integer, nullable=False)
    amount_adults = Column(Integer, nullable=True)
    score = Column(String, nullable=False)

    def __repr__(self):
        return f'{self.hotel_name}'
