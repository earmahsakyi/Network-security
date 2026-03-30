import os,sys
import pandas as pd
import numpy as np
import mlflow
from networksecurity.exception.exception import CustomException
from networksecurity.logging.logger import logging
from networksecurity.entity.config_entity import ModelTrainerConfig
from networksecurity.entity.artifact_entity import ModelTrainerArtifact,DataTransformationArtifact
from networksecurity.utils.main_utils.utils import save_object,load_object,load_numpy_array_data,evaluate_models
from networksecurity.utils.ml_utils.model import NetworkModel
from networksecurity.utils.ml_utils.mertics import get_classification_score
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import r2_score
from sklearn.tree import DecisionTreeClassifier
from sklearn.ensemble import AdaBoostClassifier,GradientBoostingClassifier,RandomForestClassifier



class ModelTrainer:
    def __init__(self,model_trainer_config:ModelTrainerConfig,data_transformation_artifact:DataTransformationArtifact):
        try:
            self.model_trainer_config = model_trainer_config
            self.data_transformation_artifact = data_transformation_artifact
        except Exception as e:
            raise CustomException(e,sys)
    
    def tract_mlflow(self,model,classification_metric):
        try:
            logging.info('entered ml flow method')
            with mlflow.start_run():
                f1_score = classification_metric.f1_score
                precision_score = classification_metric.precision_score
                recall_score = classification_metric.recall_score

                mlflow.log_metric('f1_score',f1_score)
                mlflow.log_metric('precision_score',precision_score)
                mlflow.log_metric('recall_score',recall_score)
                mlflow.sklearn.log_model('best model',model)

        except Exception as e:
            raise CustomException(e,sys)


    def train_model(self,X_train,y_train,X_test,y_test):
        models = {
                "Random Forest": RandomForestClassifier(verbose=1),
                "Decision Tree": DecisionTreeClassifier(),
                "Gradient Boosting": GradientBoostingClassifier(verbose=1),
                "Logistic Regression": LogisticRegression(verbose=1),
                "AdaBoost": AdaBoostClassifier(),
              
            }
        params={
            "Decision Tree": {
                'criterion':['gini', 'entropy', 'log_loss'],
                # 'splitter':['best','random'],
                # 'max_features':['sqrt','log2'],
            },
            "Random Forest":{
                # 'criterion':['gini', 'entropy', 'log_loss'],
                
                # 'max_features':['sqrt','log2',None],
                'n_estimators': [8,16,32,128,256]
            },
            "Gradient Boosting":{
                # 'loss':['log_loss', 'exponential'],
                'learning_rate':[.1,.01,.05,.001],
                'subsample':[0.6,0.7,0.75,0.85,0.9],
                # 'criterion':['squared_error', 'friedman_mse'],
                # 'max_features':['auto','sqrt','log2'],
                'n_estimators': [8,16,32,64,128,256]
            },
            "Logistic Regression":{},
            "AdaBoost":{
                'learning_rate':[.1,.01,.001],
                'n_estimators': [8,16,32,64,128,256]
            }
            
        }

        model_report: dict = evaluate_models(X_train=X_train,y_train=y_train,X_test=X_test,y_test=y_test,models=models,params=params)

        ##get the best_model name 
        best_model_name = max(model_report,key=model_report.get)
        best_model_score = model_report[best_model_name]

        best_model = models[best_model_name]
        logging.info(f'Best Model is: {best_model}')
        y_train_pred = best_model.predict(X_train)
        classification_train_metric = get_classification_score(y_true=y_train,y_pred=y_train_pred)
        
        ##function to track the ml flow for train dataset
        self.tract_mlflow(model=best_model_name,classification_metric=classification_train_metric)



        y_test_pred = best_model.predict(X_test)
        classification_test_metric = get_classification_score(y_true=y_test,y_pred=y_test_pred)
        ##mlflow for test dataset
        self.tract_mlflow(model=best_model_name,classification_metric=classification_test_metric)

        ##preprocessor.pkl file
        object_file_path = self.data_transformation_artifact.transformed_object_file_path
        preprocessor = load_object(file_path=object_file_path)

        model_dir_path = os.path.dirname(self.model_trainer_config.trained_model_file_path)
        os.makedirs(model_dir_path,exist_ok=True)

        Network_Model = NetworkModel(preprocessor=preprocessor,model=best_model)
        model_file_path = self.model_trainer_config.trained_model_file_path
        save_object(file_path=model_file_path,obj=Network_Model)

        ##Model Trainer artifacts
        model_trainer_artifact = ModelTrainerArtifact(
            trained_model_file_path=model_dir_path,
            train_metric_artifact=classification_train_metric,
            test_metric_artifact= classification_test_metric
        ) 
        logging.info(f'Model Trainer Artifacts: {model_trainer_artifact}')

        return model_trainer_artifact

        
    def initiate_model_trainer(self) -> ModelTrainerArtifact:
        try:
            train_file_path = self.data_transformation_artifact.transformed_train_file_path
            test_file_path = self.data_transformation_artifact.transformed_test_file_path
            

            ##loading training and test array
            train_arr = load_numpy_array_data(file_path=train_file_path)
            test_arr = load_numpy_array_data(file_path=test_file_path)

            X_train,y_train,X_test,y_test = (
                train_arr[:,:-1],
                train_arr[:,-1],
                test_arr[:,:-1],
                test_arr[:,-1],
            )
            Model_trainer_artifact = self.train_model(X_train=X_train,y_train=y_train,X_test=X_test,y_test=y_test)

            return Model_trainer_artifact

        except Exception as e:
            raise CustomException(e,sys)

        
