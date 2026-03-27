import os,sys
import pandas as pd
import numpy as np
from networksecurity.entity.config_entity import DataTransformationConfig
from sklearn.impute import KNNImputer
from sklearn.pipeline import Pipeline
from networksecurity.exception.exception import CustomException
from networksecurity.logging.logger import logging
from networksecurity.constant.training_pipeline import target_column,data_transformation_imputer_params
from networksecurity.entity.artifact_entity import DataTransformationArtifact,DataValidationArtifact
from networksecurity.utils.main_utils.utils import save_numpy_array_data,save_object


class DataTransformation:
    def __init__(self,data_validation_artifact:DataValidationArtifact,data_transformation_config:DataTransformationConfig):

        try:
            self.data_validation_artifact = data_validation_artifact
            self.data_transformation_config = data_transformation_config
        except Exception as e:
            raise CustomException(e,sys)
    
    @staticmethod
    def read_data(file_path) -> pd.DataFrame:
        try:
            return pd.read_csv(file_path)

        except Exception as e:
            raise CustomException(e,sys)
    
    def get_data_transfromer_object(cls)-> Pipeline:
        try:
            logging.info('entered get_data_transfromer_object method')
            imputer = KNNImputer(**data_transformation_imputer_params)
            logging.info(f'initialised KNNImputer with {data_transformation_imputer_params}')
            preprocessor:Pipeline = Pipeline([
                ('imputer',imputer)
            ])

            return preprocessor
        except Exception as e:
            raise CustomException(e,sys)
        
    def initiate_data_transformation(self)-> DataTransformationArtifact:
        try:
            logging.info('started the data_transformation method class')
            ##read the data using the static method created
            train_df = DataTransformation.read_data(self.data_validation_artifact.valid_train_file_path)
            test_df = DataTransformation.read_data(self.data_validation_artifact.valid_test_file_path)

            
            ## drop target column
            input_feature_train_df = train_df.drop(columns=[target_column])
            target_feature_train_df = train_df[target_column]
            target_feature_train_df = target_feature_train_df.replace(-1,0)

            input_feature_test_df = test_df.drop(columns=[target_column])
            target_feature_test_df = test_df[target_column]
            target_feature_test_df = target_feature_test_df.replace(-1,0)

            preprocessor_obj = self.get_data_transfromer_object()
            transformed_input_train_feature = preprocessor_obj.fit_transform(input_feature_train_df)
            
            transformed_input_test_feature = preprocessor_obj.transform(input_feature_test_df)

            train_arr = np.c_[transformed_input_train_feature,np.array(target_feature_train_df)]
            test_arr = np.c_[transformed_input_test_feature,np.array(target_feature_test_df)]

            save_numpy_array_data(file_path=self.data_transformation_config.transformed_train_file_path,array=train_arr)
            save_numpy_array_data(file_path=self.data_transformation_config.transformed_test_file_path,array=test_arr)
            save_object(file_path=self.data_transformation_config.transformed_object_file_path,obj=preprocessor_obj)

            ##preparing artifacts;
            data_transformation_artifact = DataTransformationArtifact(
                transformed_object_file_path= self.data_transformation_config.transformed_object_file_path,
                transformed_train_file_path=self.data_transformation_config.transformed_train_file_path,
                transformed_test_file_path= self.data_transformation_config.transformed_test_file_path
            )

            return data_transformation_artifact


        except Exception as e:
            raise CustomException(e,sys)