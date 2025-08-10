# 🌦️ API-INTEGRATION-AND-DATA-VISUALIZATION

## Weather Dashboard with Streamlit & OpenWeatherMap API

This project is a **Weather Dashboard** built using **Python** and **Streamlit**. It integrates with the **OpenWeatherMap API** to fetch real-time weather data and uses **Plotly** for data visualization. The dashboard displays **current weather conditions** along with **mock historical trends** for temperature, humidity, and precipitation.

---

## ✅ Features

- Fetch real-time weather data from **OpenWeatherMap**
- Display **current weather** with emojis for conditions
- Show **5-day forecast** with average temperature per day
- Visualize **temperature, humidity, and precipitation trends** using **Plotly**
- Generate **mock historical data** for visualizations
- Download weather data as a **CSV file**
- Simple and responsive **Streamlit UI**
- **Error handling** and **API key protection** using `.env` file
- **Caching with `@st.cache_data`** for better performance

---

## 🛠 Technologies Used

- [Python](https://www.python.org/)
- [Streamlit](https://streamlit.io/)
- [Plotly](https://plotly.com/)
- [OpenWeatherMap API](https://openweathermap.org/api)
- [pandas](https://pandas.pydata.org/)
- [python-dotenv](https://pypi.org/project/python-dotenv/)

---

## 🚀 Getting Started (Step-by-Step Guide)

### ✅ Prerequisites
Ensure you have the following installed:
- **Python 3.8+** → [Download Python](https://www.python.org/downloads/)
- **Git** (optional, for cloning) → [Download Git](https://git-scm.com/)
- **OpenWeatherMap API Key** → [Get it here](https://openweathermap.org/api)

---

### 1️⃣ Clone or Download the Repository
Using Git:
git clone https://github.com/Praneesh-Gattadi/API-INTEGRATION-AND-DATA-VISUALIZATION.git
cd API-INTEGRATION-AND-DATA-VISUALIZATION
Or download ZIP from GitHub and extract it.

2️⃣ Set Up a Virtual Environment (Recommended)
Create and activate a virtual environment:

python -m venv env

Activate it
On Windows:
env\Scripts\activate
On macOS/Linux:
source env/bin/activate

3️⃣ Install Dependencies
Create a requirements.txt file with:

streamlit
requests
pandas
plotly
python-dotenv

Then install:
pip install -r requirements.txt

4️⃣ Get Your OpenWeatherMap API Key
Sign up at OpenWeatherMap

Go to Profile > API Keys

Copy your API key


5️⃣ Configure Environment Variables
Create a .env file in the project root:
OPENWEATHER_API_KEY=your_api_key_here
important: Add .env to .gitignore:
.env

6️⃣ Run the Weather Dashboard
Start the app:
streamlit run app.py
You should see the dashboard at:
http://localhost:8501

Alternative way:

Copy your app.py path

Open CMD or Terminal:

cd path_to_your_file
streamlit run app.py

📌 Project Structure

API-INTEGRATION-AND-DATA-VISUALIZATION/

├── app.py               
├── requirements.txt     
├── .env                 
└── README.md            

💡 Notes

Make sure your API key is valid and active.

Free OpenWeatherMap API allows 60 calls per minute.

Do NOT share your .env file publicly.

## OUTPUT

<img width="1366" height="768" alt="Image" src="https://github.com/user-attachments/assets/eb740d61-e3d8-4c94-b2e1-57c75b619ee5" />
<img width="1366" height="768" alt="Image" src="https://github.com/user-attachments/assets/81f11835-043b-4b09-a70f-8fb06978ec11" />
<img width="1366" height="768" alt="Image" src="https://github.com/user-attachments/assets/1f1c1519-bad5-4361-ac06-e51a936eb352" />
<img width="1366" height="768" alt="Image" src="https://github.com/user-attachments/assets/85d1bcf2-bf09-4c34-8831-f282f8d655ac" />
<img width="1366" height="768" alt="Image" src="https://github.com/user-attachments/assets/52946539-61cc-491b-a88e-74cfe10d1990" />

✨ Author: Praneesh Gattadi
Made with ❤️ using Streamlit
