import os
import datetime
import requests
import streamlit as st
import json
from dotenv import load_dotenv


load_dotenv()

WEATHER_API_KEY = os.getenv("OPENWEATHER_API_KEY")
WEATHER_API_URL = "https://api.openweathermap.org/data/2.5/weather"
DEFAULT_LOCATION = "Manila, PH"

NEWS_API_KEY = os.getenv("NEWS_API_KEY")
NEWS_API_URL = "https://newsapi.org/v2/top-headlines"
MAX_NEWS_HEADLINES = 5

def fetch_weather_draft(location):
    if not WEATHER_API_KEY:
        return "⚠️ Weather API key not found. Please set OPENWEATHER_API_KEY in your .env file."

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

def fetch_news_draft(limit):

    if not NEWS_API_KEY:
        return "⚠️ News API key not found. Please set NEWS_API_KEY in your .env file."
    
    query_parameters = {
        "language": "en", # language english to get news more
        "apiKey": NEWS_API_KEY,
        "pageSize": limit
    }
    
    try:
        response = requests.get(NEWS_API_URL, params=query_parameters)
        response.raise_for_status()
        
        news_data = response.json()
        articles = news_data.get("articles", [])
        
        if not articles:
            return "📰 No top headlines found right now."
            
        formatted_news = ""
        for article in articles:
            title = article.get("title", "No Title")
            formatted_news += f"📰 **{title}**\n\n"
            
        return formatted_news
        
    except requests.exceptions.RequestException as error:
        return "⚠️ Could not fetch news. Check your connection or API key."

def fetch_schedule_draft():
    schedule = "schedule.json"

    if not os.path.exists(schedule):
        return "📅 No schedule found. Please create a schedule.json file."
    
    try:
        with open(schedule, "r") as file:
            schedule_data = json.load(file)
        if not schedule_data:
            return "📅 Your schedule is empty. Please add some events to schedule.json."
        
        formatted_schedule = ""
        for time in schedule_data.items():
            formatted_schedule += f"📅 **{time[0]}**: {time[1]}\n\n"

        return formatted_schedule
    except json.JSONDecodeError as e:
        return "⚠️ Invalid schedule format. Please ensure schedule.json is a valid JSON file."


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
        st.info(fetch_weather_draft(DEFAULT_LOCATION)) #
        
        st.header("Today's Schedule")
        st.success(fetch_schedule_draft()) 
        
    # right
    with right_column:
        st.header("Top Headlines")
        st.warning(fetch_news_draft(MAX_NEWS_HEADLINES)) 

if __name__ == "__main__":
    render_dashboard()