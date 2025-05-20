# Import required libraries
import os                   # For environment variables and file operations
import requests             # For making API requests to OpenWeatherMap
import matplotlib.pyplot as plt  # For data visualization
from datetime import datetime   # For handling timestamps
from dotenv import load_dotenv  # For loading API keys securely from .env file

# Load environment variables from .env file (where API key is stored)
load_dotenv()
API_KEY = os.getenv("OPENWEATHER_API_KEY")  # Fetch API key from .env

def fetch_weather_data(city_name):
    """
    Fetches weather forecast data from OpenWeatherMap API.
    
    Args:
        city_name (str): Name of the city to fetch weather data for.
    
    Returns:
        dict: JSON response containing weather data if successful, None otherwise.
    """
    base_url = "http://api.openweathermap.org/data/2.5/forecast"  # API endpoint
    params = {
        'q': city_name,      # City name from user input
        'appid': API_KEY,    # API key (loaded from .env)
        'units': 'metric'    # Use metric units (Celsius, m/s, etc.)
    }
    
    try:
        # Make GET request to OpenWeatherMap API
        response = requests.get(base_url, params=params)
        response.raise_for_status()  # Raise exception for HTTP errors (4xx/5xx)
        return response.json()      # Return parsed JSON data
        
    except requests.exceptions.RequestException as e:
        # Handle network errors, invalid API keys, or city not found
        print(f"Error fetching data: {e}")
        return None

def create_visualizations(data):
    """
    Generates a 4-panel weather dashboard using matplotlib.
    
    Args:
        data (dict): Weather data fetched from OpenWeatherMap API.
    """
    if not data:
        print("No data to visualize!")
        return

    # Extract relevant data points from API response
    forecasts = data['list']  # List of forecast entries (each 3 hours apart)
    
    # Extract timestamps and convert to readable format
    timestamps = [f['dt_txt'] for f in forecasts]  # Original timestamps (strings)
    dates = [datetime.strptime(ts, "%Y-%m-%d %H:%M:%S") for ts in timestamps]  # Convert to datetime objects
    
    # Extract weather metrics
    temps = [f['main']['temp'] for f in forecasts]        # Temperature in °C
    humidity = [f['main']['humidity'] for f in forecasts] # Humidity in %
    wind_speed = [f['wind']['speed'] for f in forecasts]  # Wind speed in m/s
    pressure = [f['main']['pressure'] for f in forecasts] # Pressure in hPa

    # Create a 2x2 grid of subplots (dashboard layout)
    fig, axes = plt.subplots(2, 2, figsize=(15, 10))
    fig.suptitle(f"Weather Dashboard for {data['city']['name']}", fontsize=16)

    # Plot 1: Temperature Trend (Line Graph)
    axes[0, 0].plot(dates, temps, color='red', marker='o')
    axes[0, 0].set_title("Temperature (°C)")
    axes[0, 0].set_xlabel("Time")
    axes[0, 0].grid(True)

    # Plot 2: Humidity Trend (Bar Chart)
    axes[0, 1].bar(dates, humidity, color='blue', alpha=0.7)
    axes[0, 1].set_title("Humidity (%)")
    axes[0, 1].set_xlabel("Time")
    axes[0, 1].grid(True)

    # Plot 3: Wind Speed (Scatter Plot)
    axes[1, 0].scatter(dates, wind_speed, color='green')
    axes[1, 0].set_title("Wind Speed (m/s)")
    axes[1, 0].set_xlabel("Time")
    axes[1, 0].grid(True)

    # Plot 4: Pressure Trend (Line Graph)
    axes[1, 1].plot(dates, pressure, color='purple', linestyle='--')
    axes[1, 1].set_title("Pressure (hPa)")
    axes[1, 1].set_xlabel("Time")
    axes[1, 1].grid(True)

    # Adjust layout to prevent overlapping
    plt.tight_layout()
    plt.show()

if __name__ == "__main__":
    # Main execution block
    print("=== Weather Data Visualization Dashboard ===")
    city = input("Enter city name (e.g., London, Tokyo): ").strip()
    
    # Fetch data and generate visualizations
    weather_data = fetch_weather_data(city)
    if weather_data:
        create_visualizations(weather_data)
    else:
        print("Failed to fetch weather data. Please check:")
        print("- Your API key in .env file")
        print("- City name spelling")
        print("- Internet connection")
