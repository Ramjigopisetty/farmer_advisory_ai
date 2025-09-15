# 🌾 Farmer Advisory AI

An AI-powered system to help farmers select the best crops based on soil and weather conditions. The system provides crop recommendations in multiple languages and can also generate audio advice for accessibility.

---

## Problem Statement
Farmers often struggle to decide which crops to cultivate due to limited access to expert guidance, soil data, and accurate weather information. Incorrect decisions can lead to low yield, financial loss, and inefficient resource use. This project provides a smart solution to guide farmers with real-time crop recommendations.

---

## Solution Overview
- **Input Options:** Farmers can provide data by:
  - Uploading a CSV with soil readings (N, P, K, pH, temperature, humidity, rainfall)
  - Entering their district or city to fetch soil and weather data
- **AI Analysis:** A machine learning model evaluates soil nutrients and weather to recommend the most suitable crops.
- **Output:** Recommendations are provided in:
  - Text format (English and regional languages)
  - Audio format using text-to-speech for accessibility

---

## Features
- Crop recommendation based on soil nutrients and weather
- Multi-language support (Hindi, Telugu, Tamil, Bengali, Marathi)
- Audio output for easy understanding
- Reports are saved in CSV format for tracking
- Rule-based fallback if ML model is unavailable

---

## Project Structure

farmer_advisor/
├── app.py # Streamlit app
├── weather.py # Weather fetching module
├── soil.py # Soil data processing
├── crop_recommender.py # ML model & rule-based crop recommender
├── translator_speech.py # Translation & text-to-speech
├── trainer.py # Script to train crop recommendation model
├── utils.py # Utility functions (reports folder etc.)
├── requirements.txt # Python dependencies
├── README.md # Project documentation
└── data/
├── crop_dataset_sample.csv # Sample crop dataset
├── sample_farmer_input.csv # Example CSV for upload mode
└── soil_map_sample.csv # Soil data mapping

yaml
Copy code

---

## Setup Instructions

1. **Clone the repository**  
   ```bash
   git clone <your-repo-url>
   cd farmer_advisor
Create and activate a virtual environment

bash
Copy code
python -m venv venv
venv\Scripts\activate    # Windows
# source venv/bin/activate   # Mac/Linux
Install dependencies

bash
Copy code
pip install -r requirements.txt
Place your datasets

Ensure crop_dataset_sample.csv and soil_map_sample.csv are in the data/ folder.

Train the ML model

bash
Copy code
python trainer.py
This will generate models/crop_model.joblib.

Run the Streamlit app

bash
Copy code
streamlit run app.py
The app will open in your browser at http://localhost:8501.

How to Use
Open the sidebar and choose Input Mode:

Upload CSV (Kaggle format) – Provide soil readings from CSV

District – Enter your district to fetch soil & weather data

City – Enter your city to fetch weather data only

Select the Output Language for text and audio.

Click Get Advisory:

Soil info and weather are displayed

Crop recommendations appear

Reports are saved in the reports/ folder

Optional: play or download audio advice

Notes
For testing, you can use sample_farmer_input.csv provided in data/.

Ensure you have internet connectivity for fetching live weather data.

The system uses a fallback rule-based method if the ML model is unavailable.

Future Improvements
Integrate real-time soil sensors

Expand district & state coverage

Add more languages and audio quality improvements

Deploy as a mobile app for easier farmer access