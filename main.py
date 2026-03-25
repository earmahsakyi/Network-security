from networksecurity.components.data_ingestion import DataIngestion
from networksecurity.components.data_validation import DataValidation
from networksecurity.logging.logger import logging
import sys
from networksecurity.exception.exception import CustomException
from networksecurity.entity.config_entity import DataIngestionConfig,DataValidationConfig
from networksecurity.entity.config_entity import TrainingPipelineConfig

if __name__ == '__main__':
    try:
        training_pipeline_config = TrainingPipelineConfig()
        data_ingestion_config = DataIngestionConfig(training_pipeline_config=training_pipeline_config)
        data_ingestion = DataIngestion(data_ingestion_config=data_ingestion_config)
        logging.info('Initiate the data ingestion')
        data_ingestion_art =data_ingestion.initiate_data_ingestion()
        logging.info('data ingestion completed')
        data_validation_config = DataValidationConfig(training_pipeline_config=training_pipeline_config)
        data_validation = DataValidation(data_ingestion_artifact=data_ingestion_art,data_valiation_config=data_validation_config)
        logging.info('initiate data validation')
        data_V_at = data_validation.initiate_data_validation()
        print(data_V_at)
        logging.info('data validation is completed')
    except Exception as e:
        raise CustomException(e,sys)