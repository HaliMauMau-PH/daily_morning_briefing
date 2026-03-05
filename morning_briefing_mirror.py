import datetime
import os

from dotenv import load_dotenv

#load environment
load_dotenv()


WEATHER_API_KEY = os.getenv("OPENWEATHER_API_KEY")
DEFAULT_LOCATION = "Manila, PH"

def get_weather():
    return

def get_local_headlines():
    return

def get_daily_schedue():
    return

def generate_morning_briefing():

    currren_date = datetime.date.today()
    formatted_date = currren_date.strftime("%A, %B %d, %Y")
    seperator = "=" * 50

    print(seperator)
    print(f"Good morning! Today is {formatted_date}.")
    print(seperator)

if WEATHER_API_KEY:
    print("Weather API key found. Fetching weather data...")
else:
    print("Weather API key not found. Skipping weather data.")

    print(f"\n{separator}")

if __name__ == "__main__":
    generate_morning_briefing()