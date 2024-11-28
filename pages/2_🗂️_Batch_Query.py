import joblib
import pandas as pd
import streamlit as st
import numpy as np

from descriptors import get_maccs_fingerprints
from rdkit.Chem import PandasTools


def tree_std_to_confidence(tree_std_array):
    confidence_list = []
    for tree_std in tree_std_array:
        min_tree_std = 0.29
        max_tree_std = 0.91
        if tree_std < min_tree_std:
            confidence = 1
        elif tree_std > max_tree_std:
            confidence = 0
        else:
            confidence = (-1/(max_tree_std-min_tree_std))*tree_std + 1.468
        confidence_list.append(confidence)
    return confidence_list


def main():
    # Load the entire pipeline
    model_pipeline = joblib.load('pepper_pipeline_model.pkl')

    # Streamlit app title
    st.title("PEPPER: an app to Predict Environmental Pollutant PERsistence ")

    st.markdown("""
    Currently we support the prediction of the expected percentage breakthrough of micropollutants from
    conventional wastewater treatment, that is, the percentage that potentially escapes the plant 
    without being successfully removed. Visit section [Learn more](https://pepper-app.streamlit.app/Learn_more) 
    for further details.  
    """)

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

        print('Preprocess data for predicting')
        # Manually apply the transformations in the pipeline to X_test, except the last estimator
        # X_test_transformed = model_pipeline.named_steps['scaler'].transform(X)
        X_test_transformed = model_pipeline.named_steps['variance_selector'].transform(X)

        print('Start predictions')
        # Get individual tree predictions for each instance in the test set
        individual_tree_predictions = np.array([
            [tree.predict(X_test_transformed) for tree in model_pipeline.named_steps['regressor'].estimators_]
        ]).squeeze()  # Shape: (n_estimators, n_test_samples)

        # Calculate mean prediction and standard deviation across tree predictions for each test sample
        y_pred_means = individual_tree_predictions.mean(axis=0)

        print('Get AD metrics')
        prediction_std_dev = individual_tree_predictions.std(axis=0)
        confidence_std_dev = tree_std_to_confidence(prediction_std_dev)

        # Use the pipeline to make predictions
        predicted_logB = model_pipeline.predict(X)

        # Convert to percentages
        predictions = np.round((10**predicted_logB)*100)

        # Show it as a dataframe
        predictions_df = pd.DataFrame(input_data)
        predictions_df['Breakthrough (%)'] = predictions
        predictions_df['Confidence (0-1)'] = np.round(confidence_std_dev, decimals=1)

        # Show the predictions
        st.markdown(""" ### Predictions: """)
        st.dataframe(predictions_df)

        st.write("""
        📢⚠️ The frame below shows the chemical structures. We are working to give you the chemical structures as part of the file to be downloaded.  """)

        PandasTools.AddMoleculeColumnToFrame(predictions_df, smilesCol='SMILES')
        predictions_df.rename(columns={'ROMol': 'Structure'})
        predictions_df.drop(columns='SMILES', inplace=True)

        st.markdown(predictions_df.to_html(escape=False), unsafe_allow_html=True)


if __name__ == '__main__':
    main()
    print('app is running')
