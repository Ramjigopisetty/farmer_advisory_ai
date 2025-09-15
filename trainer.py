# trainer.py
import pandas as pd
import os
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split
import joblib

DATA_CSV = os.path.join("data", "crop_dataset_sample.csv")
MODEL_DIR = "models"
MODEL_PATH = os.path.join(MODEL_DIR, "crop_model.joblib")

def train_simple_model():
    if not os.path.exists(DATA_CSV):
        raise FileNotFoundError(f"{DATA_CSV} not found. Place Kaggle dataset at this path.")
    df = pd.read_csv(DATA_CSV)
    required = ["N","P","K","temperature","humidity","ph","rainfall","label"]
    missing = [c for c in required if c not in df.columns]
    if missing:
        raise ValueError(f"Missing columns in dataset: {missing}")

    df = df.fillna(0)
    X = df[["N","P","K","temperature","humidity","ph","rainfall"]]
    y = df["label"]

    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)
    clf = RandomForestClassifier(n_estimators=200, random_state=42)
    clf.fit(X_train, y_train)

    print("Train accuracy:", clf.score(X_train, y_train))
    print("Test accuracy:", clf.score(X_test, y_test))

    os.makedirs(MODEL_DIR, exist_ok=True)
    joblib.dump(clf, MODEL_PATH)
    print("Saved model to", MODEL_PATH)

if __name__ == "__main__":
    train_simple_model()
