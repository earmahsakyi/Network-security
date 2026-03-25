import sys,os
import pandas as pd
import numpy as np
from networksecurity.entity.config_entity import DataValidationConfig
from networksecurity.entity.artifact_entity import DataValidationArtifact
from networksecurity.logging.logger import logging
from networksecurity.exception.exception import CustomException
from networksecurity.entity.artifact_entity import DataIngestionArtifact
from scipy.stats import ks_2samp
from networksecurity.constant.training_pipeline import schema_file_path
from networksecurity.utils.main_utils.utils import read_yaml_file
from networksecurity.utils.main_utils.utils import write_yaml_file


class DataValidation:
    def __init__(self,data_ingestion_artifact:DataIngestionArtifact,
                 data_valiation_config: DataValidationConfig):
        try:
            self.data_ingestion_artifact = data_ingestion_artifact
            self.data_validation_config = data_valiation_config
            self.schema_config = read_yaml_file(schema_file_path)
        except Exception as e:
            raise CustomException(e,sys)
    
    @staticmethod
    def read_data(file_path) -> pd.DataFrame:
        try:
            return pd.read_csv(file_path)

        except Exception as e:
            raise CustomException
    
    def validate_number_of_columns(self,dataframe:pd.DataFrame) -> bool:
        try:
            number_of_columns = len(self.schema_config['columns'])
            logging.info(f'required number of columns: {number_of_columns}')
            num_col_of_dataframe = len(dataframe.columns)
            logging.info(f' dataframe has this number of columns: {num_col_of_dataframe}')
            if number_of_columns == num_col_of_dataframe:
                return True
            return False

        except Exception as e:
            raise CustomException(e,sys)
    def validate_numerical_columns(self,dataframe:pd.DataFrame)-> bool:
        try:
            number_of_num_cols = set(self.schema_config['numerical_columns']);
            num_col_dataframe = [col for col in dataframe.columns if pd.api.types.is_numeric_dtype(dataframe[col])]
            if number_of_num_cols == set(num_col_dataframe):
                return True
            return False

        except Exception as e:
            raise CustomException(e,sys)
    
    def detect_dataset_drift(self,base_df,current_df,threshold=0.05) -> bool:
        try:
            status = True
            report= {}
            for col in base_df.columns:
                d1 = base_df[col]
                d2 = current_df[col]
                is_same_dist = ks_2samp(d1,d2)
                if threshold <= is_same_dist.pvalue:
                    drift = False
                else:
                    drift= True
                    status = False
                report.update({
                    col: {
                        'p_value': float(is_same_dist.pvalue),
                        'drift_status': drift

                    }
                })
            drift_report_file_path = self.data_validation_config.drift_report_file_path
            dir_name = os.path.dirname(drift_report_file_path)
            os.makedirs(dir_name,exist_ok=True)
            write_yaml_file(file_path=drift_report_file_path,content=report)
        

            return status


        except Exception as e:
            raise CustomException(e,sys)
        
    def initiate_data_validation(self) -> DataValidationArtifact:
        try: 
            train_file_path = self.data_ingestion_artifact.trained_file_path
            test_file_path = self.data_ingestion_artifact.test_file_path

            ## read the data from data from train and test dataset
            logging.info('Reading the train and test dataset')
            train_dataframe = DataValidation.read_data(file_path=train_file_path)
            test_dataframe = DataValidation.read_data(file_path=test_file_path)

            ##validating the number of columns
            train_status = self.validate_number_of_columns(dataframe=train_dataframe)
            if not train_status:
                error_message = f'Train dataframe does not contain all columns. \n'
            
            test_status = self.validate_number_of_columns(dataframe=test_dataframe)
            if not test_status:
                error_message = f'Train dataframe does not contain all columns. \n'

            ##validate numerical columns
            train_num_cols_status = self.validate_numerical_columns(dataframe=train_dataframe)
            if not train_num_cols_status:
                message=f'Train dataframe does not contain the exact numerical features'
            test_num_cols_status = self.validate_numerical_columns(dataframe=test_dataframe)
            if not test_num_cols_status:
                message=f'Train dataframe does not contain the exact numerical features'

            ##lets check data drift
            status = self.detect_dataset_drift(base_df=train_dataframe,current_df=test_dataframe)
            dir_path = os.path.dirname(self.data_validation_config.valid_train_file_path)
            os.makedirs(dir_path,exist_ok=True)

            train_dataframe.to_csv(
                self.data_validation_config.valid_train_file_path,index=False,header=True
            )
            test_dataframe.to_csv(
                self.data_validation_config.valid_test_file_path,index=False,header=True
            )

            data_validation_artifact = DataValidationArtifact(
                validation_status=status,
                valid_train_file_path=self.data_ingestion_artifact.trained_file_path,
                valid_test_file_path=self.data_ingestion_artifact.test_file_path,
                invalid_test_file_path=None,
                invalid_train_file_path=None,
                drift_report_file_path=self.data_validation_config.drift_report_file_path

            )

            return data_validation_artifact

            

        except Exception as e:
            raise CustomException(e,sys)


