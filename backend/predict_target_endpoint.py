from pepper_lab.predict import Predict
import pandas as pd

def predict(input_smiles):
    data = pd.DataFrame(input_smiles, columns=["SMILES"])
    pepper_predict = Predict(renku=True)
    predictions_df = pepper_predict.predict_endpoint('pepper_object_wwtp_optimized_trained_model.pkl',
                                    input_model_format='pickle', input_smiles=data,
                                    input_smiles_type='dataframe') # The backend accepts single molecules

    # Select what to show in the app
    logb = predictions_df['logB_predicted']
    breakthrough_perc = (10**logb)*100
    rounded_b_perc = round(breakthrough_perc, 1)
    predictions_df['Breakthrough (%)'] = rounded_b_perc

    confidence = predictions_df['{}_predicted'.format(pepper_predict.model.target_variable_std_name)]
    rounded_confidence = round(confidence, 2)
    predictions_df['Confidence 0-1'] = rounded_confidence

    predictions_df = predictions_df[[pepper_predict.model.compound_name,
                                     pepper_predict.model.smiles_name,
                                     'Breakthrough (%)',
                                     'Confidence 0-1']]
    predictions_df.fillna("", inplace=True)
    return predictions_df.to_dict(orient="list")
