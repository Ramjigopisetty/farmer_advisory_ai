# weather.py
import os
import requests

# Option: hardcode your OpenWeatherMap API key here (for quick testing)
OPENWEATHER_API_KEY = "cf9a5491918b00301e5e151cf10fbaed"  # <-- replace with your key or set to "" to disable

def get_weather_by_city(city_name):
    return _fetch_current_weather(q=city_name)

def get_weather_by_pincode(pincode, country_code="IN"):
    return _fetch_current_weather(zip=f"{pincode},{country_code}")

def _fetch_current_weather(q=None, zip=None):
    if not OPENWEATHER_API_KEY or OPENWEATHER_API_KEY == "cf9a5491918b00301e5e151cf10fbaed":
        # No API key — return Nones so app can still run with uploaded CSV
        return None, None, None, None

    base = "https://api.openweathermap.org/data/2.5/weather"
    params = {"appid": OPENWEATHER_API_KEY, "units": "metric"}
    if q:
        params["q"] = q
    if zip:
        params["zip"] = zip

    r = requests.get(base, params=params, timeout=8)
    r.raise_for_status()
    data = r.json()

    temp = data.get("main", {}).get("temp")
    humidity = data.get("main", {}).get("humidity")
    rain = 0.0
    if isinstance(data.get("rain", {}), dict):
        rain = data.get("rain", {}).get("1h", data.get("rain", {}).get("3h", 0.0)) or 0.0
    weather_main = data.get("weather", [{}])[0].get("main")
    return temp, weather_main, humidity, rain
