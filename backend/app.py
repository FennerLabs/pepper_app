from fastapi import FastAPI
app = FastAPI()

@app.get("/")
async def read_root():
    return {"message": "Welcome to the model API!"}

@app.get('/predict/')
async def serve_foo(smiles: str):
    # Calculate using pepper-lab
    from predict_target_endpoint import predict
    predictions_df = predict(smiles)

    return predictions_df
