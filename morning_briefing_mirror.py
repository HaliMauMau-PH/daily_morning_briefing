import os
import datetime
import requests
import streamlit as st
from dotenv import load_dotenv


load_dotenv()

WEATHER_API_KEY = os.getenv("OPENWEATHER_API_KEY")
WEATHER_API_URL = "https://api.openweathermap.org/data/2.5/weather"
DEFAULT_LOCATION = "Manila, PH"


def fetch_weather_draft():
    if not WEATHER_API_KEY:
        return "⚠️ Weather API key not found. Please set OPENWEATHER_API_KEY in your .env file."
    return f"🌤️ {DEFAULT_LOCATION}: 28°C, Partly Cloudy (Draft)"

    query_params = {
        "q": location,
        "appid": WEATHER_API_KEY,
        "units": "metric"
    }    

    try:
        response = requests.get(WEATHER_API_URL, params=query_params)
        response.raise_for_status()

        weather_data = response.json()
        temp = weather_data["main"]["temp"]
        description = weather_data["weather"][0]["description"].capitalize()
        
        return f"🌤️ {location}: {temp}°C, {description} "
    except requests.RequestException as e:
        return f"⚠️ Failed to fetch weather data: {e}"

def fetch_news_draft():
    return "📰 Top Story: Something Something bout bread."

def fetch_schedule_draft():
    return "📅 10:00 AM - Go to school\n\n📅 2:00 PM - Take over the world"


def render_dashboard():
    #page config
    st.set_page_config(page_title="Morning Briefing", page_icon="🌅", layout="wide")

    #header
    current_date = datetime.date.today().strftime("%A, %B %d, %Y")
    st.title("🌅 Good Morning!")
    st.subheader(f"Today is {current_date}")
    
    st.divider()
    
    # split into 2
    left_column, right_column = st.columns(2)
    
    # left
    with left_column:
        st.header("Current Weather")
        st.info(fetch_weather_draft()) #
        
        st.header("Today's Schedule")
        st.success(fetch_schedule_draft()) 
        
    # right
    with right_column:
        st.header("Top Headlines")
        st.warning(fetch_news_draft()) 

if __name__ == "__main__":
    render_dashboard()