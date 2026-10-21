"""Train and persist the password-strength classifier.

Improvements over the original:
* Regenerates a balanced labelled dataset if it is missing.
* Uses a stratified train/test split with a fixed seed for reproducibility.
* Reports per-class metrics *and* cross-validated accuracy.
* Persists the model, the label encoder and the feature schema together in a
  single ``models/model.pkl`` bundle (the old ``vectorizer.pkl`` name was
  misleading — it never held a vectoriser).
"""

from __future__ import annotations

import os

import joblib
import pandas as pd
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import classification_report
from sklearn.model_selection import cross_val_score, train_test_split
from sklearn.preprocessing import LabelEncoder

from utils.console import enable_utf8
from utils.data_preprocessing import generate_labeled_csv
from utils.feature_extractor import FEATURE_NAMES, extract_features

enable_utf8()

DATA_PATH = "data/labeled_passwords.csv"
MODEL_PATH = "models/model.pkl"


def load_dataset(path: str = DATA_PATH) -> pd.DataFrame:
    if not os.path.exists(path):
        print("ℹ️  Labelled dataset not found — generating it now...")
        generate_labeled_csv(out_path=path)
    return pd.read_csv(path)


def main() -> None:
    df = load_dataset()
    df = df.dropna(subset=["password"]).astype({"password": str})

    X = df["password"].apply(extract_features).tolist()
    y = df["strength"]

    le = LabelEncoder()
    y_encoded = le.fit_transform(y)

    X_train, X_test, y_train, y_test = train_test_split(
        X, y_encoded, test_size=0.2, random_state=42, stratify=y_encoded
    )

    clf = RandomForestClassifier(n_estimators=200, random_state=42, n_jobs=-1)
    clf.fit(X_train, y_train)

    y_pred = clf.predict(X_test)
    print("\n📊 Classification report (held-out test set):\n")
    print(classification_report(
        y_test, y_pred, labels=le.transform(le.classes_), target_names=le.classes_
    ))

    cv = cross_val_score(clf, X, y_encoded, cv=5, n_jobs=-1)
    print(f"🔁 5-fold cross-validated accuracy: {cv.mean():.3f} ± {cv.std():.3f}\n")

    importances = sorted(
        zip(FEATURE_NAMES, clf.feature_importances_), key=lambda kv: kv[1], reverse=True
    )
    print("🏅 Top feature importances:")
    for name, weight in importances[:6]:
        print(f"   {name:<22} {weight:.3f}")

    os.makedirs(os.path.dirname(MODEL_PATH), exist_ok=True)
    joblib.dump(
        {"model": clf, "label_encoder": le, "features": list(FEATURE_NAMES)},
        MODEL_PATH,
    )
    print(f"\n✅ Model bundle saved to {MODEL_PATH}")


if __name__ == "__main__":
    main()
