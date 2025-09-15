# utils.py
import os

def ensure_reports_dir():
    os.makedirs("reports", exist_ok=True)
