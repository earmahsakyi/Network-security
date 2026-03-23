from datetime import datetime
import os 
from networksecurity.constant import training_pipeline


class TrainingPipelineConfig:
    def __init__(self,timestamp=datetime.now()):
        timestamp = timestamp.strftime('%m_%d_%Y_%H_%M_%S')
        self.pipeline_name = training_pipeline.pipeline_name
        self.artifact_name = training_pipeline.artifact_dir
        self.artifact_dir = os.path.join(self.artifact_name,timestamp)
        self.timestamp = timestamp

class DataIngestionConfig:
    def __init__(self, training_pipeline_config: TrainingPipelineConfig):
        self.data_ingestion_dir: str = os.path.join(
            training_pipeline_config.artifact_dir,
            training_pipeline.data_ingestion_dir_name
        ) ## getting the directory for the data ingestion (artifacts-timestamp/data_ingestion)

        self.feature_store_file_path: str = os.path.join(
            self.data_ingestion_dir,
            training_pipeline.data_ingestion_feature_store_dir,training_pipeline.file_name
        ) ##getting the directory for the data ingestion feature store (artifacts-timestamp/data_ingestion/feature_store/phisinData.csv)

        self.training_file_path: str = os.path.join(
            self.data_ingestion_dir,
            training_pipeline.data_ingestion_ingested_dir,training_pipeline.train_file_name
        )  ##getting the directory for the data ingestion train file path (artifacts-timestamp/data_ingestion/ingested/train.csv)
        
        self.testing_file_path: str = os.path.join(
            self.data_ingestion_dir,
            training_pipeline.data_ingestion_ingested_dir,training_pipeline.test_file_name
        )  ##getting the directory for the data ingestion test file path (artifacts-timestamp/data_ingestion/ingested/test.csv)

        self.train_test_split_ratio: float = training_pipeline.data_ingestion_train_test_split_ratio
        self.collection_name: str = training_pipeline.data_ingestion_collection_name
        self.database_name: str = training_pipeline.data_ingestion_database_name

        