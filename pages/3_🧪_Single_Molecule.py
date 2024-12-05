import streamlit as st
import pandas as pd
from rdkit import Chem

from descriptors import get_maccs_fingerprints

import numpy as np

from rdkit.Chem import PandasTools


def tree_std_to_confidence(tree_std_dev):
    min_tree_std = 0.29
    max_tree_std = 0.91
    if tree_std_dev < min_tree_std:
        confidence = 1
    elif tree_std_dev > max_tree_std:
        confidence = 0
    else:
        confidence = (-1/(max_tree_std-min_tree_std))*tree_std_dev + 1.468

    return confidence


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
Currently we support the prediction of the expected percentage breakthrough of micropollutants from
conventional wastewater treatment, that is, the percentage that potentially escapes the plant 
without being successfully removed. Visit section [Learn more](https://pepper-app.streamlit.app/Learn_more) 
for further details.  
""")
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

            molecule = [molecule]

            # Calculate the MACCS fingerprints for the input data

            X = get_maccs_fingerprints(molecule)

            import joblib
            model_pipeline = joblib.load('pepper_pipeline_model.pkl')

            print('Preprocess data for predicting')
            # Manually apply the transformations in the pipeline to X_test, except the last estimator
            # X_test_transformed = model_pipeline.named_steps['scaler'].transform(X)
            X_test_transformed = model_pipeline.named_steps['variance_selector'].transform(X)

            print('Start predictions')
            # Get individual tree predictions for each instance in the test set
            individual_tree_predictions = np.array([
                [tree.predict(X_test_transformed) for tree in model_pipeline.named_steps['regressor'].estimators_]
            ]).squeeze()  # Shape: (n_estimators, n_test_samples)

            # Calculate mean prediction and standard deviation across tree predictions for each test sample
            y_pred_means = individual_tree_predictions.mean(axis=0)

            print('Get AD metrics')
            prediction_std_dev = individual_tree_predictions.std(axis=0)
            confidence_std_dev = tree_std_to_confidence(prediction_std_dev)

            # Use the pipeline to make predictions
            predicted_logB = model_pipeline.predict(X)

            # Convert to percentages
            predictions = np.round((10 ** predicted_logB) * 100)

            # Show it as a dataframe
            predictions_df = pd.DataFrame()
            predictions_df['SMILES'] = molecule


            # Show the predictions
            # st.write('Predictions:')
            # st.dataframe(predictions_df)

            PandasTools.AddMoleculeColumnToFrame(predictions_df, smilesCol='SMILES')
            predictions_df.rename(columns={'ROMol': 'Structure'}, inplace=True)
            predictions_df.drop(columns='SMILES', inplace=True)
            predictions_df['Breakthrough (%)'] = predictions
            predictions_df['Confidence (0-1)'] = np.round(confidence_std_dev, decimals=1)

            st.markdown(predictions_df.to_html(escape=False, index=False), unsafe_allow_html=True)


else:
    st.warning("Please enter a SMILES string")



