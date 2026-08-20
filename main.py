from fastapi import FastAPI
import requests

app = FastAPI()

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