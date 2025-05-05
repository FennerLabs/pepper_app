import streamlit as st
import pandas as pd


def main():

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

        print('Start predictions')

        # Calculate using pepper-lab
        from predict_target_endpoint import predict
        predictions_df = predict(input_data)

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
