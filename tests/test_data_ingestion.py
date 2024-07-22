import unittest
from unittest.mock import patch, MagicMock
import pandas as pd
import numpy as np
import sys
from io import StringIO

# Importing the classes and functions to be tested
from src.components.data_ingestion import DataIngestion
from src.components.data_ingestion import ModelTrainer
from src.utils import get_top_n_features, calculate_number_of_parameters_to_append, append_other_feature

class TestDataIngestion(unittest.TestCase):

    @patch('src.components.data_ingestion.pd.read_csv')
    @patch('src.components.data_ingestion.pd.DataFrame.to_csv')
    @patch('src.components.data_ingestion.logging.info')
    @patch('src.components.data_ingestion.logging.error')
    @patch('src.components.data_ingestion.os.makedirs')
    def test_data_ingestion_success(self, mock_makedirs, mock_logging_error, mock_logging_info, mock_to_csv, mock_read_csv):
        # Mocking necessary objects
        mock_read_csv.return_value = pd.DataFrame({'col1': [1, 2, 2], 'col2': ['a', 'b', 'b']})
        mock_to_csv.return_value = None

        # Initialize DataIngestion class
        data_ingestion = DataIngestion()

        # Mock the output path
        data_ingestion.ingestion_config.data_path = 'mocked_data_path'
        data_ingestion.ingestion_config.raw_data_path = 'mocked_raw_data_path'

        # Test initiate_data_ingestion method
        result = data_ingestion.initiate_data_ingestion()

        # Assertions
        self.assertEqual(result, 'mocked_data_path')
        mock_logging_info.assert_any_call('Entered the data ingestion method')
        mock_logging_info.assert_any_call('Read the dataset as dataframe')
        mock_logging_info.assert_any_call('Performing drop duplicate and saving cleaned csv')
        mock_to_csv.assert_any_call('mocked_raw_data_path', index=False, header=True)
        mock_to_csv.assert_any_call('mocked_data_path', index=False, header=True)
        mock_logging_info.assert_any_call("Ingestion of the data is completed and cleaned csv saved to mocked_data_path")

    @patch('src.components.data_ingestion.logging.error')
    def test_data_ingestion_exception_handling(self, mock_logging_error):
        # Mocking necessary objects
        with patch('src.components.data_ingestion.pd.read_csv') as mock_read_csv:
            mock_read_csv.side_effect = Exception("Mocked exception")

            # Initialize DataIngestion class
            data_ingestion = DataIngestion()

            # Test initiate_data_ingestion method
            with self.assertRaises(Exception):
                data_ingestion.initiate_data_ingestion()

        # Assertions
        mock_logging_error.assert_any_call('Error in data ingestion: Mocked exception')

    @patch('src.components.model_trainer.ModelTrainer.initiate_model_trainer')
    @patch('src.components.model_trainer.ModelTrainer.retrain_model_with_user_input')
    @patch('src.components.model_trainer.ModelTrainer.predict_with_model')
    @patch('sys.stdout', new_callable=StringIO)
    def test_main_execution_success(self, mock_stdout, mock_predict_with_model, mock_retrain_model, mock_initiate_model):
        # Mocking necessary objects and methods
        mock_initiate_model.return_value = (MagicMock(), ['feature1', 'feature2'], 0.85)
        mock_retrain_model.return_value = (MagicMock(), 0.9, 5, ['feature1', 'feature2'])
        mock_predict_with_model.return_value = ('prediction', 0.8)

        # Mocking user responses
        np.random.seed(0)
        user_responses = np.random.choice([0, 1], size=(1, 5))

        # Simulate main execution flow
        with patch('src.components.data_ingestion.logging.error'):
            data_ingestion = DataIngestion()
            data_path = data_ingestion.initiate_data_ingestion()

            primary_column = "hip_joint_pain"

            model_train = ModelTrainer()

            cleaned_data, top_features, accuracy = model_train.initiate_model_trainer(data_path)

            features_from_user, length_of_parameters = get_top_n_features(cleaned_data, primary_column, n=35)

            num_of_features_to_append = calculate_number_of_parameters_to_append(length_of_parameters)

            total_features_for_new_training = append_other_feature(top_features[:num_of_features_to_append], features_from_user)

            new_model, new_accuracy, number_to_choose, total_features = model_train.retrain_model_with_user_input(cleaned_data, total_features_for_new_training)

            print(f"accuracy: {new_accuracy}, number: {number_to_choose}")

            user_responses = np.random.choice([0, 1], size=(1, number_to_choose))

            prediction, _ = model_train.predict_with_model(new_model, user_responses, total_features)
            print(prediction)

        # Assertions
        self.assertIn("accuracy: 0.9, number: 5", mock_stdout.getvalue())
        self.assertIn("prediction", mock_stdout.getvalue())

    @patch('src.components.data_ingestion.pd.read_csv')
    @patch('src.components.data_ingestion.pd.DataFrame.to_csv')
    @patch('src.components.data_ingestion.logging.info')
    @patch('src.components.data_ingestion.logging.error')
    @patch('src.components.data_ingestion.os.makedirs')
    def test_data_ingestion_csv_operations(self, mock_makedirs, mock_logging_error, mock_logging_info, mock_to_csv, mock_read_csv):
        # Mocking necessary objects
        mock_read_csv.return_value = pd.DataFrame({'col1': [1, 2, 2], 'col2': ['a', 'b', 'b']})
        mock_to_csv.return_value = None

        # Initialize DataIngestion class
        data_ingestion = DataIngestion()

        # Mock the output path
        data_ingestion.ingestion_config.data_path = 'mocked_data_path'
        data_ingestion.ingestion_config.raw_data_path = 'mocked_raw_data_path'

        # Test initiate_data_ingestion method
        result = data_ingestion.initiate_data_ingestion()

        # Assertions
        mock_read_csv.assert_called_once()
        mock_to_csv.assert_any_call('mocked_raw_data_path', index=False, header=True)
        mock_to_csv.assert_any_call('mocked_data_path', index=False, header=True)

if __name__ == '__main__':
    unittest.main()
