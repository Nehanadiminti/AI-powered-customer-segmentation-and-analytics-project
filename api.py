from fastapi import FastAPI, UploadFile, File, HTTPException
from pydantic import BaseModel
import pandas as pd
import io

from src.prediction_pipeline import predict_customer_segment
from src.recommendation_engine import generate_recommendations
from src.data_adapter import prepare_customer_data


# ============================================================
# CREATE FASTAPI APPLICATION
# ============================================================

app = FastAPI(
    title="CustoLens AI API",
    description=(
        "AI-powered customer segmentation and "
        "recommendation API"
    ),
    version="1.0.0"
)


# ============================================================
# REQUEST MODEL
# ============================================================

class CustomerInput(BaseModel):

    age: float
    income: float
    annual_spending: float


# ============================================================
# ROOT ENDPOINT
# ============================================================

@app.get("/")
def root():

    return {
        "message": "CustoLens AI API is running",
        "version": "1.0.0"
    }


# ============================================================
# HEALTH CHECK
# ============================================================

@app.get("/health")
def health_check():

    return {
        "status": "healthy",
        "service": "CustoLens AI"
    }


# ============================================================
# SINGLE CUSTOMER PREDICTION
# ============================================================

@app.post("/predict")
def predict_customer(
    customer: CustomerInput
):

    try:

        # ----------------------------------------------------
        # Purchase frequency is hidden from the API user,
        # just as it is hidden from the Streamlit UI.
        # ----------------------------------------------------

        purchase_frequency = 0.5


        # ----------------------------------------------------
        # MODEL PREDICTION
        # ----------------------------------------------------

        segment = predict_customer_segment(

            age=customer.age,

            income=customer.income,

            purchase_frequency=purchase_frequency,

            annual_spending=customer.annual_spending
        )


        # ----------------------------------------------------
        # RECOMMENDATIONS
        # ----------------------------------------------------

        recommendations = (
            generate_recommendations(
                segment
            )
        )


        return {

            "predicted_segment": segment,

            "recommendations": recommendations
        }


    except Exception as error:

        raise HTTPException(

            status_code=500,

            detail=str(error)
        )


# ============================================================
# CSV PREDICTION
# ============================================================

@app.post("/predict-csv")
async def predict_csv(
    file: UploadFile = File(...)
):

    try:

        # ----------------------------------------------------
        # CHECK FILE TYPE
        # ----------------------------------------------------

        if not file.filename.lower().endswith(
            ".csv"
        ):

            raise HTTPException(

                status_code=400,

                detail="Please upload a CSV file."
            )


        # ----------------------------------------------------
        # READ CSV
        # ----------------------------------------------------

        contents = await file.read()

        uploaded_df = pd.read_csv(
            io.BytesIO(contents)
        )


        # ----------------------------------------------------
        # PREPARE CUSTOMER DATA
        # ----------------------------------------------------

        prepared_df, mapping, missing_columns = (
            prepare_customer_data(
                uploaded_df
            )
        )


        # ----------------------------------------------------
        # VALIDATION
        # ----------------------------------------------------

        if missing_columns:

            raise HTTPException(

                status_code=400,

                detail={
                    "message": (
                        "Required customer information "
                        "could not be identified."
                    ),

                    "missing_columns": missing_columns
                }
            )


        # ----------------------------------------------------
        # PREDICT CUSTOMERS
        # ----------------------------------------------------

        predictions = []


        for _, row in prepared_df.iterrows():

            prediction = predict_customer_segment(

                age=row["age"],

                income=row["income"],

                purchase_frequency=(
                    row["purchase_frequency"]
                ),

                annual_spending=(
                    row["annual_spending"]
                )
            )

            predictions.append(
                prediction
            )


        # ----------------------------------------------------
        # CREATE RESULTS
        # ----------------------------------------------------

        result_df = uploaded_df.copy()

        result_df[
            "predicted_segment"
        ] = predictions


        # ----------------------------------------------------
        # GENERATE RECOMMENDATIONS
        # ----------------------------------------------------

        recommendations = []


        for segment in predictions:

            recommendation = (
                generate_recommendations(
                    segment
                )
            )

            recommendations.append(
                recommendation
            )


        # ----------------------------------------------------
        # SUMMARY
        # ----------------------------------------------------

        summary = {

            "Premium": predictions.count(
                "Premium"
            ),

            "Regular": predictions.count(
                "Regular"
            ),

            "Budget": predictions.count(
                "Budget"
            )
        }


        # ----------------------------------------------------
        # RETURN RESPONSE
        # ----------------------------------------------------

        return {

            "filename": file.filename,

            "total_customers": len(
                result_df
            ),

            "segment_summary": summary,

            "predictions": result_df.to_dict(
                orient="records"
            ),

            "recommendations": recommendations
        }


    except HTTPException:

        raise


    except Exception as error:

        raise HTTPException(

            status_code=500,

            detail=str(error)
        )