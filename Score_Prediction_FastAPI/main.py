from fastapi import FastAPI
from pydantic import BaseModel
import numpy as np
import pandas as pd
import joblib


#load model dan scaler
model = None
scaler = None

#initialize fastapi app
app= FastAPI()

#Preload the Model for Latency Reduction
@app.on_event('startup')
async def load_model():
    global model, scaler
    model = joblib.load('lr_model.pkl')
    scaler = joblib.load('scaler.pkl')

#define the request model for the input
class Prediction_request(BaseModel):
    Hours_studied: float

# home endpoint
@app.get('/')
async def home():
    return {'message': 'Welcome to score prediction'}

#prediction endpoint
@app.post('/predict')
def predict(request: Prediction_request):
    try:
        hours = request.Hours_studied
        data = pd.DataFrame([[hours]], columns=['Hours_studied'])
        scaled_data = scaler.transform(data)
        predictions = model.predict(scaled_data)
        return {'predicted_test_score': float(predictions[0])}
    
    except Exception as e:
        return {'error': str(e)}
