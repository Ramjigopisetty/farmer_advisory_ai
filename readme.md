# Farmer Advisory AI — MVP

## Quick start
1. Create virtualenv
   ```bash
   python -m venv venv
   source venv/bin/activate   # mac/linux
   venv\Scripts\activate      # windows
Install dependencies

bash
Copy code
pip install -r requirements.txt
Set environment variables (recommended):

bash
Copy code
export OPENWEATHER_API_KEY="your_openweathermap_key"
(Optional) Train simple model:

bash
Copy code
python trainer.py
Run the Streamlit app:

bash
Copy code
streamlit run app.py