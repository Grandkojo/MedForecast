# src/components/config.py

from dataclasses import dataclass
import os
from sklearn.ensemble import GradientBoostingClassifier, RandomForestClassifier


@dataclass
class DataIngestionConfig:
    data_path: str = os.path.join('artifacts', 'cleaned_data.csv')
    raw_data_path: str = os.path.join('artifacts', 'data.csv')

@dataclass
class DataIngestionConfig:
    data_path: str = os.path.join('artifacts', 'cleaned_data.csv')
    raw_data_path: str = os.path.join('artifacts', 'data.csv')

@dataclass
class DataTransformationConfig:
    preprocessor_obj_file_path: str = os.path.join('artifacts', 'model.pkl')

@dataclass
class ModelTrainerConfig:
    trained_model: str = os.path.join('artifacts', 'model.pkl')
    user_data_path: str = os.path.join('artifacts', 'user_data.csv')
    specifics_trained_model: str = os.path.join('artifacts', 'user_specific_model.pkl')
    models = GradientBoostingClassifier()
