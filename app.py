from networksecurity.pipeline.training_pipeline import TrainingPipeline
import sys,os
import certifi
from pymongo.mongo_client import MongoClient
from pymongo.server_api import ServerApi
from dotenv import load_dotenv
from networksecurity.logging.logger import logging
from networksecurity.exception.exception import CustomException
from fastapi.middleware.cors import CORSMiddleware
from fastapi import FastAPI, File, UploadFile, Request
from uvicorn import run as app_run
from fastapi.responses import Response
from starlette.responses import RedirectResponse
import pandas as pd
from networksecurity.utils.ml_utils.model import NetworkModel
from networksecurity.utils.main_utils.utils import load_object
from networksecurity.constant.training_pipeline import data_ingestion_database_name,data_ingestion_collection_name
from fastapi.templating import Jinja2Templates

templates = Jinja2Templates(directory='./templates')
load_dotenv()

uri = os.getenv('MONGO_URL')
cert_auth = certifi.where() ##certificate authority to verify the ssl/tls certificates
mongo_client = MongoClient(uri,server_api=ServerApi('1'),tlsCAFile=cert_auth)

database = mongo_client[data_ingestion_database_name]
collection = database[data_ingestion_collection_name]

app = FastAPI()
origins = ['*']

app.add_middleware(CORSMiddleware,allow_origins=origins,
                   allow_credentials=True,allow_methods=['*'],
                   allow_headers=['*'])

@app.get('/',tags=['authentication'])
async def index():
    return RedirectResponse(url='/docs') 

@app.get('/train')
async def train_route():
    try:
        train_pipeline = TrainingPipeline()
        train_pipeline.run_pipeline()
        return Response(status_code=200,content='training successful')
    
    except Exception as e:
        raise CustomException(e,sys)
    
@app.post('/predict')
async def predict_route(request:Request,file:UploadFile=File(...)):
    try:
        df = pd.read_csv(file.file)
        preprocessor_obj_path = os.path.join('final_models','preprocessor.pkl')
        model_obj_path = os.path.join('final_models','model.pkl')
        preprocessor = load_object(file_path=preprocessor_obj_path)
        model = load_object(file_path=model_obj_path)
        network_model = NetworkModel(preprocessor=preprocessor,model=model)
        print("Columns:", df.columns)
        print("First row:", df.iloc[0])
        print("Data types:", df.dtypes)
        y_pred = network_model.predict(df)
        print(y_pred)
        df['predicted_col'] = y_pred
        print(df['predicted_col'])
        df.to_csv('prediction_output/output.csv')
        table_html = df.to_html()

        return  templates.TemplateResponse(request=request,name='table.html',context={'table':table_html})
    except Exception as e:
        raise CustomException(e,sys)
    


    
if __name__ == '__main__':
    app_run(app=app,host='localhost',port=5000)


