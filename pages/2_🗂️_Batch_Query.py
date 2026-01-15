import streamlit as st
import pandas as pd
import time
from pepper_lab.predict import Predict

def main():

    # Streamlit app title
    st.title("PEPPER: an app to Predict Environmental Pollutant PERsistence ")

    st.markdown("""
    Currently we support the prediction of the following endpoints:
    - expected percentage breakthrough of micropollutants from
    conventional wastewater treatment, that is, the percentage that potentially escapes the plant 
    without being successfully removed. 
    - primary half-life (DT50) in soil, trained on regulatory data on OECD 307 soil biodegradation studies for pesticides.
    
    Visit section [Learn more](https://pepper-app.streamlit.app/Learn_more) 
    for further details.  
    """)

    # Dropdown menu for selecting a molecule
    endpoints = ['WWTP breakthrough', 'Soil half-life (Salz)']
    model_selected_from_box = st.selectbox('Choose endpoint to predict',
                                     placeholder='Choose an option',
                                     index=None,
                                     options=endpoints)

    # Upload CSV file
    uploaded_file = st.file_uploader("Upload a CSV file with chemical substance data", type="csv")

    @st.cache_data
    def convert_df(df):
        # IMPORTANT: Cache the conversion to prevent computation on every rerun
        return df.to_csv().encode("utf-8")
    example_csv = pd.read_csv('test_pepper_app.csv')
    csv = convert_df(example_csv)

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

        print('Start predictions')

        with st.spinner("Prediction is running...", show_time=True):
            time.sleep(3)

            if model_selected_from_box == 'WWTP breakthrough':
                from pepper_lab.predict import Predict
                pepper_predict = Predict(renku=True)
                my_model = Predict.load_pickle('pepper_object_wwtp_optimized_trained_model.pkl')
                model_data = my_model.data[['SMILES', 'logB']]
                model_data['Training Breakthrough (%)'] = round((10**model_data['logB'])*100,1)
                model_data.drop(columns='logB', inplace=True)
                # st.write("This is the model data", model_data)
                from predict_target_endpoint import predict_WWTP_breakthrough
                predictions_df = predict_WWTP_breakthrough(input_data)
                try:
                    merged_df = pd.merge(predictions_df, model_data, on='SMILES', how='left', suffixes=('', '_model'))
                    # st.write("Merged DataFrame:", merged_df)
                except Exception as e:
                    st.write("Error trying to fetch available experimental data:", e)
                if merged_df is not None:
                    predictions_df = merged_df

            elif model_selected_from_box == 'Soil half-life (Salz)':
                from predict_target_endpoint import predict_soil_DT50
                predictions_df = predict_soil_DT50(input_data, model_type = 'Salz')
            else:
                st.write("Please choose an option")

        st.success("Done!")

        # Show the predictions
        st.markdown(""" ### Predictions: """)
        config = {
            "Structure": st.column_config.ImageColumn(width="medium"),
        }
        st.dataframe(predictions_df, column_config=config, row_height=100)


if __name__ == '__main__':
    main()
    print('app is running')
