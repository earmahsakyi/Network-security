import os
import sys
import json
import certifi
from dotenv import load_dotenv
import pandas as pd
import numpy as np
from pymongo.mongo_client import MongoClient
from pymongo.server_api import ServerApi
from networksecurity.logging.logger import logging
from networksecurity.exception.exception import CustomException

load_dotenv()

MONGODB_URL = os.getenv('MONGO_URL') ## mongodb url
cert_auth = certifi.where() ##certificate authority to verify the ssl/tls certificates


class NetworkDataExtract:
    def __init__(self,collection,database): ## constructor for creating object instance
        try:
            self.database = database
            self.collection = collection
            self.records  = []

        except Exception as e:
            raise CustomException(e,sys)

    def cv_to_json_convertor(self,file_path):
        try:
            ##step 1 read your data
            data = pd.read_csv(file_path)
            ## step 2 drop index if any 
            data.reset_index(drop=True,inplace=True)

            ##convert each row to json format
            self.records = json.loads((data.T.to_json())).values()
            return self.records 

        except Exception as e:
            raise CustomException(e,sys)



    def insert_data_mongodb(self):
        try:
            mongo_client = MongoClient(MONGODB_URL,server_api=ServerApi('1'),tlsCAFile=cert_auth)## connect to database
            db = mongo_client[self.database] ## specify database
            coll = db[self.collection] ## collection
            coll.insert_many(self.records) ##insert into database

            return (len(self.records))


        except Exception as e:
            raise CustomException(e,sys)
        


