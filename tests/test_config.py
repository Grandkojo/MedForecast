import unittest
from src.components.config import DataIngestionConfig, DataTransformationConfig, ModelTrainerConfig
from sklearn.ensemble import GradientBoostingClassifier, RandomForestClassifier
import os

class TestConfigClasses(unittest.TestCase):

    def test_data_ingestion_config_defaults(self):
        config = DataIngestionConfig()
        self.assertEqual(config.data_path, os.path.join('artifacts', 'cleaned_data.csv'))
        self.assertEqual(config.raw_data_path, os.path.join('artifacts', 'data.csv'))

    def test_data_transformation_config_defaults(self):
        config = DataTransformationConfig()
        self.assertEqual(config.preprocessor_obj_file_path, os.path.join('artifacts', 'model.pkl'))

    def test_model_trainer_config_defaults(self):
        config = ModelTrainerConfig()
        self.assertEqual(config.trained_model, os.path.join('artifacts', 'model.pkl'))
        self.assertEqual(config.user_data_path, os.path.join('artifacts', 'user_data.csv'))
        self.assertEqual(config.specifics_trained_model, os.path.join('artifacts', 'user_specific_model.pkl'))
        self.assertIsInstance(config.models, GradientBoostingClassifier)

    def test_imports(self):
        self.assertTrue(hasattr(DataIngestionConfig, 'data_path'))
        self.assertTrue(hasattr(DataTransformationConfig, 'preprocessor_obj_file_path'))
        self.assertTrue(hasattr(ModelTrainerConfig, 'trained_model'))
        self.assertTrue(hasattr(ModelTrainerConfig, 'user_data_path'))
        self.assertTrue(hasattr(ModelTrainerConfig, 'specifics_trained_model'))
        self.assertTrue(hasattr(ModelTrainerConfig, 'models'))
        self.assertTrue(issubclass(GradientBoostingClassifier, object))
        self.assertTrue(issubclass(RandomForestClassifier, object))

    def test_attributes_are_strings(self):
        self.assertIsInstance(DataIngestionConfig.data_path, str)
        self.assertIsInstance(DataIngestionConfig.raw_data_path, str)
        self.assertIsInstance(DataTransformationConfig.preprocessor_obj_file_path, str)
        self.assertIsInstance(ModelTrainerConfig.trained_model, str)
        self.assertIsInstance(ModelTrainerConfig.user_data_path, str)
        self.assertIsInstance(ModelTrainerConfig.specifics_trained_model, str)

if __name__ == '__main__':
    unittest.main()