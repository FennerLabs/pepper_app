import streamlit as st
import pandas as pd
from rdkit.Chem import PandasTools


def main():
    # Load the entire pipeline
    # model_pipeline = joblib.load('pepper_pipeline_model.pkl')
    # model_regressor = joblib.load('pepper_wwtp_optimized_trained_regressor.pkl')

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
    #todo: take out
    uploaded_file = example_csv
    if uploaded_file is not None:
        # Load the uploaded data
        # input_data = pd.read_csv(uploaded_file)

        # todo: take out
        input_data = uploaded_file

        # Show the input data
        st.write("Uploaded data:", input_data)

        print('Start predictions')

        # Calculate the MACCS fingerprints for the input data
        from predict_target_endpoint import predict
        predictions_df = predict(input_data)

        # Show the predictions
        print(predictions_df)
        st.markdown(""" ### Predictions: """)
        st.dataframe(predictions_df)

        st.write("""
        📢⚠️ The frame below shows the chemical structures. We are working to give
        you the chemical structures as part of the file to be downloaded.  """)

        PandasTools.AddMoleculeColumnToFrame(predictions_df, smilesCol='SMILES')
        predictions_df.rename(columns={'ROMol': 'Structure'})
        predictions_df.drop(columns='SMILES', inplace=True)

        st.markdown(predictions_df.to_html(escape=False), unsafe_allow_html=True)


if __name__ == '__main__':
    main()
    print('app is running')
