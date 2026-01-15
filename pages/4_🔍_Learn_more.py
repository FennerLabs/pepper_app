import streamlit as st

st.set_page_config(
    page_title="Details",
    page_icon="👩🏽‍💻",
)

st.write(" # Want to know more about our models? 👩🏽‍💻")


st.markdown(
    """
    ### What can I predict with these models? 
    - Our vision is to provide models for diverse endpoints related to persistence of
    micropollutants in the environment.
    - Currently, we provide model predictions for WWTP breakthrough and soil biotransformation

    - Breakthrough from conventional wastewater treatment plants is defined as
    
    > $$Breakthrough (\%) = \\frac{Cn_{effluent}}{Cn_{influent}}  \\times 100 $$
    
    which represents the percentage of substance that potentially escapes the plant untreated. 
    
    - Primary soil biotransformation half-lives are predicted in log(days) and converted to days by the app.
    
    ### How does the model work?
    
    - Our data-driven models predict persistence endpoints of interest based on chemical structure alone.
    - SMILES strings are used to calculate molecular descriptors that are best suited for a given endpoint. 
    - The app takes SMILES as input, calculates relevant descriptors, predicts endpoints using a pre-trained model, 
    and returns predictions for each input molecule. 
    - You may download the predictions as a csv file. 
    - We encourage including an 'ID' column (in addition to the obligatory 'SMILES' column)
    to keep track of the molecules in your batch. 
        

    ### Which data did you use for training? 
    ###### WWTP breakthrough
    - We use monitoring data from conventional wastewater treatment plants.
    - All these plants have activated sludge and do not employ advanced treatment. 
    - In the future we want to adjust predictions to different treatment scenarios. 
    - However, at this time we focus on conventional treatment with an understanding that this technology reflects
    the most common treatment strategy worldwide.
    - Training data is available on [GitHub](https://github.com/FennerLabs/pepper/tree/main/data/wwtp-data).
    
    ###### Soil half-lives
    - The soil half-life data consists of reported biotranformation half-lives reported in regulatory studies (OECD 307) 
    for pesticides and pesticide transformation.
    - The original EAWAG-SOIL data package is available on [enviPath](https://envipath.org/package/5882df9c-dae1-4d80-a40e-db4724271456)
    - For each substance in the training data, we applied Bayesian inference to obtain a representative half-life
     distribution from its reported half-lives. The mean log-transformed half-life and its uncertainty were used to t
     rain a probabilistic half-life model.
    - The training data is available on [GitHub](https://github.com/FennerLabs/pepper/tree/main/data/soil) and [Zenodo](https://doi.org/10.5281/zenodo.18245745) (DOI: 10.5281/zenodo.18245745)


    ### May I apply these models to any molecule? 
    - Instead of an in- or out-of-domain classification we provide a metric of confidence.
    - This metric of confidence depends on the algorithm used: 
    ###### WWTP breakthrough
    - The current implementation uses a Random Forest regressor so the confidence is a function of 
    the agreement between the predictions of individual trees. 
    - Avoid using predictions with confidence 0.
    ###### Soil half-lives
    - The predicted uncertainty represents the standard deviation of the half-life distribution estimated by a 
    Gaussian Process Regressor.
    - The standard deviation is calibrated (for more details, see [Salz et al., 2025](https://doi.org/10.26434/chemrxiv-2025-xmslf)).
    - Confidence levels thresholds are defined to categorize predictions into "good" (stdev <= 0.5), "acceptable" (stdev <= 0.7), and "low" (stdev > 0.7).
    
    
    ##### 📢⚠️ This page is under construction:
    ###### We will have a major deployment with more detailed documentation once our work is published.  

"""
)
