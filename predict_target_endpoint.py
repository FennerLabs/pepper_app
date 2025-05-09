# from narwhals import DataFrame
from rdkit.Chem import PandasTools
from utils import image_from_mol


def render_structures(predictions_df):
    PandasTools.AddMoleculeColumnToFrame(predictions_df, smilesCol='SMILES', molCol='Structure')
    predictions_df["Structure"] = predictions_df["Structure"].apply(image_from_mol)
    return predictions_df


def predict_WWTP_breakthrough(input_data, input_smiles_type: str = 'dataframe'):
    from pepper_lab.predict import Predict

    input_smiles = input_data
    pepper_predict = Predict(renku=True)
    predictions_df = pepper_predict.predict_endpoint('pepper_object_wwtp_optimized_trained_model.pkl',
                                    input_model_format='pickle', input_smiles=input_smiles,
                                    input_smiles_type=input_smiles_type)

    print(predictions_df.columns)

    # Select what to show in the app
    logb = predictions_df['logB_predicted']
    breakthrough_perc = (10**logb)*100
    rounded_b_perc = round(breakthrough_perc, 1)
    predictions_df['Breakthrough (%)'] = rounded_b_perc

    confidence = predictions_df['{}_predicted'.format(pepper_predict.model.target_variable_std_name)]
    rounded_confidence = round(confidence, 2)
    predictions_df['Confidence 0-1'] = rounded_confidence

    predictions_df = predictions_df[[pepper_predict.model.compound_name,
                                     'Breakthrough (%)',
                                     'Confidence 0-1',
                                     pepper_predict.model.smiles_name]]

    predictions_df = render_structures(predictions_df)
    return predictions_df


def get_confidence_level(standard_deviation_list):
    new_list = []
    for stdev in standard_deviation_list.values:
        if stdev < 0.5:
            cat = 'high'
        elif stdev < 0.7:
            cat = 'medium'
        else:
            cat = 'low'
        new_list.append(cat)
    return new_list


def predict_soil_DT50(input_data, model_type='fast', input_smiles_type: str = 'dataframe'):
    from pepper_lab.predict import Predict

    input_smiles = input_data
    pepper_predict = Predict(renku=True)
    if model_type == 'fast':
        predictions_df = pepper_predict.predict_endpoint('final_model_soil_all_data_fast.pkl',
                                    input_model_format='pickle', input_smiles=input_smiles,
                                    input_smiles_type=input_smiles_type)
    elif model_type == 'enviPath':
        predictions_df = pepper_predict.predict_endpoint('final_model_soil_all_data_default_setup.pkl',
                                    input_model_format='pickle', input_smiles=input_smiles,
                                    input_smiles_type=input_smiles_type)
    else:
        print("Model not defined")

    predictions_df.drop(columns='SMILES', inplace=True)
    predictions_df['logDT50_mean_predicted'] = predictions_df['logDT50_mean_predicted'].round(2)
    predictions_df['logDT50_std_predicted'] = predictions_df['logDT50_std_predicted'].round(2)
    predictions_df['Predicted DT50 [days]'] = (10 ** predictions_df['logDT50_mean_predicted']).round(1)
    predictions_df['Confidence level'] = get_confidence_level(predictions_df['logDT50_std_predicted'])
    if type(input_data) != str and 'Compound' in input_data.columns:
        predictions_df['compound_name'] = input_data['Compound']
    predictions_df.rename(columns={'original_SMILES': 'SMILES',
                                   'logDT50_mean_predicted': 'Predicted logDT50 [log(days)]',
                                   'logDT50_std_predicted': 'Predicted uncertainty (stdev of logDT50)',
                                   'compound_name': 'Compound name',
                                   'logDT50_mean_experimental': 'experimental logDT50',
                                   'logDT50_std_experimental': 'experimental variability (stdev of logDT50)'},
                          inplace = True)
    predictions_df = predictions_df[['Compound name', 'Predicted DT50 [days]','Confidence level',
                                     'Predicted logDT50 [log(days)]',
                                     'Predicted uncertainty (stdev of logDT50)', 'experimental logDT50',
                                     'experimental variability (stdev of logDT50)', 'warnings', 'SMILES',]]
    predictions_df = render_structures(predictions_df)
    return predictions_df
