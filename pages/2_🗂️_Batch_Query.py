import streamlit as st
import pandas as pd
import time

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
    endpoints = ['WWTP breakthrough', 'Soil half-life (fast)', 'Soil half-life (using enviPath rules)']
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
            time.sleep(1)

            if model_selected_from_box == 'WWTP breakthrough':
                from predict_target_endpoint import predict_WWTP_breakthrough
                predictions_df = predict_WWTP_breakthrough(input_data)
            elif model_selected_from_box == 'Soil half-life (fast)':
                # Calculate using pepper-lab
                from predict_target_endpoint import predict_soil_DT50
                predictions_df = predict_soil_DT50(input_data, model_type = 'fast')
            elif model_selected_from_box == 'Soil half-life (using enviPath rules)':
                # Calculate using pepper-lab
                from predict_target_endpoint import predict_soil_DT50
                predictions_df = predict_soil_DT50(input_data, model_type = 'enviPath')
            else:
                st.write("Please choose an option")

        st.success("Done!")

        # Show the predictions
        st.markdown(""" ### Predictions: """)
        st.dataframe(predictions_df)

        st.write("""
        📢⚠️ The frame below shows the predictions along chemical structures.
        We are working to give you the chemical structures as part of the file to be downloaded.  """)

        st.markdown(predictions_df.to_html(escape=False), unsafe_allow_html=True)


if __name__ == '__main__':
    main()
    print('app is running')
