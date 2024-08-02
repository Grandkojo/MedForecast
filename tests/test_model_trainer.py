import unittest
from unittest.mock import patch, MagicMock
import pandas as pd
import numpy as np
from src.components.model_trainer import ModelTrainer
from src.exception import CustomException

class TestModelTrainer(unittest.TestCase):

    @patch('src.components.model_trainer.pd.read_csv')
    @patch('src.components.model_trainer.train_test_split')
    @patch('src.components.model_trainer.save_model')
    @patch('src.components.model_trainer.logging')
    def test_initiate_model_trainer(self, mock_logging, mock_save_model, mock_train_test_split, mock_read_csv):
        # Mock data
        mock_df = pd.DataFrame({
            'feature1': [1, 2, 3, 4],
            'feature2': [2, 3, 4, 5],
            'label': [0, 1, 0, 1]
        })

        mock_read_csv.return_value = mock_df
        mock_train_test_split.return_value = (mock_df[['feature1', 'feature2']], 
                                              mock_df[['feature1', 'feature2']], 
                                              mock_df['label'], 
                                              mock_df['label'])

        mock_model = MagicMock()
        mock_model.score.return_value = 0.75
        mock_model.feature_importances_ = np.array([0.7, 0.3])
        mock_model_trainer_config = MagicMock()
        mock_model_trainer_config.models = mock_model
        mock_model_trainer_config.trained_model = "mock_path"

        with patch('src.components.model_trainer.ModelTrainerConfig', return_value=mock_model_trainer_config):
            trainer = ModelTrainer()
            cleaned_data = "mock_path_to_data.csv"
            result = trainer.initiate_model_trainer(cleaned_data)

            # Assertions
            self.assertEqual(result[2], 0.75)
            self.assertEqual(result[1], ['feature1', 'feature2'])

            mock_read_csv.assert_called_once_with(cleaned_data)
            mock_save_model.assert_called_once_with(mock_model, "mock_path")
            self.assertTrue(mock_logging.info.called)

    @patch('src.components.model_trainer.pd.DataFrame.to_csv')
    @patch('src.components.model_trainer.train_test_split')
    @patch('src.components.model_trainer.save_model')
    @patch('src.components.model_trainer.logging')
    def test_retrain_model_with_user_input(self, mock_logging, mock_save_model, mock_train_test_split, mock_to_csv):
        # Mock data
        mock_df = pd.DataFrame({
            'feature1': [1, 2, 3, 4],
            'feature2': [2, 3, 4, 5],
            'label': [0, 1, 0, 1]
        })
        total_features_from_user = ['feature1', 'feature2', 'label']

        mock_train_test_split.return_value = (mock_df[['feature1', 'feature2']], 
                                              mock_df[['feature1', 'feature2']], 
                                              mock_df['label'], 
                                              mock_df['label'])

        mock_model = MagicMock()
        mock_model.score.return_value = 0.8
        mock_model_trainer_config = MagicMock()
        mock_model_trainer_config.models = mock_model
        mock_model_trainer_config.specifics_trained_model = "mock_specifics_path"
        mock_model_trainer_config.user_data_path = "mock_user_data_path"

        with patch('src.components.model_trainer.ModelTrainerConfig', return_value=mock_model_trainer_config):
            trainer = ModelTrainer()
            result = trainer.retrain_model_with_user_input(mock_df, total_features_from_user)

            # Assertions
            self.assertEqual(result[1], 0.8)
            self.assertEqual(result[2], len(total_features_from_user))

            mock_to_csv.assert_called_once_with("mock_user_data_path", index=False)
            mock_save_model.assert_called_once_with(mock_model, "mock_specifics_path")
            self.assertTrue(mock_logging.info.called)

    @patch('src.components.model_trainer.pd.DataFrame')
    @patch('src.components.model_trainer.logging')
    def test_predict_with_model(self, mock_logging, mock_DataFrame):
        # Mock data
        user_responses = [[1, 2], [3, 4]]
        total_features_from_user = ['feature1', 'feature2', 'prognosis']

        mock_df = pd.DataFrame(user_responses, columns=total_features_from_user)
        mock_DataFrame.return_value = mock_df

        mock_model = MagicMock()
        mock_model.predict.return_value = [0, 1]

        trainer = ModelTrainer()
        result = trainer.predict_with_model(mock_model, user_responses, total_features_from_user)

        # Assertions
        self.assertEqual(result[1], [0, 1])
        self.assertTrue(mock_logging.info.called)

if __name__ == '__main__':
    unittest.main()
