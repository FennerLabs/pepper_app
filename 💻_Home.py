import pandas as pd
import streamlit as st

st.set_page_config(
    page_title="Welcome!",
    page_icon="👋",
)

# Streamlit app title
st.title("PEPPER - Predict Environmental Pollutant PERsistence ")

st.write("## Welcome to Pepper web app! 👋")


@st.cache_data
def convert_df(df):
    # IMPORTANT: Cache the conversion to prevent computation on every rerun
    return df.to_csv().encode("utf-8")


example_csv = pd.read_csv('test_pepper_app.csv')
csv = convert_df(example_csv)

# st.sidebar.success(" 📄 Download example file")
st.sidebar.download_button(
    label="Download example file",
    data=csv,
    file_name="pepper_example.csv",
    mime="text/csv",
)


st.markdown(
    """
    Pepper-app is the web app version of [PEPPER](https://github.com/FennerLabs/pepper), a collection of models and methods 
    developed by [FennerLabs](https://github.com/FennerLabs) to Predict Environmental Pollutant PERsistence.
    If you want to learn more about Prof. Kathrin Fenner and her group
    follow this [link](https://www.eawag.ch/en/department/uchem/organisation/gruppenseite-fenner).
    
    
    ### What is this app for?
    The pepper-app allows you to predict the following endpoints related to persistence of pollutants in the environment.
        - Breakthrough (%) for wastewater treatment plants (WWTP)
        - Primary soil biotransformation half-life (DT50)
    
    ### How to use the app? 
    1. Choose if you want to run predictions for single molecules
    ([Single molecule](https://pepper-app.streamlit.app/Single_Molecule)) or for several 
    molecules at once ([Batch query](https://pepper-app.streamlit.app/Batch_Query))
 
    ###### Single molecule
    
    - Enter a valid SMILES string in the search bar (you can obtain valid SMILES using ChemDraw or from databases like PubChem)
    - If you just want to check out the app, you can select a molecule from the dropdown list
    
    ###### Batch query
    
    - Upload a csv file with a list of molecules for which you want to predict.
    - The csv file must have a column of SMILES strings. We provide an example file 📄 available for download on the left panel 👈
    - We recommend including in the input file a column with additional information (e.g. your own ID for each molecule)
    to keep track of your predictions. That information will also appear in the predictions file.
    
    
    2. Choose the endpoint you want to predict
    3. Inspect results online or download results as .csv file (download button on 
    the upper right corner of the predictions dataframe)
       
    
    ### Want to learn more about our models? 
    - Check out our [Learn more](https://pepper-app.streamlit.app/Learn_more) section for details about the models and the training data.  
    
     ### Want to go beyond the web app?
    - Check out [My own pepper-app](https://github.com/FennerLabs/pepper_app) if you want to install the app locally. 
    
    ### How to cite us
    ###### WWTP breakthrough
    Cordero Solano, J. A., Hafner, J., McLachlan, M. S., Singer, H. & Fenner, K. 
    Predicting Micropollutant Removal in Wastewater Treatment Based on Molecular Structure: Benchmark Data and Models. 
    Environ. Sci. Technol. [doi:10.1021/acs.est.5c09314](https://doi.org/10.1021/acs.est.5c09314) (2025).
    
    ###### Soil half-lives
    Salz, M., Cordero Solano, J. A., Fenner, K. & Hafner, J. Confidently uncertain: 
    Probabilistic machine learning to predict soil biotransformation half-lives. 
    Preprint at [https://doi.org/10.26434/chemrxiv-2025-xmslf](https://doi.org/10.26434/chemrxiv-2025-xmslf) (2025).

    
    ### Main contributors to PEPPER and PEPPER-app
    - [Jose Cordero ](https://www.eawag.ch/en/about-us/portrait/organisation/staff/profile/jose-cordero/show/)
    (Swiss Federal Institute of Aquatic Science & Technology) 
    - [Jasmin Hafner ](https://www.eawag.ch/en/about-us/portrait/organisation/staff/profile/jasmin-hafner/show/) 
    (Swiss Federal Institute of Aquatic Science & Technology &  University of Zurich)
    - [Moritz Salz ](https://www.eawag.ch/en/about-us/portrait/organisation/staff/profile/moritz-salz/show/) 
    (Swiss Federal Institute of Aquatic Science & Technology)
    - [Albert Anguera](https://www.eawag.ch/en/about-us/portrait/organisation/staff/profile/albert-anguera-sempere/show/) 
    (Swiss Federal Institute of Aquatic Science & Technology)
    
    ### Acknowledgments 
    - Data to train our models was collected by members of Stockholm University including 
    [Zhe Li](https://www.su.se/english/profiles/zhli2569-1.189472), 
    [Yijing Li](https://www.su.se/english/profiles/yili6654-1.663685) 
    and [Malte Posselt](https://www.su.se/english/profiles/mapo9821-1.260962)
    - PEPPER & pepper-app were developed under a project funded by the Swiss Federal Office for the Environment (FOEN).

"""
)

# st.image('my_figure.png', use_column_width=False)
