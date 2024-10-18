from molfeat.trans.fp import FPVecTransformer

def get_maccs_fingerprints(smiles):
    transformer = FPVecTransformer(kind='maccs', dtype=float)
    maccs = transformer(smiles)
    return maccs
