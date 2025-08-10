import streamlit as st
import requests
import pandas as pd
import datetime
import random
import plotly.express as px
import os
from dotenv import load_dotenv

# --- Configuration ---
load_dotenv()  # Load environment variables from .env file

# Constants
BASE_URL = "https://api.openweathermap.org/data/2.5/weather"
FORECAST_URL = "https://api.openweathermap.org/data/2.5/forecast"
UNITS = "metric"
CACHE_TTL = 600  # 10 minutes in seconds
DEFAULT_CITIES = ["London", "New York", "Tokyo", "Paris", "Sydney"]

# Weather condition emojis
WEATHER_EMOJIS = {
    "clear": "☀️",
    "clouds": "☁️",
    "rain": "🌧️",
    "thunderstorm": "⛈️",
    "snow": "❄️",
    "mist": "🌫️",
    "drizzle": "🌦️",
    "fog": "🌁",
    "haze": "😶‍🌫️"
}

# --- Streamlit Setup ---
st.set_page_config(
    page_title="Weather Dashboard Pro",
    page_icon="🌦️",
    layout="centered",
    initial_sidebar_state="expanded"
)

# --- Helper Functions ---
def get_api_key():
    api_key = os.getenv("OPENWEATHER_API_KEY")
    if not api_key:
        st.error("API key not configured. Please set OPENWEATHER_API_KEY in your .env file")
        st.stop()
    return api_key

@st.cache_data(ttl=CACHE_TTL)
def fetch_weather_data(city_name):
    api_key = get_api_key()
    params = {'q': city_name, 'appid': api_key, 'units': UNITS}
    try:
        response = requests.get(BASE_URL, params=params, timeout=10)
        if response.status_code == 404:
            st.warning("City not found. Please check the name.")
            return None
        response.raise_for_status()
        return response.json()
    except Exception as e:
        st.error(f"⚠️ An unexpected error occurred: {str(e)}")
        st.stop()

@st.cache_data(ttl=CACHE_TTL)
def fetch_forecast_data(city_name):
    api_key = get_api_key()
    params = {'q': city_name, 'appid': api_key, 'units': UNITS, 'cnt': 40}
    try:
        response = requests.get(FORECAST_URL, params=params, timeout=10)
        response.raise_for_status()
        return response.json()
    except Exception as e:
        st.warning(f"Couldn't fetch forecast data: {str(e)}")
        return None

def format_time(timestamp):
    return datetime.datetime.fromtimestamp(timestamp).strftime('%H:%M')

def display_weather_card(data):
    if not data:
        return
    weather = data["weather"][0]
    main = data["main"]
    wind = data["wind"]
    sys = data.get("sys", {})
    condition = weather["main"].lower()
    emoji = WEATHER_EMOJIS.get(condition, "🌫️")

    st.subheader(f"{emoji} Current Weather in {data['name']}, {sys.get('country', '')}")

    col1, col2, col3 = st.columns(3)
    with col1:
        st.metric("Description", weather["description"].title())
        st.metric("Temperature", f"{main['temp']:.1f} °C")
        st.metric("Feels Like", f"{main['feels_like']:.1f} °C")

    with col2:
        st.metric("Humidity", f"{main['humidity']}%")
        st.metric("Pressure", f"{main['pressure']} hPa")
        st.metric("Visibility", f"{data.get('visibility', 0)/1000:.1f} km")

    with col3:
        st.metric("Wind Speed", f"{wind['speed']} m/s")
        st.metric("Wind Direction", f"{wind.get('deg', 'N/A')}°")
        st.metric("Sunrise/Sunset", f"{format_time(sys['sunrise'])} / {format_time(sys['sunset'])}")

def display_forecast(forecast_data):
    if not forecast_data:
        return

    st.subheader("📅 5-Day Forecast")
    forecast_list = forecast_data['list']
    forecast_days = {}

    for item in forecast_list:
        date = datetime.datetime.fromtimestamp(item['dt']).strftime('%Y-%m-%d')
        forecast_days.setdefault(date, []).append(item)

    cols = st.columns(min(5, len(forecast_days)))
    for i, (date, day_data) in enumerate(forecast_days.items()):
        with cols[i % len(cols)]:
            day_name = datetime.datetime.strptime(date, '%Y-%m-%d').strftime('%a')
            avg_temp = sum(item['main']['temp'] for item in day_data) / len(day_data)
            conditions = [item['weather'][0]['main'].lower() for item in day_data]
            condition = max(set(conditions), key=conditions.count)
            emoji = WEATHER_EMOJIS.get(condition, "🌫️")
            st.metric(f"{day_name} {emoji}", f"{avg_temp:.1f}°C", help=f"Conditions: {condition.title()}")

def generate_mock_history(base_temp, base_humidity):
    dates = [datetime.date.today() - datetime.timedelta(days=i) for i in range(4, -1, -1)]
    return pd.DataFrame({
        "Date": [d.strftime("%Y-%m-%d") for d in dates],
        "Temperature (°C)": [round(base_temp + random.uniform(-5, 5), 1) for _ in dates],
        "Humidity (%)": [max(30, min(100, base_humidity + random.randint(-15, 15))) for _ in dates],
        "Precipitation (mm)": [round(random.uniform(0, 10), 1) for _ in dates]
    })

def create_visualizations(df):
    tab1, tab2, tab3 = st.tabs(["Temperature", "Humidity", "Precipitation"])

    with tab1:
        fig = px.line(df, x="Date", y="Temperature (°C)", title="Temperature Trends", markers=True)
        fig.update_traces(line_color='orange', fill='tozeroy')
        st.plotly_chart(fig, use_container_width=True)

    with tab2:
        fig = px.line(df, x="Date", y="Humidity (%)", title="Humidity Trends", markers=True)
        fig.update_traces(line_color='blue', fill='tozeroy')
        st.plotly_chart(fig, use_container_width=True)

    with tab3:
        fig = px.bar(df, x="Date", y="Precipitation (mm)", title="Precipitation (Last 5 Days)",
                     color="Precipitation (mm)", color_continuous_scale="blues")
        st.plotly_chart(fig, use_container_width=True)

# --- Main Application ---
def main():
    st.title("🌦️ Advanced Weather Dashboard")

    with st.sidebar:
        st.header("Quick Access")
        for quick_city in DEFAULT_CITIES:
            if st.button(quick_city):
                st.session_state.city = quick_city
                st.rerun()

        st.divider()
        st.subheader("📘 About")
        st.markdown("This dashboard provides real-time weather data and forecasts using the OpenWeatherMap API.")
        st.markdown("---")
        st.markdown("Made with ❤️ using Streamlit")

    if 'city' not in st.session_state:
        st.session_state.city = "London"

    city = st.text_input(
        "Enter city name:",
        value=st.session_state.city,
        key="city_input",
        help="Enter a valid city name (e.g., 'Paris', 'New York')"
    ).strip()

    if st.button("Get Weather", type="primary") or city != st.session_state.city:
        if not city:
            st.warning("⚠️ Please enter a city name")
            st.stop()

        if not all(c.isalpha() or c.isspace() or c in "-',." for c in city):
            st.error("❌ Invalid city name. Please use only letters, spaces, hyphens, or apostrophes.")
            st.stop()

        with st.spinner("🔍 Searching for weather data..."):
            weather_data = fetch_weather_data(city)
            forecast_data = fetch_forecast_data(city)
            if weather_data:
                st.session_state.city = city
                display_weather_card(weather_data)

                if forecast_data:
                    st.divider()
                    display_forecast(forecast_data)

                st.divider()
                st.subheader("📈 Historical Trends")
                mock_data = generate_mock_history(
                    base_temp=weather_data["main"]["temp"],
                    base_humidity=weather_data["main"]["humidity"]
                )
                create_visualizations(mock_data)

                st.download_button(
                    label="📥 Download Data as CSV",
                    data=mock_data.to_csv(index=False),
                    file_name=f"{city}_weather_data.csv",
                    mime="text/csv"
                )

if __name__ == "__main__":
    main()
