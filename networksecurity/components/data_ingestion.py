import sys
import os
import pandas as pd
import numpy as np
from networksecurity.logging.logger import logging
from networksecurity.exception.exception import CustomException
from sklearn.model_selection import train_test_split
from networksecurity.entity.config_entity import DataIngestionConfig
from pymongo.mongo_client import MongoClient
from pymongo.server_api import ServerApi
from dotenv import load_dotenv
import certifi
from networksecurity.entity.artifact_entity import DataIngestionArtifact

load_dotenv()

MONGODB_URL = os.getenv('MONGO_URL')
cert_auth = certifi.where()


class DataIngestion: 
    def __init__(self,data_ingestion_config: DataIngestionConfig):
        try:
            self.data_ingestion_config = data_ingestion_config

        except Exception as e:
            raise CustomException(e,sys)

    def  export_collection_as_dataframe(self):
        try:
            database_name = self.data_ingestion_config.database_name
            collection_name = self.data_ingestion_config.collection_name   
            self.mongo_client = MongoClient(MONGODB_URL,server_api=ServerApi('1'),tlsCAFile=cert_auth)
            collection = self.mongo_client[database_name][collection_name]
            df = pd.DataFrame(list(collection.find()))
           
            if '_id' in df.columns.to_list(): ## droping _id from the dataset
                df.drop(columns=['_id'], inplace=True)
            
            df.replace({'na':np.nan},inplace=True)
            return df
        
        except Exception as e:
            raise CustomException(e,sys)
    
    def export_data_into_feature_store(self, dataframe:pd.DataFrame):
        try:
            feature_store_file_path = self.data_ingestion_config.feature_store_file_path
            dir_path = os.path.dirname(feature_store_file_path)
            os.makedirs(dir_path,exist_ok=True)
            dataframe.to_csv(feature_store_file_path,header=True,index=False)

            return dataframe
        except Exception as e:
            raise CustomException(e,sys)
    
    def split_data_as_train_test(self,dataframe: pd.DataFrame):
        try:
            train_set, test_set = train_test_split(dataframe,
                                                   test_size=self.data_ingestion_config.train_test_split_ratio,random_state=42)
            logging.info('Performed train test split on the dataframe')
            logging.info('Exited split data_as_train_test method of Data_Ingestion class')
            dir_path = os.path.dirname(self.data_ingestion_config.training_file_path)
            os.makedirs(dir_path,exist_ok=True)
            train_set.to_csv(self.data_ingestion_config.training_file_path,header=True,index=False)
            test_set.to_csv(self.data_ingestion_config.testing_file_path,header=True,index=False)
            logging.info('Exported train and test file path')

        except Exception as e:
            raise CustomException(e,sys)

    def initiate_data_ingestion(self):
        try:
        
            dataframe = self.export_collection_as_dataframe()
            dataframe = self.export_data_into_feature_store(dataframe=dataframe)
            self.split_data_as_train_test(dataframe=dataframe)
            data_ingestion_artifacts = DataIngestionArtifact(trained_file_path=self.data_ingestion_config.training_file_path,
                                                             test_file_path=self.data_ingestion_config.testing_file_path)

            return (
                data_ingestion_artifacts.trained_file_path,
                data_ingestion_artifacts.test_file_path
            )

        except Exception as e:
            raise CustomException(e,sys)