from sklearn.ensemble import (AdaBoostClassifier, GradientBoostingRegressor, RandomForestRegressor)
from sklearn.linear_model import LinearRegression
from sklearn.metrics import r2_score
from sklearn.neighbors import KNeighborsRegressor
from sklearn.tree import DecisionTreeRegressor
from xgboost import XGBRegressor
from src.exception import CustomException
from src.logger import logging
from src.utils import save_object, evaluate_model
from dataclasses import dataclass
import os
import symtable
import sys


@dataclass
class ModelTrainerConfig:
    Trained_model_file_path = os.path.join("artifacts","model.pkl")

class ModelTrainer: 
    def __init__(self):
        self.model_trainer_config = ModelTrainerConfig()

    def initiate_model_trainer(self, train_array, test_array, preprocessor=None): 
        try:
            logging.info("split training and test input data")
            X_train, y_train, X_test, y_test = (train_array[:,:-1],
                                                train_array[:,-1],
                                                test_array[:,:-1],
                                                test_array[:,-1])
        
            models = {
                "Random Forest": RandomForestRegressor(),
                "Decision Tree": DecisionTreeRegressor(),
                "Gradient Boosting": GradientBoostingRegressor(),
                'Linear Regression' : LinearRegression(),
                "K-Neighbors Regressor" : KNeighborsRegressor(),
                "XGBoosting" : XGBRegressor(),
                "AdaBoost Classifier": AdaBoostClassifier()

            }
            
            

            model_report: dict=evaluate_model(X_train=X_train, y_train=y_train,
                                             X_test=X_test,y_test=y_test,
                                              models=models)
            best_model_score = max(sorted(model_report.values()))
            
            if best_model_score<0.6:
                raise CustomException("No best model found")

            best_model_name = list(model_report.keys())[
                list(model_report.values()).index(best_model_score)] 
            best_model = models[best_model_name]
            
            save_object(file_path=self.model_trainer_config.Trained_model_file_path,
                        obj=best_model)
            y_pred = best_model.predict(X_test)
            r2_square = r2_score(y_test, y_pred)
        except Exception as e:
            CustomException(e,sys)