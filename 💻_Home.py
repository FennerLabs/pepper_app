import pandas as pd
import streamlit as st

st.set_page_config(
    page_title="Welcome!",
    page_icon="👋",
)

# Streamlit app title
st.title("PEPPER: an app to Predict Environmental Pollutant PERsistence ")

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
    Pepper-app is the web app version of ([PEPPER](https://github.com/FennerLabs/pepper)) a collection of models and methods 
    developed by [FennerLabs](https://github.com/FennerLabs) to Predict Environmental Pollutant PERsistence.
    If you want to learn more about Prof. Kathrin Fenner and her group
    follow this [link](https://www.eawag.ch/en/department/uchem/organisation/gruppenseite-fenner).
    
    
    The main developers of the PEPPER package and the Pepper-app are:
    - [Jose Cordero ](https://www.eawag.ch/en/about-us/portrait/organisation/staff/profile/jose-cordero/show/)
    (Swiss Federal Institute of Aquatic Science & Technology) 
    - [Jasmin Hafner ](https://www.eawag.ch/en/about-us/portrait/organisation/staff/profile/jasmin-hafner/show/) 
    (Swiss Federal Institute of Aquatic Science & Technology &  University of Zurich)
    - [Albert Anguera](https://www.eawag.ch/en/about-us/portrait/organisation/staff/profile/albert-anguera-sempere/show/) 
    (Swiss Federal Institute of Aquatic Science & Technology)
    
    
    
    ### How to use the app? 
    - First, choose if you want to make queries for a few molecules one by one 
    ([single molecule](https://pepper-app.streamlit.app/Single_Molecule)) or for several 
    molecules at once ([batch query](https://pepper-app.streamlit.app/Batch_Query)). 
    
    ##### Single molecule
    
    - If you want to make queries one by one please enter a valid SMILES string on the search bar. 
    You can get valid SMILES using ChemDraw or from databases like PubChem.
    - If you just want to check out the app, you can simply select a molecule from the droplist.
    
    ##### Batch Query
    
    - For many molecules use the batch mode by uploading a csv file with a list of molecules for which you want to predict.
    - The csv file must have a column of SMILES strings.
    We provide an example file 📄 available for download on the left panel 👈
    - You can then download the results as a csv file by clicking on the download button on 
    the upper right corner of the predictions dataframe.
    - We recommend including in the input file a column with additional information (e.g. your own ID for each molecule)
    to keep track of your predictions.
    That information will also appear in the predictions file.   
    
    
    ### Want to learn more about our predictions? 
    - Check out our [Learn more](https://pepper-app.streamlit.app/Learn_more) section for details about the models and the training data.  
    
     ### Want to go beyond the web app?
    - Check out [My own pepper-app](https://github.com/FennerLabs/pepper_app) if you want to install the app locally. 
"""
)


