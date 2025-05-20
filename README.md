# -API-INTEGRATION-AND-DATA-VISUALIZATION

COMPANY: CODTECH IT SOLUTIONS

NAME: Gattadi Manikanta

INTERN ID: CT04DM1361

DOMAIN: Python Programming

DURATION: 4 Weeks

MENTOR: NEELA SANTOSH

# wheather integration and data visualization.

This Python-based Weather Dashboard Application is a command-line tool designed to fetch and visualize weather data for a specified city using the OpenWeatherMap API. The script allows users to input a city name, after which it retrieves both the current weather conditions and a 5-day forecast broken into 3-hour intervals.

Current Weather Retrieval: Retrieves real-time weather data for any user-input city.

5-Day Forecast: Fetches a detailed 5-day forecast with 3-hour intervals (up to 40 time points).

Data Processing: Transforms raw JSON responses into well-structured pandas DataFrames.

Visualizations: Creates and saves a dashboard consisting of four informative subplots.

CSV Export: Saves processed data into CSV files for current and forecast weather.

Error Handling: Includes robust error handling for failed API requests and data processing steps.

Modules and Workflow
1. User Input
The program prompts the user to enter a city name. This city name is used in the API requests to fetch the respective weather data.

2. Fetching Weather Data
The get_weather_data() function connects to the OpenWeatherMap API using the city name and a secure API key stored in a .env file. It fetches two sets of data:

Current Weather Data

5-Day Forecast Data (in 3-hour intervals)

Both datasets are returned as JSON objects.

3. Processing API Responses
The process_data() function converts the JSON responses into two pandas DataFrames:

current_df holds real-time weather metrics such as temperature, humidity, wind speed, and conditions.

forecast_df contains forecast data over the next five days, including temperature trends, humidity, wind speed, and conditions.

Datetime fields are converted from UNIX timestamps to human-readable formats using the datetime module.

4. Visualization
The create_visualizations() function creates a 2x2 subplot dashboard using matplotlib and seaborn. The plots include:

Bar Chart: Snapshot of current temperature, humidity, wind speed, and "feels like" temperature.

Line Plot: 5-day temperature forecast.

Bar Chart: Frequency of various weather conditions (e.g., Clear, Rain).

Scatter Plot: Correlation between wind speed and humidity, colored by temperature.

The dashboard is saved as a high-resolution PNG image (weather_dashboard.png) and displayed to the user.

5. CSV Export
The processed DataFrames are saved locally as:

current_weather.csv

weather_forecast.csv

These files can be reused for analysis, visualization, or integration with other tools.

#output

![Image](https://github.com/user-attachments/assets/7c224684-214e-4a15-9023-94b161bce9a1)


![Image](https://github.com/user-attachments/assets/c7a997fb-78e9-4c23-831e-8d674ec545a5)

