# app.py
import streamlit as st
import pandas as pd
import os
from datetime import datetime

from weather import get_weather_by_city, get_weather_by_pincode
from soil import get_soil_by_district  # optional: provides static soil mapping
from crop_recommender import recommend_crops, load_model_if_exists, build_context_from_inputs
from utils import ensure_reports_dir

st.set_page_config(page_title="Farmer Advisory AI", page_icon="🌾", layout="centered")
st.title("🌾 Farmer Advisory AI — MVP")
st.write("Use the sidebar to choose input mode. Upload soil readings (N,P,K,ph) or use district lookup + weather.")

# Sidebar
st.sidebar.header("Inputs")
mode = st.sidebar.selectbox("Input mode", ["Upload CSV (Kaggle)", "District", "City"])

# Load model if exists
model = load_model_if_exists()

# File uploader UI
if mode == "Upload CSV (Kaggle)":
    uploaded = st.file_uploader(
        "Upload CSV with columns: N,P,K,temperature,humidity,ph,rainfall,label (label optional)",
        type=["csv"]
    )
else:
    uploaded = None

if mode == "District":
    district = st.text_input("District name (e.g., Hyderabad)", value="Hyderabad")
elif mode == "City":
    city = st.text_input("City name (for weather lookup)", value="Hyderabad")
else:
    district = None
    city = None

st.markdown("**Sample input (CSV)**")
if os.path.exists("data/sample_farmer_input.csv"):
    st.code(open("data/sample_farmer_input.csv").read())

if st.button("🔍 Get Advisory"):
    try:
        reports = []

        if mode == "Upload CSV (Kaggle)":
            if not uploaded:
                st.error("Please upload CSV file in Kaggle format.")
                st.stop()
            df = pd.read_csv(uploaded)
            # Take first row as demo (later can loop through all rows)
            row = df.iloc[0].to_dict()
            soil_info = {
                "nitrogen": row.get("N") or row.get("n") or row.get("Nitrogen"),
                "phosphorus": row.get("P") or row.get("p") or row.get("Phosphorus"),
                "potassium": row.get("K") or row.get("k") or row.get("Potassium"),
                "ph_range": row.get("ph") or row.get("pH") or row.get("PH"),
                "soil_type": row.get("soil_type", "unknown")
            }
            context = build_context_from_inputs(
                soil_info=soil_info,
                weather_dict={
                    "temperature": row.get("temperature"),
                    "humidity": row.get("humidity"),
                    "rainfall": row.get("rainfall")
                }
            )
            temp = context["weather"]["temperature"]
            weather_main = None  # no weather string in CSV
            st.success(f"Using uploaded soil/weather values (temperature={temp})")

        elif mode == "District":
            if not district:
                st.error("Enter district.")
                st.stop()
            soil_info = get_soil_by_district(district)
            temp, weather_main, humidity, rainfall = get_weather_by_city(district)
            context = build_context_from_inputs(
                soil_info=soil_info,
                weather_dict={"temperature": temp, "humidity": humidity, "rainfall": rainfall}
            )
            st.success(f"Weather: {temp}°C, {weather_main} (humidity {humidity}%)")

        elif mode == "City":
            soil_info = None
            temp, weather_main, humidity, rainfall = get_weather_by_city(city)
            context = build_context_from_inputs(
                soil_info=None,
                weather_dict={"temperature": temp, "humidity": humidity, "rainfall": rainfall}
            )
            st.success(f"Weather: {temp}°C, {weather_main} (humidity {humidity}%)")

        # Show soil info and recommendations
        st.write("Soil info:", soil_info)
        recs = recommend_crops(soil_info=soil_info, weather_main=weather_main, model=model, context=context)

        st.write("### 🧾 Recommendations")
        for i, r in enumerate(recs, 1):
            st.write(f"{i}. {r}")
            reports.append(r)

        # Save report
        ensure_reports_dir()
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        report_path = os.path.join("reports", f"advisory_{timestamp}.csv")
        pd.DataFrame(
            {"recommendation": reports, "context": [str(context)]*len(reports)}
        ).to_csv(report_path, index=False)
        st.info(f"Saved report → `{report_path}`")

    except Exception as e:
        st.error(f"Error: {e}")
