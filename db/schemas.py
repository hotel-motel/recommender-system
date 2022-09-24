from datetime import date
from pydantic import BaseModel

class PassengerBase(BaseModel):
    first_name: str
    last_name: str
    national_code:str

class Passenger(PassengerBase):
    id: int
    trip_id: int
    class Config:
        orm_mode = True

class TripBase(BaseModel):
    start: date
    end: date
    amount: int

class Trip(TripBase):
    id: int
    creator_id: int
    room_id: int
    passengers: list[Passenger] = []
    class Config:
        orm_mode = True

class RoomBase(BaseModel):
    number: int
    price: int
    floor: int
    max_capacity: int

class Room(RoomBase):
    id: int
    hotel_id:int
    trips: list[Trip] = []
    class Config:
        orm_mode = True

class UserBase(BaseModel):
    email: str

class User(UserBase):
    id: int
    trips: list[Trip] = []
    class Config:
        orm_mode = True

class HotelBase(BaseModel):
    name: str
    address: str
    image: str
    credit: int

class Hotel(HotelBase):
    id: int
    city_id: int
    rooms: list[Room]=[]
    class Config:
        orm_mode = True

class CityBase(BaseModel):
    name: str
    image: str
    hotels: list[Hotel] = []

class City(CityBase):
    id: int
    class Config:
        orm_mode = True