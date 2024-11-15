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
    (https://github.com/FennerLabs) to Predict Predict Environmental Pollutant PERsistence 
    
    **👈 Select a demo from the sidebar** to some of the services available 
    
    ### Want to beyond the web app?
    - Check out [My own Pepper-app](https://github.com/FennerLabs/pepper_app) if you want to install the app locally. 
      This is possible thanks to [Albert Anguera](https://github.com/anguera5)
    - Ask a question in our [community
        forums](https://discuss.streamlit.io)
    ### See more complex demos
    - Use a neural net to [analyze the Udacity Self-driving Car Image
        Dataset](https://github.com/streamlit/demo-self-driving)
    - Explore a [New York City rideshare dataset](https://github.com/streamlit/demo-uber-nyc-pickups)
"""
)

