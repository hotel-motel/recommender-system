from datetime import date
from pydantic import BaseModel


class TripBase(BaseModel):
    start: date
    end: date
    amount: int

class Trip(TripBase):
    id: int
    creator_id: int
    class Config:
        orm_mode = True

class UserBase(BaseModel):
    email: str

class User(UserBase):
    id: int
    trips: list[Trip] = []
    class Config:
        orm_mode = True