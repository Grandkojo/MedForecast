import os
import sys
import pandas as pd
import numpy as np
from dataclasses import dataclass
from sklearn.model_selection import train_test_split
from src.exception import CustomException
from src.logger import logging
from src.components.model_trainer import ModelTrainer
from src.utils import get_top_n_features, append_other_feature, calculate_number_of_parameters_to_append
from src.components.config import DataIngestionConfig

class DataIngestion:
    def __init__(self) -> None:
        """ initialize the config for data ingestion
        """
        self.ingestion_config = DataIngestionConfig()

    def initiate_data_ingestion(self) -> str:
        """ initiate the ingestion of the data for processing
        """

        logging.info("Entered the data ingestion method")
        try:
            df = pd.read_csv('src/components/health.csv')

            logging.info('Read the dataset as dataframe')

            os.makedirs(os.path.dirname(self.ingestion_config.data_path), exist_ok=True)
            df.to_csv(self.ingestion_config.raw_data_path, index=False, header=True)

            logging.info('Performing drop duplicate and saving cleaned csv')

            df.drop_duplicates(inplace=True)
            df.to_csv(self.ingestion_config.data_path, index=False, header=True)

            logging.info("Ingestion of the data is completed and cleaned csv saved to {}".format(self.ingestion_config.data_path))

            return self.ingestion_config.data_path
        except Exception as e:
            logging.error(f"Error in data ingestion: {e}")
            raise CustomException(e, sys)



#test and simulate processing pipeline
if __name__ == '__main__':
    try:
        obj = DataIngestion()
        data_path = obj.initiate_data_ingestion()

        primary_column = "nausea"

        model_train = ModelTrainer()

        cleaned_data, top_features, accuracy = model_train.initiate_model_trainer(data_path)

        # print(top_features, accuracy )
        # print('\n')

        features_from_user, length_of_parameters = get_top_n_features(cleaned_data, primary_column, n=35)

        # print(features_from_user, length_of_parameters)
        # print('\n')


        num_of_features_to_append = calculate_number_of_parameters_to_append(length_of_parameters)

        # print(num_of_features_to_append)

        total_features_for_new_training = append_other_feature(top_features[:num_of_features_to_append] , features_from_user)

        # print(total_features_for_new_training, len(total_features_for_new_training))

        # print(length_of_parameters, len(total_features_for_new_training))

        new_model, new_accuracy, number_to_choose, total_features = model_train.retrain_model_with_user_input(cleaned_data, total_features_for_new_training)

        print(f"accuracy: {new_accuracy}, number: {number_to_choose}")

        #simulate a user's response would be conncted later
        user_responses = np.random.choice([0, 1], size=(1, number_to_choose))


        prediction, _ = model_train.predict_with_model(new_model, user_responses, total_features)
        print(prediction)
    
    except Exception as e:
        logging.error(f"Error in main execution: {e}")
        raise CustomException(e, sys)

        