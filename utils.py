import numpy as np
import joblib
import streamlit

from descriptors import get_maccs_fingerprints

@streamlit.cache_resource
def load_pepper_pipeline():
    """Load the entire pipeline"""
    return joblib.load('pepper_pipeline_model.pkl')

def perform_predictions_for_smiles(smiles):
    # Calculate the MACCS fingerprints for the input data
    X = get_maccs_fingerprints(smiles)

    # Use the pipeline to make predictions
    predicted_logB = load_pepper_pipeline().model_pipeline.predict(X)

    # Convert to percentages
    predictions = np.round((10*predicted_logB ) *100)
    return predictions