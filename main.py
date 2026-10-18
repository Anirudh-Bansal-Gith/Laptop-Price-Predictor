from fastapi import FastAPI, HTTPException
import joblib
from schema import LaptopSpecs
from data_preparation import prepare_data

app = FastAPI()

pipe = joblib.load('laptop_pipe.joblib')

def run_data(data: dict, pipe) -> float:
    try:
        prepared_df = prepare_data(data, pipe)
    except Exception as e:
        return e
    try:
        prediction = pipe.predict(prepared_df)
    except Exception as e:
        return e
    
    return float(prediction[0])

@app.post("/predict")
def predict(specs: LaptopSpecs):
    res = run_data(specs.model_dump(), pipe)
    if isinstance(res, Exception):
        raise HTTPException(status_code=400, detail=str(res))
    return {"predicted_price": round(res, 2)}