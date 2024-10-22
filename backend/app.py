from fastapi import FastAPI
import joblib
import numpy as np

from descriptors import get_maccs_fingerprints

model_pipeline = joblib.load('pepper_pipeline_model.pkl')
app = FastAPI()

@app.get("/")
async def read_root():
    return {"message": "Welcome to the model API!"}

@app.get('/predict/')
async def serve_foo(smiles: str):
    smiles_list = smiles.split(',')

    # Calculate the MACCS fingerprints for the input data
    X = get_maccs_fingerprints(smiles_list)

    # Use the pipeline to make predictions
    predicted_logB = model_pipeline.predict(X)
    return np.round((10**predicted_logB ) *100).tolist()