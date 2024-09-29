# store a get_maccs_fingerprints function
from molfeat.trans.fp import FPVecTransformer


# main function
def get_maccs_fingerprints(smiles):
    transformer = FPVecTransformer(kind='maccs', dtype=float)
    maccs = transformer(smiles)
    return maccs