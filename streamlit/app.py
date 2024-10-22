import pandas as pd
import streamlit as st
import requests
from rdkit.Chem import PandasTools

def main():

    # Streamlit app title
    st.title("PEPPER: an app to Predict Environmental Pollutant PERsistence ")

    # Upload CSV file
    uploaded_file = st.file_uploader("Upload a CSV file with chemical substance data", type="csv")

    if uploaded_file is not None:
        # Load the uploaded data
        input_data = pd.read_csv(uploaded_file)

        # Show the input data
        st.write("Uploaded data:", input_data)

        response = requests.request("get", "http://backend:8000/predict/", params={"smiles": ",".join(input_data.SMILES)})

        # Show it as a dataframe
        predictions_df = pd.DataFrame(input_data)
        predictions_df['Breakthrough (%)'] = response.json()
        print(response.json())
        print(predictions_df)

        # Show the predictions
        st.write("Predictions:", predictions_df)

        PandasTools.AddMoleculeColumnToFrame(predictions_df, smilesCol='SMILES')
        predictions_df.rename(columns={'ROMol': 'Structure'})
        predictions_df.drop(columns='SMILES', inplace=True)

        st.markdown(predictions_df.to_html(escape=False), unsafe_allow_html=True)


if __name__ == '__main__':
    main()
    print('app is running')
