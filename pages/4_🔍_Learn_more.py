import streamlit as st

st.set_page_config(
    page_title="Details",
    page_icon="👩🏽‍💻",
)

st.write(" # Thank you for wanting to know more about our models 👩🏽‍💻")


st.markdown(
    """
    ### What can I predict with these models? 
    - Our vision is to provide models for many diverse endpoints related to persistence of
    micropollutants in the environment.
    - Currently we support breakthrough from conventional wastewater treatment plants, which is defined as follows:
    
    
    > $$Breakthrough (\%) = \\frac{Cn_{effluent}}{Cn_{influent}}  \\times 100 $$
    
    Which represents the percentage of substance that potentially escapes the plant untreated. 
    
    ### How does the model work?
    
    - These are data driven models which predict your property of interest based on chemical structure.
    - The SMILES strings provided are used to calculate the molecular descriptors best suited for that property. 
    - A pre-trained model takes those descriptors as input and returns predictions for each of your molecules. 
    - You may download the predictions as a csv file. 
    - We encourage including an 'ID' column (in addition to the obligatory 'SMILES' column)
    to keep track of the molecules in your batch. 
        

    ### Which data did you use for training? 
    - We use monitoring data from coventional wastewater treatment plants.
    - All these plants have activated sludge and do not employ advanced treatment. 
    - In the future we want to adjust predictions to different treatment scenarios. 
    - However, at this time we focus on conventional treatment with an understanding that this technology reflects
    the most common treatment strategy worldwide.


    ### May I apply these models to any molecule? 
    - Instead of a in- or out-of-domain classification we provide a metric of confidence.
    - This metric of confidence depends on the algorithm used. 
    - The current implementation uses a Random Forest regressor so the confidence is a function of 
    the agreement between the predictions of individual trees. 
    - Avoid using predictions with confidence 0.
    
    
    ##### 📢⚠️ This page is under construction:
    ###### We will have a major deployment with more detailed documentation once our work is published.  

"""
)
