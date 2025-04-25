# store a get_maccs_fingerprints function

def get_maccs_fingerprints(input_smiles):
    from pepper_lab.pepper import Pepper
    from pepper_lab.descriptors import Descriptors

    # calculate descriptors
    pep = Pepper(renku=True)
    descriptors = Descriptors(pep)
    descriptors.model_data = input_smiles
    descriptors.load_descriptors(from_csv=False, MACCS=True)
    descriptors.maccs.drop(columns=descriptors.smiles_name, inplace=True)
    return descriptors.maccs
