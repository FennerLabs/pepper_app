import joblib
import pandas as pd
import streamlit as st
import numpy as np

from descriptors import get_maccs_fingerprints
from rdkit.Chem import PandasTools


def main():
    # Load the entire pipeline
    model_pipeline = joblib.load('pepper_pipeline_model.pkl')

    # Streamlit app title
    st.title("PEPPER: an app to Predict Environmental Pollutant PERsistence ")

    # Upload CSV file
    uploaded_file = st.file_uploader("Upload a CSV file with chemical substance data", type="csv")

    @st.cache_data
    def convert_df(df):
        # IMPORTANT: Cache the conversion to prevent computation on every rerun
        return df.to_csv().encode("utf-8")

    example_csv = pd.read_csv('test_pepper_app.csv')
    csv = convert_df(example_csv)

    st.sidebar.success(" 📄 Download example file")
    st.sidebar.download_button(
        label="Download example file",
        data=csv,
        file_name="pepper_example.csv",
        mime="text/csv",
    )


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

        # Show the predictions
        st.write("Predictions:", predictions_df)

        PandasTools.AddMoleculeColumnToFrame(predictions_df, smilesCol='SMILES')
        predictions_df.rename(columns={'ROMol': 'Structure'})
        predictions_df.drop(columns='SMILES', inplace=True)

        st.markdown(predictions_df.to_html(escape=False), unsafe_allow_html=True)


if __name__ == '__main__':
    main()
    print('app is running')
