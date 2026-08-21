from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy.orm import Session
import requests
import bcrypt

from database import Base, engine, get_db
from models import User
from schemas import UserCreate, UserOut

app = FastAPI()

Base.metadata.create_all(bind=engine)


@app.get("/")
def read_root():
    return {"message": "Assalamualaikum! Muslim Habit Tracker backend is alive."}


@app.get("/prayer-times")
def get_prayer_times(city: str = "Doha", country: str = "Qatar"):
    response = requests.get(
        "https://api.aladhan.com/v1/timingsByCity",
        params={"city": city, "country": country, "method": 2}
    )
    data = response.json()
    return data["data"]["timings"]


@app.post("/signup", response_model=UserOut)
def signup(user: UserCreate, db: Session = Depends(get_db)):
    existing = db.query(User).filter(User.email == user.email).first()
    if existing:
        raise HTTPException(status_code=400, detail="Email already registered")

    hashed = bcrypt.hashpw(user.password.encode(), bcrypt.gensalt()).decode()
    new_user = User(email=user.email, hashed_password=hashed, city=user.city, country=user.country)
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return new_user