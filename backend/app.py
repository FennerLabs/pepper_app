from fastapi import FastAPI
# import joblib
# import numpy as np
# from descriptors import get_maccs_fingerprints
# model_pipeline = joblib.load('pepper_pipeline_model.pkl')
app = FastAPI()

@app.get("/")
async def read_root():
    return {"message": "Welcome to the model API!"}

@app.get('/predict/')
async def serve_foo(smiles: str):
    # Calculate using pepper-lab
    from streamlit.predict_target_endpoint import predict
    predictions_df = predict(smiles)

    return predictions_df
