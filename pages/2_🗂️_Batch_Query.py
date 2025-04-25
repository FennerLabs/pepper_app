import joblib
import pandas as pd
import streamlit as st
import numpy as np

from prepare_input import get_maccs_fingerprints
# from rdkit.Chem import PandasTools


reduced_features_names = ['struct-19', 'struct-37', 'struct-38', 'struct-49', 'struct-53',
       'struct-54', 'struct-62', 'struct-66', 'struct-72', 'struct-74',
       'struct-77', 'struct-78', 'struct-79', 'struct-80', 'struct-82',
       'struct-83', 'struct-84', 'struct-86', 'struct-89', 'struct-90',
       'struct-91', 'struct-92', 'struct-93', 'struct-95', 'struct-96',
       'struct-97', 'struct-98', 'struct-99', 'struct-100', 'struct-101',
       'struct-104', 'struct-105', 'struct-106', 'struct-108', 'struct-109',
       'struct-111', 'struct-112', 'struct-113', 'struct-114', 'struct-115',
       'struct-116', 'struct-117', 'struct-118', 'struct-120', 'struct-123',
       'struct-125', 'struct-126', 'struct-127', 'struct-128', 'struct-129',
       'struct-131', 'struct-132', 'struct-133', 'struct-134', 'struct-135',
       'struct-136', 'struct-137', 'struct-138', 'struct-139', 'struct-140',
       'struct-141', 'struct-142', 'struct-144', 'struct-145', 'struct-146',
       'struct-149', 'struct-150', 'struct-151', 'struct-152', 'struct-153',
       'struct-154', 'struct-155', 'struct-156', 'struct-157', 'struct-158',
       'struct-159', 'struct-160', 'struct-162', 'struct-163', 'struct-164',
       'struct-165']


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
    # model_pipeline = joblib.load('pepper_pipeline_model.pkl')
    model_regressor = joblib.load('pepper_app/pepper_wwtp_optimized_trained_regressor.pkl')

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
        X = get_maccs_fingerprints(input_data)
        st.write("Fingerprints_sheet:", X)

        print('Preprocess data for predicting')
        # Manually apply the transformations in the pipeline to X_test, except the last estimator
        X_test_selected = X[X.columns.isin(reduced_features_names)]

        print('Start predictions')
        # Get individual tree predictions for each instance in the test set
        individual_tree_predictions = np.array([
            [tree.predict(X_test_selected) for tree in model_regressor.estimators_]
        ]).squeeze()  # Shape: (n_estimators, n_test_samples)

        # Calculate mean prediction and standard deviation across tree predictions for each test sample
        y_pred_means = individual_tree_predictions.mean(axis=0)

        print('Get AD metrics')
        prediction_std_dev = individual_tree_predictions.std(axis=0)
        confidence_std_dev = tree_std_to_confidence(prediction_std_dev)

        # Use the pipeline to make predictions
        # predicted_logB = model_pipeline.predict(X)
        predicted_logB = y_pred_means

        # Convert to percentages
        predictions = np.round((10**predicted_logB)*100)

        # Show it as a dataframe
        predictions_df = pd.DataFrame(input_data)
        predictions_df['Breakthrough (%)'] = predictions
        predictions_df['Confidence (0-1)'] = np.round(confidence_std_dev, decimals=1)

        # Show the predictions
        st.markdown(""" ### Predictions: """)
        st.dataframe(predictions_df)

        # st.write("""
        # 📢⚠️ The frame below shows the chemical structures. We are working to give you the chemical structures as part of the file to be downloaded.  """)
        #
        # PandasTools.AddMoleculeColumnToFrame(predictions_df, smilesCol='SMILES')
        # predictions_df.rename(columns={'ROMol': 'Structure'})
        # predictions_df.drop(columns='SMILES', inplace=True)
        #
        # st.markdown(predictions_df.to_html(escape=False), unsafe_allow_html=True)


if __name__ == '__main__':
    main()
    print('app is running')
