# soil.py
import pandas as pd
import os

SOIL_CSV = os.path.join("data", "soil_data.csv")  # put your district soil CSV here
_soil_df = None

def _normalize_cols(df):
    rename = {}
    for c in df.columns:
        key = c.strip().lower()
        if "district" in key:
            rename[c] = "district"
        elif "nitrogen" in key or key == "n":
            rename[c] = "nitrogen"
        elif "phosphor" in key or key == "p":
            rename[c] = "phosphorus"
        elif "potassium" in key or key == "k":
            rename[c] = "potassium"
        elif key in ("ph", "p_h"):
            rename[c] = "ph"
        elif "soil" in key and "type" in key:
            rename[c] = "soil_type"
        else:
            rename[c] = key.replace(" ", "_")
    return df.rename(columns=rename)

def _load_soil():
    global _soil_df
    if _soil_df is None:
        if not os.path.exists(SOIL_CSV):
            # no file: return empty df
            _soil_df = pd.DataFrame()
            return _soil_df
        df = pd.read_csv(SOIL_CSV)
        df = _normalize_cols(df)
        if "district" in df.columns:
            df["district"] = df["district"].astype(str).str.strip().str.lower()
        _soil_df = df
    return _soil_df

def get_soil_by_district(district_name):
    df = _load_soil()
    if df.empty:
        return {"soil_type": "unknown", "ph_range": None, "nitrogen": None, "phosphorus": None, "potassium": None}
    dn = str(district_name).strip().lower()
    rows = df[df["district"] == dn]
    if rows.empty:
        # partial match
        rows = df[df["district"].str.contains(dn.split()[0]) if dn else False]
    if not rows.empty:
        r = rows.iloc[0].to_dict()
        return {
            "soil_type": r.get("soil_type", "unknown"),
            "ph_range": r.get("ph"),
            "nitrogen": r.get("nitrogen"),
            "phosphorus": r.get("phosphorus"),
            "potassium": r.get("potassium")
        }
    return {"soil_type": "unknown", "ph_range": None, "nitrogen": None, "phosphorus": None, "potassium": None}
