from fastapi import FastAPI
from pydantic import BaseModel
import pickle
import numpy as np

# Load model
with open("model.pkl", "rb") as f:
    model = pickle.load(f)

app = FastAPI()

# Schema input
class IrisFeatures(BaseModel):
    sepal_length: float
    sepal_width: float
    petal_length: float
    petal_width: float

class_name = ['sentosa', 'versicolor', 'verginica']

@app.post("/predict")
def predict(features: IrisFeatures):
    data = np.array([[features.sepal_length, features.sepal_width, features.petal_length, features.petal_width]])
    prediction = model.predict(data)[0]
    predicted_class = class_name[prediction]

    if hasattr(model, 'predict_proba'):
        probabilities = model.predict_proba(data)[0]
        confidence = round(np.max(probabilities)* 100, 2) #mengambil probabilitas tertinggi

    else :
        confidence = None

    return {
        "prediction": predicted_class,
        "confidence": confidence
    }
