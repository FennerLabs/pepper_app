from fastapi import FastAPI
from predict_target_endpoint import predict
app = FastAPI()

@app.get("/")
async def read_root():
    return {"message": "Welcome to the model API!"}

@app.get('/predict/')
async def serve_foo(smiles: str):
    return predict(smiles.split(','))
