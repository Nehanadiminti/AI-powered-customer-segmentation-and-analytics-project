import streamlit as st
import pandas as pd

from src.prediction_pipeline import predict_customer_segment
from src.recommendation_engine import generate_recommendations


# ============================================================
# PAGE CONFIGURATION
# ============================================================

st.set_page_config(
    page_title="CustoLens AI",
    page_icon="👥",
    layout="wide"
)


# ============================================================
# LOAD DATA
# ============================================================

DATA_PATH = "data/customer_segmented.csv"

df = pd.read_csv(DATA_PATH)


# ============================================================
# TITLE
# ============================================================

st.title("CustoLens AI")

st.subheader(
    "AI-Powered Customer Segmentation & Recommendation System"
)

st.write(
    "CustoLens AI analyzes customer behavior and divides customers "
    "into Premium, Regular, and Budget segments."
)


# ============================================================
# CUSTOMER OVERVIEW
# ============================================================

st.markdown("---")

st.header("📊 Customer Overview")

total_customers = len(df)

premium_count = (df["segment"] == "Premium").sum()
regular_count = (df["segment"] == "Regular").sum()
budget_count = (df["segment"] == "Budget").sum()


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

st.markdown("---")

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
    purchase_frequency = st.number_input(
        "Purchase Frequency",
        min_value=0.0,
        max_value=1.0,
        value=0.8,
        step=0.1
    )

    annual_spending = st.number_input(
        "Annual Spending (₹)",
        min_value=0.0,
        value=150000.0,
        step=1000.0
    )


# ============================================================
# PREDICT BUTTON
# ============================================================

if st.button(
    "🎯 Predict Customer Segment",
    use_container_width=True
):

    # --------------------------------------------------------
    # MODEL PREDICTION
    # --------------------------------------------------------

    result = predict_customer_segment(
        age=age,
        income=income,
        purchase_frequency=purchase_frequency,
        annual_spending=annual_spending
    )

    # --------------------------------------------------------
    # PREDICTION RESULT
    # --------------------------------------------------------

    st.markdown("---")

    st.subheader("Prediction Result")

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

    # --------------------------------------------------------
    # AI RECOMMENDATIONS
    # --------------------------------------------------------

    st.subheader("💡 Recommended Strategies")

    recommendations = generate_recommendations(result)

    # If recommendation engine returns a dictionary
    if isinstance(recommendations, dict):

        if "strategy" in recommendations:

            st.write(
                f"**Strategy:** {recommendations['strategy']}"
            )

        if "recommendations" in recommendations:

            for recommendation in recommendations["recommendations"]:

                st.write(
                    f"• {recommendation}"
                )

    # If recommendation engine returns a list
    elif isinstance(recommendations, list):

        for recommendation in recommendations:

            st.write(
                f"• {recommendation}"
            )

    # Otherwise display whatever was returned
    else:

        st.write(recommendations)

# ============================================================
# CUSTOMER DATA
# ============================================================

st.divider()

st.header("👥 Customer Data")

st.write(
    "Explore the customer dataset with their predicted segments."
)

# Load segmented customer dataset
customer_data = df

# Display dataset statistics
col1, col2, col3, col4 = st.columns(4)

col1.metric("Total Customers", len(customer_data))
col2.metric(
    "Premium Customers",
    (customer_data["segment"] == "Premium").sum()
)
col3.metric(
    "Regular Customers",
    (customer_data["segment"] == "Regular").sum()
)
col4.metric(
    "Budget Customers",
    (customer_data["segment"] == "Budget").sum()
)

st.subheader("Customer Records")

st.dataframe(
    customer_data,
    use_container_width=True,
    hide_index=True
)

# ============================================================
# CSV UPLOAD & BULK CUSTOMER PREDICTION
# ============================================================

st.divider()

st.header("📂 Upload Customer CSV")

st.write(
    "Upload a CSV file containing customer information to "
    "predict segments for multiple customers."
)

uploaded_file = st.file_uploader(
    "Choose a customer CSV file",
    type=["csv"]
)

if uploaded_file is not None:

    uploaded_df = pd.read_csv(uploaded_file)

    st.subheader("Uploaded Customer Data")

    st.dataframe(
        uploaded_df,
        use_container_width=True,
        hide_index=True
    )

    # --------------------------------------------------------
    # REQUIRED COLUMNS
    # --------------------------------------------------------

    required_columns = [
        "age",
        "income",
        "purchase_frequency",
        "annual_spending"
    ]

    missing_columns = [
        column
        for column in required_columns
        if column not in uploaded_df.columns
    ]

    # --------------------------------------------------------
    # VALIDATE COLUMNS
    # --------------------------------------------------------

    if missing_columns:

        st.error(
            "Missing required columns: "
            + ", ".join(missing_columns)
        )

    else:

        st.success(
            "CSV format is valid. All required columns are present."
        )

        # ----------------------------------------------------
        # PREDICT SEGMENTS
        # ----------------------------------------------------

        if st.button(
            "🔮 Predict Segments for Uploaded Customers",
            use_container_width=True
        ):

            predictions = []

            for _, customer in uploaded_df.iterrows():

                segment = predict_customer_segment(
                    age=customer["age"],
                    income=customer["income"],
                    purchase_frequency=customer["purchase_frequency"],
                    annual_spending=customer["annual_spending"]
                )

                predictions.append(segment)

            uploaded_df["predicted_segment"] = predictions

            # ------------------------------------------------
            # GENERATE STRATEGIES
            # ------------------------------------------------

            strategies = []

            for segment in predictions:

                recommendation_result = (
                    generate_recommendations(segment)
                )

                if isinstance(recommendation_result, dict):

                    strategies.append(
                        recommendation_result.get(
                            "strategy",
                            ""
                        )
                    )

                else:

                    strategies.append("General Customer Strategy")

            uploaded_df["strategy"] = strategies

            # ------------------------------------------------
            # DISPLAY RESULTS
            # ------------------------------------------------

            st.subheader(
                "🎯 Prediction Results"
            )

            st.dataframe(
                uploaded_df,
                use_container_width=True,
                hide_index=True
            )

            # ------------------------------------------------
            # SEGMENT SUMMARY
            # ------------------------------------------------

            st.subheader(
                "📊 Predicted Segment Summary"
            )

            prediction_counts = (
                uploaded_df["predicted_segment"]
                .value_counts()
                .reindex(
                    ["Premium", "Regular", "Budget"],
                    fill_value=0
                )
            )

            col1, col2, col3 = st.columns(3)

            with col1:
                st.metric(
                    "Premium",
                    prediction_counts["Premium"]
                )

            with col2:
                st.metric(
                    "Regular",
                    prediction_counts["Regular"]
                )

            with col3:
                st.metric(
                    "Budget",
                    prediction_counts["Budget"]
                )

            # ------------------------------------------------
            # DOWNLOAD RESULTS
            # ------------------------------------------------

            csv_output = uploaded_df.to_csv(
                index=False
            )

            st.download_button(
                label="⬇️ Download Prediction Results",
                data=csv_output,
                file_name="customer_segment_predictions.csv",
                mime="text/csv"
            )

# ============================================================
# DATA VISUALIZATIONS
# ============================================================

st.divider()

st.header("📈 Customer Analytics & Visualizations")

st.write(
    "Visual insights into customer segments, spending behavior, "
    "income, and purchase frequency."
)

# ------------------------------------------------------------
# SEGMENT DISTRIBUTION
# ------------------------------------------------------------

st.subheader("📊 Customer Segment Distribution")

segment_counts = customer_data["segment"].value_counts()

st.bar_chart(
    segment_counts,
    x_label="Customer Segment",
    y_label="Number of Customers"
)


# ------------------------------------------------------------
# AVERAGE SPENDING BY SEGMENT
# ------------------------------------------------------------

st.subheader("💰 Average Annual Spending by Segment")

average_spending = (
    customer_data
    .groupby("segment")["annual_spending"]
    .mean()
    .round(2)
)

st.bar_chart(
    average_spending,
    x_label="Customer Segment",
    y_label="Average Annual Spending"
)


# ------------------------------------------------------------
# AVERAGE INCOME BY SEGMENT
# ------------------------------------------------------------

st.subheader("💵 Average Income by Segment")

average_income = (
    customer_data
    .groupby("segment")["income"]
    .mean()
    .round(2)
)

st.bar_chart(
    average_income,
    x_label="Customer Segment",
    y_label="Average Income"
)


# ------------------------------------------------------------
# PURCHASE FREQUENCY BY SEGMENT
# ------------------------------------------------------------

st.subheader("🛒 Average Purchase Frequency by Segment")

average_frequency = (
    customer_data
    .groupby("segment")["purchase_frequency"]
    .mean()
    .round(2)
)

st.bar_chart(
    average_frequency,
    x_label="Customer Segment",
    y_label="Purchase Frequency"
)


# ------------------------------------------------------------
# INCOME VS ANNUAL SPENDING
# ------------------------------------------------------------

st.subheader("📌 Income vs Annual Spending")

st.scatter_chart(
    customer_data,
    x="income",
    y="annual_spending"
)


# ------------------------------------------------------------
# SEGMENT SUMMARY
# ------------------------------------------------------------

st.subheader("📋 Segment Performance Summary")

segment_summary = (
    customer_data
    .groupby("segment")
    .agg(
        Customers=("name", "count"),
        Average_Income=("income", "mean"),
        Average_Spending=("annual_spending", "mean"),
        Average_Purchase_Frequency=("purchase_frequency", "mean")
    )
    .round(2)
)

st.dataframe(
    segment_summary,
    use_container_width=True
)