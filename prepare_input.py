# store a get_maccs_fingerprints function
import pandas as pd

reduced_features_names = ['struct-19', 'struct-37', 'struct-38', 'struct-49', 'struct-53',
       'struct-54', 'struct-62', 'struct-66', 'struct-72', 'struct-74',
       'struct-77', 'struct-78', 'struct-79', 'struct-80', 'struct-82',
       'struct-83', 'struct-84', 'struct-86', 'struct-89', 'struct-90',
       'struct-91', 'struct-92', 'struct-93', 'struct-95', 'struct-96',
       'struct-97', 'struct-98', 'struct-99', 'struct-100', 'struct-101',
       'struct-104', 'struct-105', 'struct-106', 'struct-108', 'struct-109',
       'struct-111', 'struct-112', 'struct-113', 'struct-114', 'struct-115',
       'struct-116', 'struct-117', 'struct-118', 'struct-120', 'struct-123',
       'struct-125', 'struct-126', 'struct-127', 'struct-128', 'struct-129',
       'struct-131', 'struct-132', 'struct-133', 'struct-134', 'struct-135',
       'struct-136', 'struct-137', 'struct-138', 'struct-139', 'struct-140',
       'struct-141', 'struct-142', 'struct-144', 'struct-145', 'struct-146',
       'struct-149', 'struct-150', 'struct-151', 'struct-152', 'struct-153',
       'struct-154', 'struct-155', 'struct-156', 'struct-157', 'struct-158',
       'struct-159', 'struct-160', 'struct-162', 'struct-163', 'struct-164',
       'struct-165']

def get_maccs_fingerprints(input_smiles):
    from pepper_lab.pepper import Pepper
    from pepper_lab.descriptors import Descriptors

    # calculate descriptors
    pep = Pepper(renku=True)
    descriptors = Descriptors(pep)
    descriptors.model_data = input_smiles
    descriptors.load_descriptors(from_csv=False, MACCS=True)
    descriptors.maccs.drop(columns=descriptors.smiles_name, inplace=True)
    reduced_matrix = descriptors.maccs.filter(items=reduced_features_names)
    # descriptors.maccs = pd.DataFrame(descriptors.maccs)
    # processed_X = descriptors.maccs[[descriptors.maccs.columns.intersection.isin(reduced_features_names)]]
    # processed_X = descriptors.maccs[descriptors.maccs.columns.intersection.isin(reduced_features_names)]
    return reduced_matrix
