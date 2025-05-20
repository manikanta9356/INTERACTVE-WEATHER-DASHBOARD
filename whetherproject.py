# weather_app.py

#Import Required Libraries
import requests                      # For making HTTP requests to OpenWeather API
import pandas as pd                 # For handling tabular data
import matplotlib.pyplot as plt     # For creating visualizations
import seaborn as sns               # For advanced plotting (used with matplotlib)
from datetime import datetime       # For working with timestamps
import os                           # For accessing environment variables
from dotenv import load_dotenv      # To load environment variables from .env file

# Load API Key from .env File
load_dotenv()
API_KEY = os.getenv("OPENWEATHER_API_KEY")  # Ensure your .env file has: OPENWEATHER_API_KEY=your_key

# User Input 
CITY = input("Enter City Name: ").strip()

# Function: Fetch Weather Data from OpenWeather API 
def get_weather_data():
    """
    Fetches current weather and 5-day forecast data from OpenWeatherMap API.
    Returns two dictionaries: current weather data and forecast data.
    """
    try:
        print(f"\nFetching weather data for '{CITY}'...")

        # API URL for current weather
        current_url = f"http://api.openweathermap.org/data/2.5/weather?q={CITY}&appid={API_KEY}&units=metric"
        current_response = requests.get(current_url)
        current_response.raise_for_status()  # Raises error for HTTP error codes
        current_data = current_response.json()

        # API URL for 5-day forecast (3-hour interval data)
        forecast_url = f"http://api.openweathermap.org/data/2.5/forecast?q={CITY}&appid={API_KEY}&units=metric"
        forecast_response = requests.get(forecast_url)
        forecast_response.raise_for_status()
        forecast_data = forecast_response.json()

        print("Data fetched successfully.")
        return current_data, forecast_data

    except requests.exceptions.RequestException as e:
        print(f"\nERROR: Failed to fetch data\n{str(e)}")
        print("Troubleshooting Tips:")
        print("   1. Check if your API key is valid.")
        print("   2. Ensure you have an active internet connection.")
        print("   3. Try using a different city name.\n")
        return None, None

# Function: Process Raw API Data into DataFrames
def process_data(current, forecast):
    """
    Transforms raw current and forecast JSON data into structured pandas DataFrames.
    Returns: current_df, forecast_df
    """
    try:
        # Create DataFrame for current weather data
        current_df = pd.DataFrame({
            'City': [current['name']],
            'Temperature': [current['main']['temp']],
            'Feels_Like': [current['main']['feels_like']],
            'Humidity': [current['main']['humidity']],
            'Wind_Speed': [current['wind']['speed']],
            'Conditions': [current['weather'][0]['main']],
            'Timestamp': [datetime.fromtimestamp(current['dt'])]
        })

        # Parse 5-day forecast data (at 3-hour intervals)
        forecast_list = []
        for entry in forecast['list'][:40]:  # Next 5 days = 40 intervals
            forecast_list.append({
                'DateTime': datetime.fromtimestamp(entry['dt']),
                'Temperature': entry['main']['temp'],
                'Humidity': entry['main']['humidity'],
                'Wind_Speed': entry['wind']['speed'],
                'Conditions': entry['weather'][0]['main']
            })

        forecast_df = pd.DataFrame(forecast_list)
        return current_df, forecast_df

    except Exception as e:
        print(f"\nERROR: Data processing failed\n{str(e)}\n")
        return None, None

#Function: Create and Save Weather Visualizations
def create_visualizations(current, forecast):
    """
    Creates a 2x2 dashboard plot showing weather trends and statistics.
    Saves the figure as 'weather_dashboard.png'.
    """
    try:
        # Use modern seaborn styling
        plt.style.use('seaborn-v0_8-darkgrid')

        # Set up the subplot grid (2 rows x 2 columns)
        fig, axes = plt.subplots(2, 2, figsize=(15, 10))
        fig.suptitle(f"Weather Dashboard for {current['City'].iloc[0]}", fontsize=16)

        #Plot 1: Current Weather Metrics
        metrics = ['Temperature', 'Feels_Like', 'Humidity', 'Wind_Speed']
        values = current[metrics].values[0]
        axes[0, 0].bar(metrics, values, color=['#FF6B6B', '#45B7D1', '#4ECDC4', '#A37AFC'])
        axes[0, 0].set_title('Current Weather Snapshot')

        # Plot 2: 5-Day Temperature Trend
        sns.lineplot(x='DateTime', y='Temperature', data=forecast,
                     ax=axes[0, 1], marker='o', color='#FF6B6B')
        axes[0, 1].set_title('5-Day Temperature Forecast')
        axes[0, 1].tick_params(axis='x', rotation=45)

        # Plot 3: Frequency of Weather Conditions
        forecast['Conditions'].value_counts().plot(
            kind='bar', ax=axes[1, 0], color='#4ECDC4')
        axes[1, 0].set_title('Weather Conditions Frequency')

        #Plot 4: Wind Speed vs Humidity Scatter Plot
        scatter = sns.scatterplot(x='Wind_Speed', y='Humidity', data=forecast,
                                  hue='Temperature', ax=axes[1, 1], palette='viridis')
        axes[1, 1].set_title('Wind vs Humidity Correlation')
        axes[1, 1].set_xlabel('Wind Speed (m/s)')
        axes[1, 1].set_ylabel('Humidity (%)')
        scatter.legend(title='Temp (°C)')

        # Final layout adjustments
        plt.tight_layout()
        plt.savefig('weather_dashboard.png', dpi=300, bbox_inches='tight')
        print("Dashboard saved as 'weather_dashboard.png'.")
        plt.show()

        return fig

    except Exception as e:
        print(f"\nERROR: Visualization failed\n{str(e)}\n")
        return None

#Main Program Execution
if __name__ == "__main__":
    print("\n=== Weather Dashboard Program ===\n")

    # Step 1: Fetch data from API
    current_raw, forecast_raw = get_weather_data()

    # Step 2: Process the data
    if current_raw and forecast_raw:
        current_df, forecast_df = process_data(current_raw, forecast_raw)

        # Step 3: Create visualizations and save results
        if current_df is not None and forecast_df is not None:
            dashboard = create_visualizations(current_df, forecast_df)

            # Step 4: Save processed data as CSV
            current_df.to_csv('current_weather.csv', index=False)
            forecast_df.to_csv('weather_forecast.csv', index=False)
            print("Data saved as 'current_weather.csv' and 'weather_forecast.csv'.")

    print("\nProgram completed. Check your files and visualizations.\n")
