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
    amount_nights = Column(Integer, nullable=False)
    amount_adults = Column(Integer, nullable=True)
    start_date = Column(DateTime, nullable=False)
    end_date = Column(DateTime, nullable=False)
    start_price = Column(Integer, nullable=True)
    end_price = Column(Integer, nullable=True)
    end_distance = Column(Integer, nullable=True)
