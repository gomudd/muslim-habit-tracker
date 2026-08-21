import copy
from sqlalchemy import Column, Integer, String, JSON
from database import Base

DEFAULT_REMINDERS = {
    "Fajr": {"enabled": True, "minutes_before": 15, "vibrate": True},
    "Duha": {"enabled": False, "minutes_before": 15, "vibrate": True},
    "Zohr": {"enabled": True, "minutes_before": 15, "vibrate": True},
    "Asr": {"enabled": True, "minutes_before": 15, "vibrate": True},
    "Maghrib": {"enabled": True, "minutes_before": 15, "vibrate": True},
    "Isha": {"enabled": True, "minutes_before": 15, "vibrate": True},
    "Tahajud": {"enabled": False, "minutes_before": 0, "vibrate": True},
}

class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    email = Column(String, unique=True, index=True, nullable=False)
    hashed_password = Column(String, nullable=False)
    city = Column(String, default="Doha")
    country = Column(String, default="Qatar")
    reminder_settings = Column(JSON, default=lambda: copy.deepcopy(DEFAULT_REMINDERS))