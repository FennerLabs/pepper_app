import streamlit as st
import joblib
import pandas as pd
import numpy as np
# from rdkit.Chem import PandasTools

from descriptors import get_maccs_fingerprints

# Load the entire pipeline
model_pipeline = joblib.load('pepper_pipeline_model.pkl')

# Streamlit app title
st.title("PEPPER: an App to Predict Environmental Persistence ")

# Upload CSV file
uploaded_file = st.file_uploader("Upload a CSV file with chemical substance data", type="csv")

if uploaded_file is not None:
    # Load the uploaded data
    input_data = pd.read_csv(uploaded_file)

    # Show the input data
    st.write("Uploaded data:", input_data)

    # Calculate the MACCS fingerprints for the input data
    X = get_maccs_fingerprints(input_data.SMILES)

    # Use the pipeline to make predictions
    predicted_logB = model_pipeline.predict(X)

    # Convert to percentages
    predictions = np.round((10**predicted_logB)*100)

    # Show it as a dataframe
    predictions_df = pd.DataFrame(input_data)
    predictions_df['Breakthrough (%)'] = predictions

    # Add chemical structures
    # PandasTools.AddMoleculeColumnToFrame(predictions_df, smilesCol='SMILES')

    # Show the predictions
    st.write("Predictions:", predictions_df)

