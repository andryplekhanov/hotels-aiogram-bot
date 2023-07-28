from datetime import datetime

from sqlalchemy import Integer, String, DateTime, BigInteger, ForeignKey
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import mapped_column

Base = declarative_base()


class User(Base):
    """
    Класс пользователя.

    Attributes:
        id (int): уникальный id пользователя == id пользователя Telegram
        connection_date (datetime.date): дата внесения пользователя в БД
    """

    __tablename__ = 'user'

    id = mapped_column(BigInteger, autoincrement=False, primary_key=True, unique=True, index=True)
    connection_date = mapped_column(DateTime, default=datetime.now, nullable=False)

    def __repr__(self):
        return f'{self.id}'


class Request(Base):
    """
    Класс запроса. Каждый успешный запрос пользователя к API сохраняется в экземпляре данного класса.

    Attributes:
        id (int): уникальный id запроса
        user_id (User): указание на id пользователя - автора запроса
        command (str): команда запроса, введенная пользователем
        date (datetime.date): дата запроса
        city_name (str): город, введенный пользователем для поиска отелей
    """

    __tablename__ = 'request'

    id = mapped_column(Integer, primary_key=True, autoincrement=True, index=True)
    user_id = mapped_column(BigInteger, ForeignKey('user.id', ondelete='CASCADE'), nullable=False, index=True)
    command = mapped_column(String, nullable=False)
    date = mapped_column(DateTime, default=datetime.now, nullable=False)
    city_name = mapped_column(String, nullable=False)

    def __repr__(self):
        return f'{self.date}: {self.command} - {self.city_name}'


class Result(Base):
    """
    Класс результата. Результат каждого успешного запроса пользователя к API сохраняется в экземпляре данного класса.

    Attributes:
        id (int): уникальный id результата
        request_id (Request): указание на id запроса, к которому относится данный результат
        hotel_id (str): id отеля, найденного в результате запроса
        hotel_name (str): название отеля, найденного в результате запроса
        result_str (str): подробное описание отеля (район, стоимость, удаленность от центра, рейтинг)
    """

    __tablename__ = 'result'

    id = mapped_column(Integer, primary_key=True, autoincrement=True, index=True)
    request_id = mapped_column(Integer, ForeignKey('request.id', ondelete='CASCADE'), nullable=False, index=True)
    hotel_id = mapped_column(String, nullable=False)
    hotel_name = mapped_column(String, nullable=False)
    result_str = mapped_column(String, nullable=False)

    def __repr__(self):
        return f'{self.hotel_name}'
