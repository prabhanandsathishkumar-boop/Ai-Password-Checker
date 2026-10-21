# 🔐 PassStrength AI – Smart Password Strength Checker with Machine Learning

PassStrength AI is an intelligent password-strength analyser. Unlike traditional
rule-based meters, it combines a **machine-learning classifier** trained on real
leaked passwords with an **information-theoretic engine** (Shannon & search-space
entropy), **pattern detection**, **crack-time estimation**, and **actionable
feedback** — exposed through a CLI *and* a REST API with a live web UI.

---

## ✨ Features

| Capability | Description |
|---|---|
| 🧠 **ML classifier** | RandomForest over 13 engineered features (entropy, diversity, sequences, repeats, keyboard walks, common-word & leak detection). ~97% cross-validated accuracy. |
| 📊 **Entropy analysis** | Shannon entropy *and* brute-force search-space entropy in bits. |
| ⏱️ **Crack-time estimate** | Human-readable "time to crack" at an offline-GPU guess rate (10B guesses/s). |
| 🔍 **Pattern detection** | Catches `abc`/`123` sequences, `aaa` repeats, `qwerty` keyboard walks, leet-speak common words (`P@ssw0rd`). |
| 💡 **Actionable feedback** | Tells you *why* a password is weak and *how* to fix it. |
| 🌐 **REST API + Web UI** | FastAPI backend with a zero-build, real-time HTML front-end. |
| ✅ **Tested** | 18 `pytest` cases covering the engine, features and API. |

---

## 🚀 Quick start

```bash
# 1. Install dependencies
pip install -r requirements.txt

# 2. Build the labelled dataset (leaked + synthetic, composite-scored labels)
python run_preprocessing.py

# 3. Train the model (saves a model bundle to models/model.pkl)
python train_model.py

# 4a. Analyse from the command line
python -m app.cli_analyzer "MyP@ssw0rd!"

# 4b. …or launch the web app + REST API
uvicorn app.api:app --reload
# open http://127.0.0.1:8000
```

### REST API

```bash
curl -X POST http://127.0.0.1:8000/api/analyze \
     -H "Content-Type: application/json" \
     -d '{"password":"Tr0ub4dour&3xK"}'
```

```jsonc
{
  "length": 14,
  "score": 99,
  "label": "Very Strong",
  "shannon_entropy": 47.5,
  "search_space_entropy": 91.7,
  "crack_time_human": "6.67e+07 centuries",
  "is_common": false,
  "feedback": ["Great password! Consider storing it in a password manager."],
  "ml_label": "Very Strong",
  "features": { "...": "..." }
}
```

Interactive docs are auto-generated at `http://127.0.0.1:8000/docs`.

---

## 🏗️ Project structure

```
ai-password-checker/
├── app/
│   ├── api.py            # FastAPI REST + web UI
│   ├── cli_analyzer.py   # rich command-line analyser
│   ├── predictor.py      # shared ML + heuristic prediction layer
│   └── static/index.html # live front-end
├── utils/
│   ├── strength.py          # entropy, crack-time, scoring, feedback (no deps)
│   ├── feature_extractor.py # 13-feature ML vector
│   ├── data_preprocessing.py# balanced dataset builder (composite labels)
│   └── console.py           # UTF-8 console helper (Windows-safe emoji)
├── tests/                # pytest suite
├── data/                 # raw + labelled passwords
├── models/               # trained model bundle
├── notebooks/            # training walkthrough
├── train_model.py
└── run_preprocessing.py
```

## 🔬 Why this is more than a rule-based meter

The original version labelled passwords **purely by length**, so the model could
only ever relearn length. This upgrade labels training data with a **composite
score** (entropy + character diversity − pattern penalties) and balances the
dataset with synthetic passwords across the whole spectrum. The trained model's
top signals are now `search_space_entropy`, `shannon_entropy` and `length` — it
genuinely learns what makes a password hard to guess.

## 🧪 Tests

```bash
python -m pytest -q
```

---

## 🔐 Disclaimer

This tool is for educational and research purposes only. It **does not store any
password** — all processing happens locally and in-memory.

---

## 🧠 Authors

Originally created by [Balakavi](https://instagram.com/kavi.s_netwrok/) — `#KavisNetwork`.

Upgraded to v2.0 (ML feature engineering, entropy/crack-time engine, REST API +
web UI, and test suite) as a community contribution.
