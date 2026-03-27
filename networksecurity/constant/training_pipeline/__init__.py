import os 
import sys
import pandas as pd
import numpy as np

## Data Ingestion related constant start with data_ingestion var names

data_ingestion_collection_name: str = 'networkData'
data_ingestion_database_name: str = 'burna'
data_ingestion_dir_name: str = 'data_ingestion'
data_ingestion_feature_store_dir: str = 'feature_store'
data_ingestion_ingested_dir: str = 'ingested'
data_ingestion_train_test_split_ratio: float = 0.2

##definning common constant variable for traning pipeline
target_column = 'Result'
pipeline_name: str  = 'NetworkSecurity'
artifact_dir: str = 'Artifacts'
file_name: str = 'phisingData.csv'

train_file_name:str = 'train.csv'
test_file_name:str  = 'test.csv'
schema_file_path = os.path.join('data_schema','schema.yaml')


## Data validation related constants declared below
data_validation_dir_name:str = 'data_validation'
data_validation_valid_dir:str = 'validated'
data_validation_invalid_dir:str = 'invalid'
data_validation_drift_report_dir:str = 'drift_report'
data_validation_drift_report_file_name:str = 'report.yaml'

##data Transformation related constanst

preprocessing_object_file_name: str = 'preprocessing.pkl'
data_transformation_transformed_data_dir: str = 'transformed'
data_transformation_dir_name: str = 'data_transformation'
data_transformation_transformed_object_dir: str = 'transformed_object'

##KNN imputer to replace nan values
data_transformation_imputer_params: dict = {
    'missing_values': np.nan,
    'n_neighbors': 3,
    'weights': 'uniform'
}
