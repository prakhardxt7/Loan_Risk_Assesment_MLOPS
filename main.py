# Importing Dependencies
from fastapi import FastAPI
from pydantic import BaseModel
import uvicorn
import joblib
import numpy as np
import pandas as pd
import sys
import os
from pathlib import Path

# Adding the below path to avoid module not found error
PACKAGE_ROOT = Path(os.path.abspath(os.path.dirname(__file__))).parent
sys.path.append(str(PACKAGE_ROOT))

# Import custom modules
from prediction_model.config import config 
from prediction_model.processing.data_handling import load_pipeline, load_dataset, separate_data

# Load the trained classification pipeline
classification_pipeline = load_pipeline(config.MODEL_NAME)

# Initialize FastAPI app
app = FastAPI()

# Define request model
class LoanPred(BaseModel):
    Dependents: int 
    Education: str 
    Self_Employed: str 
    TotalIncome: int  # 'income_annum'
    LoanAmount: int 
    Loan_Amount_Term: int  # 'loan_term'
    Credit_History: int  # 'cibil_score'
    Residential_Assets_Value: int 
    Commercial_Assets_Value: int
    Luxury_Assets_Value: int 
    Bank_Asset_Value: int 

# Root endpoint
@app.get("/")
def index():
    return {"message": "Welcome to Loan Prediction App"}

# Prediction endpoint
@app.post("/predict")
def predict_loan_status(loan_details: LoanPred):
    # Convert input data to dictionary
    data = loan_details.model_dump()

    # Transform input data to match model features
    new_data = {
        "no_of_dependents": data["Dependents"],
        "education": data["Education"],
        "self_employed": data["Self_Employed"],
        "income_annum": data["TotalIncome"],
        "loan_amount": data["LoanAmount"],
        "loan_term": data["Loan_Amount_Term"],
        "cibil_score": data["Credit_History"],
        "residential_assets_value": data["Residential_Assets_Value"],
        "commercial_assets_value": data["Commercial_Assets_Value"],
        "luxury_assets_value": data["Luxury_Assets_Value"],
        "bank_asset_value": data["Bank_Asset_Value"]
    }

    # Create DataFrame
    df = pd.DataFrame([new_data])

    # Make prediction
    prediction = classification_pipeline.predict(df)

    # Determine loan status
    pred = "Approved" if prediction[0] == 1 else "Rejected"

    return {"Status of Loan Application": pred}

# Run the application using `python main.py`
if __name__ == "__main__":
    uvicorn.run("main:app", host="127.0.0.1", port=8080, reload=True)
