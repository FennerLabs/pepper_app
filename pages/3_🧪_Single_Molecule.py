import streamlit as st
from rdkit import Chem


st.set_page_config(
    page_title="👋 Single Molecule Predictions",
    page_icon="👋",
)

molecule = ''

# Define figure names
figure_names = {
    "None": '',
    "Paracetamol": 'O=C(C)NC1=CC=C(O)C=C1',
    "Ibuprofen": 'CC(C)CC1=CC=C(C=C1)C(C)C(=O)O',
    "Sulfamethoxazole": 'CC1=CC(=NO1)NS(=O)(=O)C2=CC=C(C=C2)N',
    "Fluoexetine": 'CNCCC(C1=CC=CC=C1)OC2=CC=C(C=C2)C(F)(F)F',
    "Heptachlor": 'C1=CC(C2C1C3(C(=C(C2(C3(Cl)Cl)Cl)Cl)Cl)Cl)Cl',
    "Bromoxynil": 'C1=C(C=C(C(=C1Br)O)Br)C#N',
    "Diazinon": 'CCOP(=S)(OCC)OC1=NC(=NC(=C1)C)C(C)C',
    "4-nonylphenol": 'CCCCCCCCCC1=CC=C(C=C1)O'
}

# Title and instructions
st.write("# Enter the SMILES string for your molecule of interest")
st.markdown("""
Currently we support the prediction of the following endpoints:
- expected percentage breakthrough of micropollutants from
conventional wastewater treatment, that is, the percentage that potentially escapes the plant 
without being successfully removed. 
- primary half-life (DT50) in soil, trained on regulatory data on OECD 307 soil biodegradation studies for pesticides.

Visit section [Learn more](https://pepper-app.streamlit.app/Learn_more) 
for further details.  
""")

st.write('### Select a model')
# Dropdown menu for selecting a molecule
endpoints = ['WWTP breakthrough', 'Soil half-life (fast)', 'Soil half-life (using enviPath rules)']
model_selected_from_box = st.selectbox('Choose endpoint to predict',
                                       placeholder='Choose an option',
                                       index=None,
                                       options=endpoints)


st.write("#### If you just want to check the app you may select example smiles from the box below")

# Dropdown menu for selecting a molecule
selected_from_box = st.selectbox('Choose SMILES from the list:',
                                 placeholder='Choose an option',
                                 index=None,
                                 options=figure_names.keys())

st.write(f"You selected option {selected_from_box} with SMILES {figure_names.get(selected_from_box)}")

# Update `molecule` when a name is selected
if selected_from_box:
    molecule = figure_names.get(selected_from_box)

# SMILES string input
st.write("#### If you have a molecule in mind you can predict using its SMILES string")
smiles_added_manually = st.text_input("Enter SMILES string here:", '')
search_molecule = st.button("OK", key='search_molecule', type='primary')
if search_molecule:
    molecule = smiles_added_manually

reset = st.button("Reset", key='reset')

if search_molecule or selected_from_box:
    if molecule != '':
        # Check whether the SMILES string is valid
        m = Chem.MolFromSmiles(molecule, sanitize=True)
        if m is None:
            st.warning('Invalid SMILES', icon='⛔')
        else:
            st.write(f"Your input: {molecule}")
            st.warning('SMILES string accepted: Breakthrough will be calculated', icon='✅')

            # molecule = pd.DataFrame({'SMILES': [molecule]})
            # Calculate using pepper-lab
            with st.spinner("Prediction is running...", show_time=True):

                if model_selected_from_box == 'WWTP breakthrough':
                    from predict_target_endpoint import predict_WWTP_breakthrough
                    predictions_df = predict_WWTP_breakthrough(molecule, input_smiles_type='smi')

                elif model_selected_from_box == 'Soil half-life (fast)':
                    # Calculate using pepper-lab
                    from predict_target_endpoint import predict_soil_DT50
                    predictions_df = predict_soil_DT50(molecule, input_smiles_type='smi', model_type='fast')
                elif model_selected_from_box == 'Soil half-life (using enviPath rules)':
                    # Calculate using pepper-lab
                    from predict_target_endpoint import predict_soil_DT50

                    predictions_df = predict_soil_DT50(molecule, input_smiles_type='smi', model_type='enviPath')
                else:
                    st.write("Please choose an option")

            st.subheader('Done!')
            st.markdown(predictions_df.to_html(escape=False, index=False), unsafe_allow_html=True)


else:
    st.warning("Please enter a SMILES string")
