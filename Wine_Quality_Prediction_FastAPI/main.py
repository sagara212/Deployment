from fastapi import FastAPI, HTTPException
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse
from pydantic import BaseModel
import joblib
import pandas as pd
import numpy as np
import logging
from dotenv import load_dotenv
import os

#load encirontment varibel from .env file in the same directory
load_dotenv()

#load model and scaler
model = None
scaler = None

app = FastAPI()

#serve the static files from the static folder
app.mount('/static', StaticFiles(directory='static'), name='static')

#Preload the Model for Latency Reduction
@app.on_event('startup')
async def load_model():
    global model, scaler
    try:
        #use environtment variabel to load model an scaler path
        model_path = os.getenv('MODEL_PATH', 'D:\DOCUMENT\INFORMATIKA\FULL PROJEK\FastAPI\Wine_Quality_Prediction\Best_model.pkl')
        scaler_path = os.getenv('SCALER_PATH', 'D:\DOCUMENT\INFORMATIKA\FULL PROJEK\FastAPI\Wine_Quality_Prediction\scaler.pkl')
        
        model = joblib.load(model_path)
        scaler = joblib.load(scaler_path)

        logging.info('model and scaler have ben loaded succesfully')
    except Exception as e:
        logging.error(f'error loading model or scaler: {e}')
        raise HTTPException(status_code=500, detail='error loading model')

class WineFeatures(BaseModel):
    fixed_acidity: float
    volatile_acidity:float
    citric_acid: float
    residual_sugar: float
    chlorides: float
    free_sulfur_dioxide: float
    total_sulfur_dioxide: float
    density: float
    pH: float
    sulphates: float
    alcohol: float

# Home endpoint
@app.get('/')
def home():
    return FileResponse("static/index.html")

#prdiction page endpoint
@app.get("/predict")
async def predict_page():
    return FileResponse('static/predict.html')

#Predict endpoint
@app.post('/predict')
def predict(wine: WineFeatures):

    if model is None or scaler is None:
        logging.error('model is not loaded')
        raise HTTPException(status_code=503, detail='model not loaded, please try again later')
    
    # list fature
    features_to_check = [
        "fixed_acidity",
        "volatile_acidity",
        "citric_acid",
        "residual_sugar",
        "chlorides",
        "free_sulfur_dioxide",
        "total_sulfur_dioxide",
        "density",
        "pH",
        "sulphates",
        "alcohol"
    ]

    # Validasi semua fitur: nilai harus > 0
    for feature in features_to_check:
        value = getattr(wine, feature)
        if value <= 0:
            logging.warning(f"Received invalid input: {feature} should be positive.")
            raise HTTPException(status_code=400, detail=f"{feature} should be a positive number")

    #extract the features from the incoming request
    features = np.array([
        [
            wine.fixed_acidity,
            wine.volatile_acidity,
            wine.citric_acid,
            wine.residual_sugar,
            wine.chlorides,
            wine.free_sulfur_dioxide,
            wine.total_sulfur_dioxide,
            wine.density,
            wine.pH,
            wine.sulphates,
            wine.alcohol
        ]
            
    ])
    #scale the input feature
    scaled_feature = scaler.transform(features)

    #prediction
    try:
        prediction = model.predict(scaled_feature)
        logging.info(f'Prediction for quality wine: {prediction[0]}')
    except Exception as e:
        logging.error(f'error during prediction: {e}')
        raise HTTPException(status_code=500, detail='Error during prediction')

    #return the prediction
    return {'predicted_quality': str(prediction[0])}

