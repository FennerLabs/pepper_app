import streamlit as st

st.set_page_config(
    page_title="Welcome!",
    page_icon="👋",
)

st.write("# Welcome to Pepper web app! 👋")

st.sidebar.success("Select a demo above.")

st.markdown(
    """
    Pepper-app is the web app version of a system developed by FennerLabs
    (https://github.com/FennerLabs) to Predict Predict Environmental Pollutant PERsistence.
    The main contributors of the PEPPER package  are:
    Jose Cordero (Swiss Federal Institute of Aquatic Science & Technology) 
    Jasmin Hafner (Swiss Federal Institute of Aquatic Science & Technology &  University of Zurich)
    Albert Anguera (Swiss Federal Institute of Aquatic Science & Technology)
    
    **👈 Select a demo from the sidebar** to some of the services available 
    
    ### How to use the app? 
    - First, select which property are you most interest in. 
    - Then, you have two options Batch mode or Single Molecule mode.
    - When using the Batch mode please upload a csv file with a list of molecules for which you want to predict.
    - Ideally provide a csv file with at least one column of SMILES strings. (Please see the example file 📄)
    - You can provide any additional information in the csv file (e.g. your own ID for each molecule). 
    
    
    ### Want to learn more about our predictions? 
    - Check out our Data page 👈 to learn more about how were our models trained  
    
     ### Want to beyond the web app?
    - Check out [My own Pepper-app](https://github.com/FennerLabs/pepper_app) if you want to install the app locally. 
      This is possible thanks to [Albert Anguera](https://github.com/anguera5)
    - Ask a question in our [community
        forums](https://discuss.streamlit.io)
"""
)
