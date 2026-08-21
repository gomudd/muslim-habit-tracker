from fastapi import FastAPI, Depends, HTTPException
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session
from typing import Dict
import requests
import bcrypt

from database import Base, engine, get_db
from models import User
from schemas import UserCreate, UserOut, PrayerReminder
from auth import verify_password, create_access_token, get_current_user

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


@app.post("/login")
def login(form_data: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)):
    user = db.query(User).filter(User.email == form_data.username).first()
    if not user or not verify_password(form_data.password, user.hashed_password):
        raise HTTPException(status_code=401, detail="Incorrect email or password")

    access_token = create_access_token(data={"sub": user.email})
    return {"access_token": access_token, "token_type": "bearer"}


@app.get("/me", response_model=UserOut)
def read_me(current_user: User = Depends(get_current_user)):
    return current_user


@app.get("/me/reminders")
def get_reminders(current_user: User = Depends(get_current_user)):
    return current_user.reminder_settings


@app.put("/me/reminders")
def update_reminders(
    updates: Dict[str, PrayerReminder],
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    settings = dict(current_user.reminder_settings or {})
    for prayer, pref in updates.items():
        settings[prayer] = pref.dict()
    current_user.reminder_settings = settings
    db.commit()
    db.refresh(current_user)
    return current_user.reminder_settings