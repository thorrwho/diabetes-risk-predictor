from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel, Field
import joblib
import numpy as np

app = FastAPI(title="Diabetes Risk Predictor API")

app.add_middleware(CORSMiddleware, allow_origins=["*"], allow_methods=["*"], allow_headers=["*"])

model  = joblib.load("model/rf_model.joblib")
scaler = joblib.load("model/scaler.joblib")

class PatientData(BaseModel):
    pregnancies:       int   = Field(..., example=2)
    glucose:           float = Field(..., example=120)
    blood_pressure:    float = Field(..., example=70)
    skin_thickness:    float = Field(..., example=20)
    insulin:           float = Field(..., example=80)
    bmi:               float = Field(..., example=25.0)
    diabetes_pedigree: float = Field(..., example=0.5)
    age:               int   = Field(..., example=30)

@app.get("/")
def root():
    return {"status": "healthy", "message": "Diabetes Risk Predictor API is running"}

@app.post("/predict")
def predict(data: PatientData):
    try:
        features = np.array([[
            data.pregnancies, data.glucose, data.blood_pressure,
            data.skin_thickness, data.insulin, data.bmi,
            data.diabetes_pedigree, data.age
        ]])
        features_scaled = scaler.transform(features)
        prediction      = model.predict(features_scaled)[0]
        probability     = model.predict_proba(features_scaled)[0][1]
        risk_label      = "High Risk" if prediction == 1 else "Low Risk"
        advice = "Please consult a doctor." if prediction == 1 else "Maintain a healthy lifestyle."
        return {
            "risk_label": risk_label,
            "risk_probability": round(float(probability), 4),
            "advice": advice
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
