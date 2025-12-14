from fastapi import FastAPI
from pydantic import BaseModel
from fastapi.middleware.cors import CORSMiddleware
import pickle


MODEL_PATH = "BestModel.pkl"


with open(MODEL_PATH, "rb") as f:
    model = pickle.load(f)

# FastAPI
app = FastAPI(title="Body Fat & Muscle Prediction API")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

class BodyMeasurements(BaseModel):
    Weight: float
    Height: float
    Chest: float
    Abdomen: float
    Hip: float
    Thigh: float
    Biceps: float


@app.post("/predict")
def predict(data: BodyMeasurements):
    
    BMI = round(data.Weight / (data.Height ** 2), 2)
    Waist_Hip_Ratio = data.Abdomen / data.Hip
    Chest_Height_Ratio = data.Chest / data.Height
    Thigh_Height_Ratio = data.Thigh / data.Height

    input_data = [[
        data.Weight, data.Height, data.Chest, data.Abdomen,
        data.Hip, data.Thigh, data.Biceps,
        BMI, Waist_Hip_Ratio, Chest_Height_Ratio, Thigh_Height_Ratio
    ]]

    bodyfat_prediction = round(model.predict(input_data)[0], 2)
    muscle_percentage = round(100 - bodyfat_prediction, 2)

    return {
        "Predicted_Body_Fat": bodyfat_prediction,
        "Estimated_Muscle": muscle_percentage
    }