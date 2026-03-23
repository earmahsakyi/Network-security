from networksecurity.components.data_ingestion import DataIngestion
from networksecurity.logging.logger import logging
import sys
from networksecurity.exception.exception import CustomException
from networksecurity.entity.config_entity import DataIngestionConfig
from networksecurity.entity.config_entity import TrainingPipelineConfig

if __name__ == '__main__':
    try:
        training_pipeline_config = TrainingPipelineConfig()
        data_ingestion_config = DataIngestionConfig(training_pipeline_config=training_pipeline_config)
        data_ingestion = DataIngestion(data_ingestion_config=data_ingestion_config)
        logging.info('Initiate the data ingestion')
        train_path,test_path =data_ingestion.initiate_data_ingestion()
        print(train_path)
        print(test_path)
    except Exception as e:
        raise CustomException(e,sys)