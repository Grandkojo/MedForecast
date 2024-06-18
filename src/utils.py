from src.exception import CustomException
from src.logger import logging
import dill
import pandas as pd
import sys

def save_model(model, filename):
    """saves a model to the required destination"""
    try:
        with open(filename, 'wb') as file:
             dill.dump(model, file)
    except Exception as e:
        logging.info(f"Error saving model: {e}")
        raise CustomException(e, sys)

def get_columns_with_one(dataframe, primary_col):
    """ get columns in dataframe with their value as one
    """
    try:
        filtered_df = dataframe[dataframe[primary_col] == 1]

        cols_with_one = filtered_df.drop(columns=[primary_col]).any(axis=0)
        cols_with_one = cols_with_one[cols_with_one].index.tolist()
        cols = cols_with_one[:]
        prognosis_col = cols.pop()

        return cols, prognosis_col
    except Exception as e:
        logging.info(f"Error getting columns: {e}")
        raise CustomException(e, sys)
    
def get_top_n_features(dataframe, primary_col, n=40):
    """ get the n number of features required for the user to be asked on
    """
    try:
        cols_with_one, prognosis_col = get_columns_with_one(dataframe, primary_col)
        top_features = cols_with_one[:n]
        return top_features, len(top_features)
    except Exception as e:
        logging.info(f"Error getting features: {e}")
        raise CustomException(e, sys)

def append_other_feature(top_features_to_append, top_features_for_user):
    """append top features from actual dataser if the features to ask user
        does not add up to the required accuracy of model
    """
    try:
        for item in top_features_to_append:
            if item not in top_features_for_user:
                    top_features_for_user.append(item)
        
        if "Prognosis" in top_features_for_user:
            top_features_for_user.remove("Prognosis")
        
        top_features_for_user.append('prognosis')
        
        return top_features_for_user
    except Exception as e:
         logging.info(f"Error appending new features: {e}")
         raise CustomException(e, sys)

def search_parameters(search_query, feature_names):
    """a search query to get the parameters in the dataset"""
    try:
        return [feature for feature in feature_names if search_query.lower() in feature.lower()]
    except Exception as e:
         logging.info(f"Error in search: {e}")
         raise CustomException(e, sys)

def calculate_number_of_parameters_to_append(cur_length):
     """calculates the number of top parameters to append in case the accuracy is not met
      """
     try:
           desired_length = 40
           if cur_length < desired_length:
                 length_to_add = desired_length - cur_length + 1
                 return length_to_add
           return 0
     except Exception as e:
          logging.info(f"Error in calculating parameters: {e}")
          raise CustomException(e, sys)
