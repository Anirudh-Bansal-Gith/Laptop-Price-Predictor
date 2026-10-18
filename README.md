# 💻 Laptop Price Predictor

An end-to-end machine learning application that predicts the market price of a laptop in INR (₹) from its hardware specifications. Data is scraped from Flipkart, cleaned, used to train a regression pipeline, and served through a FastAPI backend with a Streamlit frontend.

![Python](https://img.shields.io/badge/Python-3.10%2B-blue)
![FastAPI](https://img.shields.io/badge/FastAPI-Backend-009688)
![Streamlit](https://img.shields.io/badge/Streamlit-Frontend-FF4B4B)
![scikit-learn](https://img.shields.io/badge/scikit--learn-ML-F7931E)
![License](https://img.shields.io/badge/License-MIT-green)

---

## 📖 Overview

Laptop prices vary widely with processor generation, GPU tier, RAM, storage and display. This project learns that relationship from ~1,900 real Flipkart listings and exposes it as a simple web app.

- **Input:** laptop specs (brand, CPU/GPU model, RAM, DDR, storage, OS, display size)
- **Output:** predicted price in ₹
- **Model:** scikit-learn `Pipeline` (OneHotEncoder + `GradientBoostingRegressor`)

---

## ✨ Features

- Scrapes and parses real listings from Flipkart
- Cleans and engineers features (`cpu_power`, `gpu_scores`, `is_ssd`, `is_hdd`)
- Trains and compares `RandomForestRegressor` vs `GradientBoostingRegressor`
- Input validation with **Pydantic** (`LaptopSpecs` schema)
- **FastAPI** REST backend with a `/predict` endpoint
- **Streamlit** frontend with an interactive spec builder
- Batch prediction across multiple CPU/GPU combinations in one click

---

## 🏗️ Architecture

```
┌────────────────┐    POST /predict    ┌──────────────────┐
│   Streamlit    │  ────────────────▶  │     FastAPI      │
│   frontend.py  │  ◀────────────────  │     main.py      │
└────────────────┘   {predicted_price} └────────┬─────────┘
                                                │
                                     ┌──────────▼──────────┐
                                     │  data_preparation.py │
                                     │  (validate + featurize)
                                     └──────────┬──────────┘
                                                │
                                     ┌──────────▼──────────┐
                                     │ laptop_pipe.joblib   │
                                     │ (sklearn Pipeline)   │
                                     └──────────────────────┘
```

---

## 📂 Project Structure

```
Laptop-Price-Predictor/
├── main.py                 # FastAPI app, /predict endpoint
├── frontend.py             # Streamlit UI
├── schema.py               # Pydantic LaptopSpecs validation model
├── data_preparation.py     # Feature engineering for inference
├── mappings.py             # CPU/GPU power score lookup tables
├── model.ipynb             # Training + model selection notebook
├── flipkart.ipynb          # Scraper for raw laptop data
├── exec.ipynb              # Early schema prototyping
├── Dirty.csv               # Raw scraped dataset
├── clean_data.csv          # Cleaned, feature-engineered dataset
├── laptop_pipe.joblib      # Serialized trained pipeline
├── requirements.txt        # Python dependencies
├── LICENSE
└── README.md
```

---

## ⚙️ Installation

Requires Python 3.10+.

```bash
git clone git@github.com:Anirudh-Bansal-Gith/Laptop-Price-Predictor.git
cd Laptop-Price-Predictor

python -m venv .venv
source .venv/bin/activate      # Windows: .venv\Scripts\activate

pip install -r requirements.txt
```

---

## 🚀 Usage

### 1. Start the backend

```bash
uvicorn main:app --reload
```

Serves at `http://127.0.0.1:8000`.

### 2. Start the frontend

In a second terminal:

```bash
streamlit run frontend.py
```

Opens at `http://localhost:8501`. Configure the laptop specs, select one or more CPU/GPU models, and click **Predict Prices**.

---

## 🔌 API Reference

### `POST /predict`

**Request body**

```json
{
  "RAM": 16,
  "processor_brand": "Intel",
  "dedicated_gpu": 1,
  "brand": "ASUS",
  "cpu_model": "Intel Core i7 Processor (13th Gen)",
  "gpu_model": "NVIDIA GeForce RTX 4060",
  "display_size": 15.6,
  "ddr": 5,
  "storage_type": "SSD",
  "os": "windows"
}
```

**Response**

```json
{
  "predicted_price": 94500.00
}
```

| Field            | Type   | Required | Notes                                   |
| ---------------- | ------ | -------- | --------------------------------------- |
| `RAM`            | int    | ✅       | RAM in GB                               |
| `processor_brand`| str    | ✅       | e.g. `Intel`, `AMD`, `Apple`            |
| `dedicated_gpu`  | int    | ✅       | `1` if dedicated GPU, else `0`          |
| `brand`          | str    | ❌       | Default `Unknown`                       |
| `cpu_model`      | str    | ❌       | Key from `mappings.cpu_scores`          |
| `gpu_model`      | str    | ❌       | Key from `mappings.gpu_scores`          |
| `display_size`   | float  | ❌       | Default `15.6`                          |
| `ddr`            | int    | ❌       | Default `4`                             |
| `storage_type`   | str    | ❌       | `SSD` \| `HDD` \| `BOTH`                |
| `os`             | str    | ❌       | `windows` \| `macos` \| `linux` \| `other` |

Invalid input raises `HTTP 400` with a validation message.

---

## 🧠 Model

Both candidate regressors were trained on an 80/20 split with one-hot encoding for categorical features.

| Model                       | RMSE (₹)    | R² Score |
| --------------------------- | ----------- | -------- |
| RandomForestRegressor       | 12,570.86   | 0.9315   |
| **GradientBoostingRegressor** | **9,367.49** | **0.9620** |

**GradientBoostingRegressor** was selected as the final model and persisted to `laptop_pipe.joblib`.

Feature set: `os`, `display_size`, `brand`, `RAM`, `ddr`, `is_ssd`, `is_hdd`, `processor_brand`, `cpu_power`, `dedicated_gpu`, `gpu_scores`.

---

## 🛠️ Tech Stack

- **Data collection:** `requests`, `BeautifulSoup`
- **Data processing:** `pandas`, `numpy`
- **ML:** `scikit-learn` (Pipeline, ColumnTransformer, OneHotEncoder, GradientBoosting)
- **Validation:** `pydantic`
- **Backend:** `FastAPI`, `uvicorn`
- **Frontend:** `Streamlit`
- **Serialization:** `joblib`

---

## 📄 License

Released under the [MIT License](LICENSE).

Copyright (c) 2026 Anirudh Bansal
