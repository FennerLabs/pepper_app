import pandas as pd
import streamlit as st
from rdkit.Chem import PandasTools

from utils import perform_predictions_for_smiles

def stuff():
    if not hasattr(st, 'already_started_server'):
        st.already_started_server = True

        st.write('''
            The first time this script executes it will run forever because it's
            running a Flask server.
    
            Just close this browser tab and open a new one to see your Streamlit
            app.
        ''')

        from flask import Flask

        app = Flask(__name__)

        @app.route('/foo')
        def serve_foo():
            return 'This page is served via Flask!'

        app.run(port=8128)

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

        predictions = perform_predictions_for_smiles(input_data.SMILES)

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
    stuff()
    main()
    print('app is running')
