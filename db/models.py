from .database import Base
from sqlalchemy.orm import relationship
from sqlalchemy import Column, Integer, String, Date, ForeignKey, DateTime

class Hotel(Base):
    __tablename__ = "hotels"
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String)
    address = Column(String)
    image = Column(String)
    credit = Column(Integer)
    star = Column(Integer)
    city_id = Column(Integer, ForeignKey("cities.id"))
    city = relationship("City", back_populates="hotels")
    rooms = relationship("Room", back_populates="hotel")

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
    room_id = Column(Integer, ForeignKey("rooms.id"))
    room = relationship("Room", back_populates="trips")
    passengers = relationship("Passenger", back_populates="trip")

class City(Base):
    __tablename__ = "cities"
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String)
    image = Column(String)
    hotels = relationship("Hotel", back_populates="city")

class Passenger(Base):
    __tablename__ = "passengers"
    id = Column(Integer, primary_key=True, index=True)
    first_name = Column(String)
    last_name = Column(String)
    national_code = Column(String)
    trip_id = Column(Integer, ForeignKey("trips.id"))
    trip = relationship("Trip", back_populates="passengers")

class Room(Base):
    __tablename__ = "rooms"
    id = Column(Integer, primary_key=True, index=True)
    number = Column(Integer)
    price = Column(Integer)
    floor = Column(Integer)
    max_capacity = Column(Integer)
    deleted_at = Column(DateTime)
    hotel_id = Column(Integer, ForeignKey("hotels.id"))
    hotel = relationship("Hotel", back_populates="rooms")
    trips = relationship("Trip", back_populates="room")