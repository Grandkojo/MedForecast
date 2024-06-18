import os
import sys
import pandas as pd
import numpy as np
from sklearn.metrics import accuracy_score
from sklearn.model_selection import train_test_split
from src.exception import CustomException
from src.logger import logging
from src.utils import save_model
from src.components.config import ModelTrainerConfig

class ModelTrainer:
    def __init__(self) -> None:
        """initialize the model trainer config"""
        self.model_trainer_config = ModelTrainerConfig()

    def initiate_model_trainer(self, cleaned_data):
        """initiate the actual model training by performing some processing
            cleaned_data: the dataset to be split for training and testing
        """
        try:
            logging.info("Split training and test data")
            cleaned_data = pd.read_csv(cleaned_data)
            X = cleaned_data.iloc[:, :-1]
            y = cleaned_data.iloc[:, -1]

            X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)
            logging.info("Split completed")

            logging.info("Training models")

            model = self.model_trainer_config.models    
            model.fit(X_train, y_train)
            accuracy = model.score(X_test, y_test)

            logging.info("Model fit and accuracy done")
            
            importances = model.feature_importances_
            indices = np.argsort(importances)[::-1]

            num_to_append = 25
            top_features = X.columns[indices[:num_to_append]].tolist()
            logging.info("Stored top 25 features in the model")

            save_model(model, self.model_trainer_config.trained_model)

            logging.info(f"Saved  model: {model.__class__.__name__} with accuracy: {accuracy}")

            return (cleaned_data, top_features, accuracy)
        
        except Exception as e:
            logging.error(f"Error in model training: {e}")
            raise CustomException(e, sys)

    def retrain_model_with_user_input(self, cleaned_data, total_features_from_user):
        """ retrain the model to specific user features chosen in the dynamic form
            cleaned_data: the actual data for the model
            total_features_from_user: the user features that are to be used to retrain the model
        """
        try:
            logging.info("Create new data csv for user")
            new_data = cleaned_data[total_features_from_user]

            logging.info("Saving the new user specific csv")
            new_data.to_csv(self.model_trainer_config.user_data_path, index=False)

            logging.info("Performing train test split on data")
            X_new = new_data.iloc[:, :-1]
            y_new= new_data.iloc[:, -1]

            X_train_new, X_test_new, y_train_new, y_test_new = train_test_split(X_new, y_new, test_size=0.2, random_state=42)
            
            logging.info("Training and fitting model")
            new_model = self.model_trainer_config.models
            new_model.fit(X_train_new, y_train_new)
            new_accuracy = new_model.score(X_test_new, y_test_new)

            number_to_choose = len(total_features_from_user)

            save_model(new_model, self.model_trainer_config.specifics_trained_model)
            logging.info("Model saved to location {}".format(self.model_trainer_config.specifics_trained_model))

            return (new_model, new_accuracy, number_to_choose, total_features_from_user)

        except Exception as e:
            raise CustomException(e, sys)
        
    def predict_with_model(self, new_model, user_responses, total_features_from_user):
        """
            predict the prognosis based on the user's input
            new_model: the newly trained model to fit the specific user
            user_responses: the array containing the user parameters chosen
        """
        try:
            logging.info("Creating user tailored dataframe")
            user_response_df = pd.DataFrame(user_responses, columns=total_features_from_user)
            user_response_df.drop(columns='prognosis', inplace=True)

            logging.info("Predicting prognosis")
            prediction = new_model.predict(user_response_df)

            logging.info("Prediction done")
            return (f"Predicted prognosis (using new model): {prediction}", prediction)
        except Exception as e:
            logging.info(f"Error predicting model: {e}")
            raise CustomException(e, sys)