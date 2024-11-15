import pandas as pd
import streamlit as st

st.set_page_config(
    page_title="👋 Single Molecule Predictions",
    page_icon="👋",
)

st.write("# Enter the SMILES string for your molecule of interest")

st.write("#### You can get SMILES using ChemDraw, or from databases such as PubChem")

st.markdown('# ⌕', unsafe_allow_html=True)
molecule = st.text_input("", "Search...")
button_clicked = st.button("OK")


def main():
    # # Calculate the MACCS fingerprints for the input data
    # X = get_maccs_fingerprints(molecule)
    #
    # # Use the pipeline to make predictions
    # predicted_logB = model_pipeline.predict(X)
    # return np.round((10 ** predicted_logB) * 100).tolist()
    if button_clicked:
        predictions_df = pd.DataFrame()
        predictions_df['SMILES'] = molecule
        predictions_df['Breakthrough'] = 'In construction'

        return st.markdown(predictions_df.to_html(escape=False), unsafe_allow_html=True)

    else:
        return st.warning("Please enter a SMILES string")


if __name__ == '__main__':
    main()
    print('Predict for single molecule')