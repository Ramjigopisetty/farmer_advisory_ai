# crop_recommender.py
import os
import joblib
import pandas as pd

MODEL_PATH = os.path.join("models", "crop_model.joblib")

def load_model_if_exists():
    if os.path.exists(MODEL_PATH):
        try:
            return joblib.load(MODEL_PATH)
        except Exception:
            return None
    return None

def build_context_from_inputs(soil_info=None, weather_dict=None):
    """
    Return a context dict used by app and by ML predictor.
    weather_dict: {"temperature":..., "humidity":..., "rainfall":...}
    """
    ctx = {"weather": {"temperature": None, "humidity": None, "rainfall": None}}
    if weather_dict:
        ctx["weather"]["temperature"] = weather_dict.get("temperature")
        ctx["weather"]["humidity"] = weather_dict.get("humidity")
        ctx["weather"]["rainfall"] = weather_dict.get("rainfall")
    return ctx

def _features_from_input(soil_info=None, context=None):
    # ensure numeric features exist; fill fallback zeros
    N = float(soil_info.get("nitrogen") or 0) if soil_info else 0.0
    P = float(soil_info.get("phosphorus") or 0) if soil_info else 0.0
    K = float(soil_info.get("potassium") or 0) if soil_info else 0.0
    ph = float(soil_info.get("ph_range") or soil_info.get("ph") or 0) if soil_info else 0.0

    temp = None
    hum = None
    rain = None
    if context and isinstance(context, dict):
        w = context.get("weather", {})
        temp = w.get("temperature", 0)
        hum = w.get("humidity", 0)
        rain = w.get("rainfall", 0)
    # cast floats, fallback 0
    features = {
        "N": float(N or 0),
        "P": float(P or 0),
        "K": float(K or 0),
        "temperature": float(temp or 0),
        "humidity": float(hum or 0),
        "ph": float(ph or 0),
        "rainfall": float(rain or 0)
    }
    return pd.DataFrame([features], columns=["N","P","K","temperature","humidity","ph","rainfall"])

def recommend_crops(soil_info=None, weather_main=None, model=None, context=None):
    """
    Returns list[str] recommendations. Prefers ML prediction (if model available), falls back to rule-based heuristics.
    """
    recs = []

    # Try ML first if model available
    if model is not None and soil_info is not None:
        try:
            X = _features_from_input(soil_info=soil_info, context=context)
            pred = model.predict(X)
            if len(pred) > 0:
                recs.append(f"ML Suggestion: {pred[0]}")
        except Exception:
            # ignore and fall back
            pass

    # Rule-based heuristics
    soil_type = (soil_info.get("soil_type") or "").lower() if soil_info else ""
    try:
        ph = float(soil_info.get("ph_range")) if soil_info and soil_info.get("ph_range") not in (None, "") else None
    except Exception:
        ph = None
    try:
        n = float(soil_info.get("nitrogen") or 0)
        p = float(soil_info.get("phosphorus") or 0)
        k = float(soil_info.get("potassium") or 0)
    except Exception:
        n = p = k = 0.0

    # soil-type hints
    if "loamy" in soil_type:
        recs.append("Loamy — rice, wheat, maize (season dependent).")
    elif "black" in soil_type:
        recs.append("Black soil — cotton, sugarcane.")
    elif "sandy" in soil_type:
        recs.append("Sandy — millet, groundnut, pulses.")

    # nutrient heuristics
    if n >= 45 and p >= 25 and k >= 20:
        recs.append("High NPK — many cereals and vegetables suitable.")
    elif n < 20 or p < 15 or k < 10:
        recs.append("Low nutrients — apply balanced fertilizer before nutrient-demanding crops.")

    # pH heuristics
    if ph is not None:
        if ph < 6.0:
            recs.append("Acidic (pH<6) — rice, tea, potato suitable.")
        elif ph > 7.5:
            recs.append("Alkaline (pH>7.5) — barley, sugarcane, cotton suitable.")

    # weather-based hints from weather_main or context
    wstr = ""
    if isinstance(weather_main, str):
        wstr = weather_main.lower()
    elif context and isinstance(context, dict):
        w = context.get("weather", {})
        temp = w.get("temperature") if w else None
        # if rainfall present and large, add note
        if w and float(w.get("rainfall") or 0) > 10:
            recs.append("Recent/expected rain — consider water-tolerant/monsoon crops.")
        if temp and float(temp) > 30:
            recs.append("High temperature — favor heat tolerant crops or irrigation.")

    if "rain" in wstr:
        recs.append("Rain predicted — sow monsoon crops and water-tolerant varieties.")
    if "clear" in wstr or "sun" in wstr:
        recs.append("Clear weather — prepare irrigation and fast-moving supplies.")

    if not recs:
        recs.append("No strong match — collect more local data or consult extension services.")

    return recs
