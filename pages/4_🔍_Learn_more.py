import streamlit as st

st.set_page_config(
    page_title="Details",
    page_icon="👩🏽‍💻",
)

st.write(" # Thank you for wanting to know more about our models 👩🏽‍💻")


st.markdown(
    """
    
    ### How does the model works?
    
    - These are data driven models which predict your property of interest based on chemical structure
    - The SMILES strings provided are used to calculate the molecular descriptors best suited for that property. 
    - A pre-trained model takes those descriptors as input and returns predictions for each of your molecules. 
    - You may download the predictions as a csv file 
    - We encourage including an 'ID' column (in addition to the obligatory 'SMILES' column)
    to keep track of the molecules in your batch 
        

    ### Which data did you use for training? 
    - We use monitoring data from wastewater treatment plants


    ### May I apply these models to any molecule? 
    - 

"""
)
