# weather.py
import requests
import streamlit as st

# Load API key securely from Streamlit secrets
OPENWEATHER_API_KEY = st.secrets["OPENWEATHER_API_KEY"]

def get_weather_by_city(city_name):
    return _fetch_current_weather(q=city_name)

def get_weather_by_pincode(pincode, country_code="IN"):
    return _fetch_current_weather(zip=f"{pincode},{country_code}")

def _fetch_current_weather(q=None, zip=None):
    if not OPENWEATHER_API_KEY:
        return None, None, None, None

    base = "https://api.openweathermap.org/data/2.5/weather"
    params = {"appid": OPENWEATHER_API_KEY, "units": "metric"}
    if q:
        params["q"] = q
    if zip:
        params["zip"] = zip

    try:
        r = requests.get(base, params=params, timeout=8)
        r.raise_for_status()
        data = r.json()
    except Exception as e:
        st.error(f"Weather API error: {e}")
        return None, None, None, None

    temp = data.get("main", {}).get("temp")
    humidity = data.get("main", {}).get("humidity")
    rain = 0.0
    if isinstance(data.get("rain", {}), dict):
        rain = data.get("rain", {}).get("1h", data.get("rain", {}).get("3h", 0.0)) or 0.0
    weather_main = data.get("weather", [{}])[0].get("main")
    return temp, weather_main, humidity, rain
