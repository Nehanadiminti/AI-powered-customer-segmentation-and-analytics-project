import streamlit as st
import pandas as pd

from src.prediction_pipeline import predict_customer_segment
from src.recommendation_engine import generate_recommendations
from src.data_adapter import prepare_customer_data


# ============================================================
# PAGE CONFIGURATION
# ============================================================

st.set_page_config(
    page_title="CustoLens AI",
    page_icon="👥",
    layout="wide"
)


# ============================================================
# LOAD TRAINED CUSTOMER DATA
# ============================================================

DATA_PATH = "data/customer_segmented.csv"

df = pd.read_csv(DATA_PATH)

customer_data = df


# ============================================================
# TITLE
# ============================================================

st.title("CustoLens AI")

st.subheader(
    "AI-Powered Customer Segmentation & Recommendation System"
)

st.write(
    "CustoLens AI analyzes customer behavior, identifies customer "
    "segments, and generates AI-powered marketing recommendations."
)


# ============================================================
# CUSTOMER OVERVIEW
# ============================================================

st.divider()

st.header("📊 Customer Overview")

total_customers = len(df)

premium_count = (
    df["segment"] == "Premium"
).sum()

regular_count = (
    df["segment"] == "Regular"
).sum()

budget_count = (
    df["segment"] == "Budget"
).sum()


col1, col2, col3, col4 = st.columns(4)


with col1:

    st.metric(
        "Total Customers",
        total_customers
    )


with col2:

    st.metric(
        "Premium Customers",
        premium_count
    )


with col3:

    st.metric(
        "Regular Customers",
        regular_count
    )


with col4:

    st.metric(
        "Budget Customers",
        budget_count
    )


# ============================================================
# INDIVIDUAL CUSTOMER PREDICTION
# ============================================================

st.divider()

st.header("🔮 Individual Customer Prediction")

st.write(
    "Enter customer information to predict the customer segment "
    "and generate personalized recommendations."
)


col1, col2 = st.columns(2)


with col1:

    age = st.number_input(
        "Age",
        min_value=18,
        max_value=100,
        value=30,
        step=1
    )

    income = st.number_input(
        "Annual Income (₹)",
        min_value=0.0,
        value=120000.0,
        step=1000.0
    )


with col2:

    annual_spending = st.number_input(
        "Annual Spending (₹)",
        min_value=0.0,
        value=150000.0,
        step=1000.0
    )


# ============================================================
# PURCHASE FREQUENCY
# ============================================================
# Purchase frequency is no longer entered manually.
# The median value from the trained customer dataset is
# used internally for individual prediction.
# ============================================================

purchase_frequency = float(
    df["purchase_frequency"].median()
)


# ============================================================
# INDIVIDUAL PREDICTION
# ============================================================

if st.button(
    "🎯 Predict Customer Segment",
    use_container_width=True
):

    result = predict_customer_segment(

        age=age,

        income=income,

        purchase_frequency=purchase_frequency,

        annual_spending=annual_spending
    )


    st.divider()

    st.subheader("Prediction Result")


    # --------------------------------------------------------
    # DISPLAY SEGMENT
    # --------------------------------------------------------

    if result == "Premium":

        st.success(
            "⭐ Predicted Customer Segment: PREMIUM"
        )

    elif result == "Regular":

        st.info(
            "🔵 Predicted Customer Segment: REGULAR"
        )

    elif result == "Budget":

        st.warning(
            "🟡 Predicted Customer Segment: BUDGET"
        )

    else:

        st.write(
            f"Predicted Customer Segment: {result}"
        )


    # ========================================================
    # RECOMMENDATIONS
    # ========================================================

    st.subheader("💡 Recommended Strategies")

    recommendations = generate_recommendations(
        result
    )


    if isinstance(
        recommendations,
        dict
    ):

        if "strategy" in recommendations:

            st.write(
                f"**Strategy:** "
                f"{recommendations['strategy']}"
            )


        if "recommendations" in recommendations:

            for recommendation in recommendations[
                "recommendations"
            ]:

                st.write(
                    f"• {recommendation}"
                )


    elif isinstance(
        recommendations,
        list
    ):

        for recommendation in recommendations:

            st.write(
                f"• {recommendation}"
            )


    else:

        st.write(
            recommendations
        )


# ============================================================
# CSV UPLOAD & BATCH PREDICTION
# ============================================================

st.divider()

st.header("📂 Upload Customer CSV")

st.write(
    "Upload a customer CSV file. CustoLens AI automatically "
    "recognizes supported customer attributes, prepares the "
    "data, predicts customer segments, and generates "
    "personalized recommendations."
)


uploaded_file = st.file_uploader(
    "Choose a customer CSV file",
    type=["csv"]
)


if uploaded_file is not None:

    # ========================================================
    # 1. READ CSV
    # ========================================================

    uploaded_df = pd.read_csv(
        uploaded_file
    )


    # ========================================================
    # 2. VALIDATE & PREPARE DATA
    # ========================================================
    #
    # Column recognition and unit conversion happen internally.
    # No mapping information is displayed to the user.
    # ========================================================

    prepared_df, column_mapping, missing_columns = (
        prepare_customer_data(
            uploaded_df
        )
    )


    # ========================================================
    # 3. VALIDATION RESULT
    # ========================================================

    if missing_columns:

        st.error(
            "❌ CustoLens AI could not identify the required "
            "customer information."
        )

        st.info(
            "The uploaded CSV must contain information "
            "equivalent to age, income, purchase frequency, "
            "and spending."
        )


    else:

        st.success(
            "✅ Customer CSV successfully recognized."
        )


        # ====================================================
        # ANALYZE CUSTOMERS
        # ====================================================

        if st.button(
            "🚀 Analyze Customers",
            use_container_width=True
        ):

            # =================================================
            # 4. PREDICT EVERY CUSTOMER
            # =================================================

            predictions = []

            total_rows = len(
                prepared_df
            )

            progress_bar = st.progress(
                0
            )

            status_text = st.empty()


            for position, (_, row) in enumerate(
                prepared_df.iterrows(),
                start=1
            ):

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


                # ------------------------------------------------
                # UPDATE PROGRESS
                # ------------------------------------------------

                progress_bar.progress(
                    position / total_rows
                )

                status_text.write(
                    f"Analyzing customer "
                    f"{position} of {total_rows}..."
                )


            # =================================================
            # 5. CREATE FINAL RESULT
            # =================================================

            result_df = uploaded_df.copy()


            result_df[
                "predicted_segment"
            ] = predictions


            # =================================================
            # 6. GENERATE RECOMMENDATIONS
            # =================================================
            #
            # Recommendations are generated internally.
            #
            # They are intentionally NOT added to result_df.
            # Therefore, the final CSV does not contain a
            # recommendations column.
            # =================================================

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


            # =================================================
            # 7. CLEAR PROGRESS
            # =================================================

            progress_bar.empty()

            status_text.empty()


            # =================================================
            # 8. DISPLAY RESULTS
            # =================================================

            st.success(
                "✅ Customer analysis completed successfully!"
            )


            st.subheader(
                "📋 Customer Analysis Results"
            )


            st.dataframe(
                result_df,
                use_container_width=True,
                hide_index=True
            )


            # =================================================
            # 9. PREDICTION SUMMARY
            # =================================================

            st.subheader(
                "📊 Prediction Summary"
            )


            result_counts = (
                result_df[
                    "predicted_segment"
                ]
                .value_counts()
            )


            col1, col2, col3 = st.columns(3)


            with col1:

                st.metric(
                    "⭐ Premium",
                    result_counts.get(
                        "Premium",
                        0
                    )
                )


            with col2:

                st.metric(
                    "🔵 Regular",
                    result_counts.get(
                        "Regular",
                        0
                    )
                )


            with col3:

                st.metric(
                    "🟡 Budget",
                    result_counts.get(
                        "Budget",
                        0
                    )
                )


            # =================================================
            # 10. DOWNLOAD RESULTS
            # =================================================

            st.subheader(
                "⬇️ Download Results"
            )


            csv_output = result_df.to_csv(
                index=False
            )


            st.download_button(

                label="⬇️ Download Prediction Results",

                data=csv_output,

                file_name=(
                    "customer_segment_predictions.csv"
                ),

                mime="text/csv",

                use_container_width=True
            )


# ============================================================
# DATA VISUALIZATIONS
# ============================================================

st.divider()

st.header(
    "📈 Customer Analytics & Visualizations"
)

st.write(
    "Visual insights into customer segments, spending behavior, "
    "income, and purchase frequency."
)


# ============================================================
# SEGMENT DISTRIBUTION
# ============================================================

st.subheader(
    "📊 Customer Segment Distribution"
)


segment_counts = (
    customer_data["segment"]
    .value_counts()
    .reindex(
        [
            "Premium",
            "Regular",
            "Budget"
        ]
    )
    .fillna(0)
)


st.bar_chart(

    segment_counts,

    x_label="Customer Segment",

    y_label="Number of Customers"
)


# ============================================================
# AVERAGE SPENDING BY SEGMENT
# ============================================================

st.subheader(
    "💰 Average Annual Spending by Segment"
)


average_spending = (
    customer_data
    .groupby("segment")[
        "annual_spending"
    ]
    .mean()
    .reindex(
        [
            "Premium",
            "Regular",
            "Budget"
        ]
    )
    .round(2)
)


st.bar_chart(

    average_spending,

    x_label="Customer Segment",

    y_label="Average Annual Spending"
)


# ============================================================
# AVERAGE INCOME BY SEGMENT
# ============================================================

st.subheader(
    "💵 Average Income by Segment"
)


average_income = (
    customer_data
    .groupby("segment")[
        "income"
    ]
    .mean()
    .reindex(
        [
            "Premium",
            "Regular",
            "Budget"
        ]
    )
    .round(2)
)


st.bar_chart(

    average_income,

    x_label="Customer Segment",

    y_label="Average Income"
)


# ============================================================
# PURCHASE FREQUENCY
# ============================================================

st.subheader(
    "🛒 Average Purchase Frequency by Segment"
)


average_frequency = (
    customer_data
    .groupby("segment")[
        "purchase_frequency"
    ]
    .mean()
    .reindex(
        [
            "Premium",
            "Regular",
            "Budget"
        ]
    )
    .round(2)
)


st.bar_chart(

    average_frequency,

    x_label="Customer Segment",

    y_label="Purchase Frequency"
)


# ============================================================
# INCOME VS ANNUAL SPENDING
# ============================================================

st.subheader(
    "📌 Income vs Annual Spending"
)


st.scatter_chart(

    customer_data,

    x="income",

    y="annual_spending"
)


# ============================================================
# SEGMENT PERFORMANCE SUMMARY
# ============================================================

st.subheader(
    "📋 Segment Performance Summary"
)


segment_summary = (
    customer_data
    .groupby("segment")
    .agg(

        Customers=(
            "name",
            "count"
        ),

        Average_Income=(
            "income",
            "mean"
        ),

        Average_Spending=(
            "annual_spending",
            "mean"
        ),

        Average_Purchase_Frequency=(
            "purchase_frequency",
            "mean"
        )
    )
    .reindex(
        [
            "Premium",
            "Regular",
            "Budget"
        ]
    )
    .round(2)
)


st.dataframe(
    segment_summary,
    use_container_width=True
)


# ============================================================
# FOOTER
# ============================================================

st.divider()

st.caption(
    "CustoLens AI • AI-Powered Customer Segmentation "
    "& Recommendation System"
)