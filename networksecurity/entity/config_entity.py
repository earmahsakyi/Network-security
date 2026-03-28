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
    

class DataValidationConfig:
    def __init__(self,training_pipeline_config: TrainingPipelineConfig):
        ##getting artifacts-timestamp/data_validation
        self.data_validation_dir: str = os.path.join(training_pipeline_config.artifact_dir,training_pipeline.data_validation_dir_name)
         ##getting artifacts-timestamp/data_validation/validated
        self.valid_data_dir: str = os.path.join(self.data_validation_dir,training_pipeline.data_validation_valid_dir)
         ##getting artifacts-timestamp/data_validation/invalid
        self.invalid_data_dir: str = os.path.join(self.data_validation_dir,training_pipeline.data_validation_invalid_dir)
         ##getting artifacts-timestamp/data_validation/train.csv
        self.valid_train_file_path: str = os.path.join(self.data_validation_dir,training_pipeline.train_file_name)
         ##getting artifacts-timestamp/data_validation/test.csv
        self.valid_test_file_path: str = os.path.join(self.data_validation_dir,training_pipeline.test_file_name)
        
        self.invalid_train_file_path:str = os.path.join(self.data_validation_dir,training_pipeline.train_file_name)
        self.invalid_test_file_path:str = os.path.join(self.data_validation_dir,training_pipeline.test_file_name)
        ## getting artifacts-timestamp/drift_report/report.yaml
        self.drift_report_file_path: str = os.path.join(self.data_validation_dir,
                                                        training_pipeline.data_validation_drift_report_dir,
                                                        training_pipeline.data_validation_drift_report_file_name
                                                        )

class DataTransformationConfig:
   def __init__(self,training_pipeline_config:TrainingPipelineConfig):
        self.data_transformation_dir: str = os.path.join( training_pipeline_config.artifact_dir,training_pipeline.data_transformation_dir_name )
        self.transformed_train_file_path: str = os.path.join( self.data_transformation_dir,training_pipeline.data_transformation_transformed_data_dir,
            training_pipeline.train_file_name.replace("csv", "npy"),)
        self.transformed_test_file_path: str = os.path.join(self.data_transformation_dir,  training_pipeline.data_transformation_transformed_data_dir,
            training_pipeline.test_file_name.replace("csv", "npy"), )
        self.transformed_object_file_path: str = os.path.join( self.data_transformation_dir, training_pipeline.data_transformation_transformed_object_dir,
            training_pipeline.preprocessing_object_file_name)
        
class ModelTrainerConfig:
    def __init__(self,training_pipeline_config:TrainingPipelineConfig):
        self.model_trainer_dir: str = os.path.join(
            training_pipeline_config.artifact_dir, training_pipeline.model_trainer_dir_name
        )
        self.trained_model_file_path: str = os.path.join(
            self.model_trainer_dir, training_pipeline.model_trainer_trained_model_dir, 
            training_pipeline.model_file_name
        )
        self.expected_accuracy: float = training_pipeline.model_trainer_expected_score
        self.overfitting_underfitting_threshold = training_pipeline.model_trainer_over_fitting_under_fitting_threshold