import streamlit as st
import pandas as pd
import requests
from mappings import list_cpu, list_gpu
import subprocess
import sys
import time
import socket
@st.cache_resource
def start_backend():
    # Check if port 8000 is already running
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        if s.connect_ex(("127.0.0.1", 8000)) != 0:
            subprocess.Popen(
                [sys.executable, "-m", "uvicorn", "main:app", "--host", "127.0.0.1", "--port", "8000"]
            )
            time.sleep(3)  # Wait for FastAPI to load the joblib model

start_backend()

# FastAPI Backend Endpoint
FASTAPI_URL = "http://127.0.0.1:8000/predict"

st.set_page_config(page_title="Laptop Price Predictor", layout="centered")
st.title("💻 Laptop Price Predictor")

# Put your full lists here
CPU_LIST = list_cpu

GPU_LIST = list_gpu

col1, col2 = st.columns(2)

with col1:
    brand = st.selectbox("Brand", ["ASUS", "Acer", "Apple", "DELL", "HP", "Lenovo", "MSI", "Samsung", "Unknown"])
    processor_brand = st.selectbox("Processor Brand", ["Intel", "AMD", "Apple", "Snapdragon", "MediaTek"])
    ram = st.select_slider("RAM (GB)", options=[4, 8, 16, 32, 64], value=16)
    ddr = st.radio("DDR", [4, 5], horizontal=True)

with col2:
    os_choice = st.selectbox("OS", ["windows", "macos", "linux", "other"])
    storage_type = st.selectbox("Storage Type", ["SSD", "HDD", "BOTH"])
    display_size = st.number_input("Display Size", value=15.6, step=0.1)
    dedicated_gpu = st.checkbox("Dedicated GPU Present")

# Multiple choice dropdowns for CPU and GPU
selected_cpus = st.multiselect("Select CPU Model(s)", options=CPU_LIST, default=[CPU_LIST[0]])
selected_gpus = st.multiselect("Select GPU Model(s)", options=GPU_LIST, default=[GPU_LIST[0]])

if st.button("Predict Prices", type="primary", use_container_width=True):
    cpus_to_run = selected_cpus if selected_cpus else [None]
    gpus_to_run = selected_gpus if selected_gpus else [None]

    results = []

    for cpu in cpus_to_run:
        for gpu in gpus_to_run:
            payload = {
                "RAM": ram,
                "processor_brand": processor_brand,
                "dedicated_gpu": 1 if dedicated_gpu else 0,
                "brand": brand,
                "cpu_model": cpu,
                "gpu_model": gpu,
                "display_size": display_size,
                "ddr": ddr,
                "storage_type": storage_type,
                "os": os_choice
            }

            try:
                # Calls FastAPI endpoint
                response = requests.post(FASTAPI_URL, json=payload)
                if response.status_code == 200:
                    price = response.json()["predicted_price"]
                    results.append({
                        "CPU Model": cpu or "Default / Average",
                        "GPU Model": gpu or "Default / Average",
                        "Predicted Price (₹)": f"₹{price:,.2f}"
                    })
                else:
                    st.error(f"FastAPI Error: {response.text}")
            except requests.exceptions.ConnectionError:
                st.error("FastAPI backend is not running! Start it with: `uvicorn main:app --reload`")
                st.stop()

    if results:
        st.subheader("Prediction Results")
        st.table(pd.DataFrame(results))