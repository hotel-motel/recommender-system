from .database import Base
from sqlalchemy import Column, Integer, String, Date


class User(Base):
    __tablename__ = "users"
    id = Column(Integer, primary_key=True, index=True)
    email = Column(String, unique=True, index=True)
    password = Column(String)

class Trip(Base):
    __tablename__ = "trips"
    id = Column(Integer, primary_key=True, index=True)
    start = Column(Date)
    end = Column(Date)
    amount = Column(Integer)