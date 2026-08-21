from pydantic import BaseModel, EmailStr

class UserCreate(BaseModel):
    email: EmailStr
    password: str
    city: str = "Doha"
    country: str = "Qatar"

class UserOut(BaseModel):
    id: int
    email: str
    city: str
    country: str

    class Config:
        from_attributes = True

class PrayerReminder(BaseModel):
    enabled: bool
    minutes_before: int
    vibrate: bool = True