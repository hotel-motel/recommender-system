from .database import Base
from sqlalchemy.orm import relationship
from sqlalchemy import Column, Integer, String, Date, ForeignKey

class User(Base):
    __tablename__ = "users"
    id = Column(Integer, primary_key=True, index=True)
    email = Column(String, unique=True, index=True)
    password = Column(String)
    trips = relationship("Trip", back_populates="creator")

class Trip(Base):
    __tablename__ = "trips"
    id = Column(Integer, primary_key=True, index=True)
    start = Column(Date)
    end = Column(Date)
    amount = Column(Integer)
    creator_id = Column(Integer, ForeignKey("users.id"))
    creator = relationship("User", back_populates="trips")