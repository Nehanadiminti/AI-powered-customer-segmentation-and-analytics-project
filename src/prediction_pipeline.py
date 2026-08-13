import os
import joblib
import pandas as pd

from src.recommendation_engine import generate_recommendations


# --------------------------------------------------
# MODEL PATH
# --------------------------------------------------

MODEL_PATH = os.path.join(
    os.path.dirname(__file__),
    "..",
    "data",
    "customer_segmentation_model.pkl"
)


# --------------------------------------------------
# LOAD MODEL
# --------------------------------------------------

model = joblib.load(MODEL_PATH)


# --------------------------------------------------
# PREDICT CUSTOMER SEGMENT
# --------------------------------------------------

def predict_customer_segment(
    age,
    income,
    purchase_frequency,
    annual_spending
):

    customer = pd.DataFrame({
        "age": [age],
        "income": [income],
        "purchase_frequency": [purchase_frequency],
        "annual_spending": [annual_spending]
    })

    prediction = model.predict(customer)

    segment = prediction[0]

    return segment


# --------------------------------------------------
# COMPLETE CUSTOMER ANALYSIS
# --------------------------------------------------

def analyze_customer(
    age,
    income,
    purchase_frequency,
    annual_spending
):

    segment = predict_customer_segment(
        age,
        income,
        purchase_frequency,
        annual_spending
    )

    recommendation_result = generate_recommendations(segment)

    return {
        "segment": segment,
        "strategy": recommendation_result["strategy"],
        "recommendations": recommendation_result["recommendations"]
    }