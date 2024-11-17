import streamlit as st
import pandas as pd
from rdkit import Chem

from descriptors import get_maccs_fingerprints

import numpy as np

from rdkit.Chem import PandasTools


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
    "Diazinon": 'CCOP(=S)(OCC)OC1=NC(=NC(=C1)C)C(C)C',
    "4-nonylphenol": 'CCCCCCCCCC1=CC=C(C=C1)O'
}

# Title and instructions
st.write("# Enter the SMILES string for your molecule of interest")
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
        # Check wether the SMILES stirng is valid
        m = Chem.MolFromSmiles(molecule, sanitize=False)
        if m is None:
            st.warning('Invalid SMILES',icon='⛔')
        else:
            st.write(f"Your input: {molecule}")
            st.warning('SMILES string accepted: Breakthrough will be calculated', icon='✅')

            molecule = [molecule]

            # Calculate the MACCS fingerprints for the input data

            X = get_maccs_fingerprints(molecule)

            import joblib
            model_pipeline = joblib.load('pepper_pipeline_model.pkl')

            # Use the pipeline to make predictions
            predicted_logB = model_pipeline.predict(X)

            # Convert to percentages

            predictions = np.round((10 ** predicted_logB) * 100)

            # Show it as a dataframe
            predictions_df = pd.DataFrame()
            predictions_df['SMILES'] = molecule
            predictions_df['Breakthrough (%)'] = predictions

            # Show the predictions
            st.write("Predictions:", predictions_df)

            PandasTools.AddMoleculeColumnToFrame(predictions_df, smilesCol='SMILES')
            predictions_df.rename(columns={'ROMol': 'Structure'})
            predictions_df.drop(columns='SMILES', inplace=True)

            st.markdown(predictions_df.to_html(escape=False), unsafe_allow_html=True)

            # # Create a DataFrame to display predictions (placeholder for real logic)
            # predictions_df = pd.DataFrame()
            # predictions_df['SMILES'] = [molecule]  # Wrap in a list to avoid issues
            # predictions_df['Breakthrough'] = ['In construction']
            #
            # # Display the DataFrame
            # st.markdown(predictions_df.to_html(escape=False), unsafe_allow_html=True)



else:
    st.warning("Please enter a SMILES string")



