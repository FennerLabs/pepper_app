# store a get_maccs_fingerprints function
import datamol as dm
from molfeat.trans.fp import FPVecTransformer


# main function
def get_maccs_fingerprints(smiles):
    transformer = FPVecTransformer(kind='maccs', dtype=float)
    maccs = transformer(smiles)
    return maccs

# test_maccs = get_maccs_fingerprints(['CCC', 'CCCC', 'C1=CC=C2C(=C1)C=CC3=CC=CC=C3N2C(=O)N'])
# print(test_maccs)


