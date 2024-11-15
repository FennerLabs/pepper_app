import pandas as pd
import streamlit as st

st.set_page_config(
    page_title="Welcome!",
    page_icon="👋",
)

st.write("# Welcome to Pepper web app! 👋")


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



st.markdown(
    """
    Pepper-app is the web app version of a system developed by FennerLabs
    (https://github.com/FennerLabs) to Predict Predict Environmental Pollutant PERsistence.
    The main contributors of the PEPPER package  are:
    - [Jose Cordero ](https://www.eawag.ch/en/about-us/portrait/organisation/staff/profile/jose-cordero/show/)
    (Swiss Federal Institute of Aquatic Science & Technology) 
    - [Jasmin Hafner ](https://www.eawag.ch/en/about-us/portrait/organisation/staff/profile/jasmin-hafner/show/) 
    (Swiss Federal Institute of Aquatic Science & Technology &  University of Zurich)
    - [Albert Anguera](https://www.eawag.ch/en/about-us/portrait/organisation/staff/profile/albert-anguera-sempere/show/) 
    (Swiss Federal Institute of Aquatic Science & Technology)
    
    
    ### How to use the app? 
    - First, select which property are you most interest in. 
    - Then, you have two options Batch mode or Single Molecule mode.
    - When using the Batch mode please upload a csv file with a list of molecules for which you want to predict.
    - Ideally provide a csv file with at least one column of SMILES strings. (Please see the example file 📄)
    - You can provide any additional information in the csv file (e.g. your own ID for each molecule). 
    
    
    ### Want to learn more about our predictions? 
    - Check out our Data page 👈 to learn more about how were our models trained  
    
     ### Want to beyond the web app?
    - Check out [My own pepper-app](https://github.com/FennerLabs/pepper_app) if you want to install the app locally. 
"""
)


