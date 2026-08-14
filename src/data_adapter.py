import pandas as pd
import re


# ============================================================
# NORMALIZE COLUMN NAME
# ============================================================

def normalize_column_name(column):
    """
    Convert different column-name formats into a standard format.

    Examples:
        Annual Income (₹)      -> annual_income
        Income_LPA             -> income_lpa
        Purchase Frequency     -> purchase_frequency
        Purchase Amount       -> purchase_amount
    """

    column = str(column).strip().lower()

    # Remove currency symbols
    column = re.sub(r"[₹$€£]", "", column)

    # Replace spaces and special characters with underscores
    column = re.sub(r"[^a-z0-9]+", "_", column)

    # Remove leading/trailing underscores
    column = column.strip("_")

    return column


# ============================================================
# COLUMN ALIASES
# ============================================================

COLUMN_ALIASES = {

    # --------------------------------------------------------
    # AGE
    # --------------------------------------------------------

    "age": [
        "age",
        "age_years",
        "customer_age",
        "customer_age_years",
        "years_old",
        "years"
    ],


    # --------------------------------------------------------
    # INCOME - RUPEES
    # --------------------------------------------------------

    "income": [
        "income",
        "annual_income",
        "yearly_income",
        "salary",
        "annual_salary",
        "yearly_salary",
        "income_rupees",
        "income_rs",
        "income_inr",
        "income_in_rupees",
        "annual_income_rupees",
        "annual_income_rs",
        "annual_income_inr",
        "earnings",
        "annual_earnings"
    ],


    # --------------------------------------------------------
    # INCOME - LPA / LAKHS
    # --------------------------------------------------------

    "income_lpa": [
        "income_lpa",
        "annual_income_lpa",
        "salary_lpa",
        "income_lakh",
        "income_lakhs",
        "annual_income_lakh",
        "annual_income_lakhs",
        "income_in_lakhs",
        "income_lakh_per_annum"
    ],


    # --------------------------------------------------------
    # MONTHLY INCOME
    # --------------------------------------------------------

    "monthly_income": [
        "monthly_income",
        "monthly_salary",
        "income_per_month",
        "salary_per_month",
        "monthly_earnings"
    ],


    # --------------------------------------------------------
    # ANNUAL SPENDING - RUPEES
    # --------------------------------------------------------

    "annual_spending": [
        "annual_spending",
        "yearly_spending",
        "annual_expense",
        "yearly_expense",
        "total_annual_spending",
        "spending",
        "spending_rupees",
        "spending_inr",
        "spending_rs",
        "spending_in_rupees",
        "annual_spending_rupees",
        "annual_spending_rs",
        "annual_spending_inr",
        "annual_expenditure",
        "yearly_expenditure",
        "total_spending"
    ],


    # --------------------------------------------------------
    # ANNUAL SPENDING - LAKHS
    # --------------------------------------------------------

    "annual_spending_lakh": [
        "annual_spending_lakh",
        "annual_spending_lakhs",
        "annual_spending_lakh_rupees",
        "spending_lakh",
        "spending_lakhs",
        "annual_expense_lakh",
        "annual_expense_lakhs",
        "annual_spending_in_lakhs",
        "spending_in_lakhs",
        "annual_expenditure_lakh",
        "annual_expenditure_lakhs"
    ],


    # --------------------------------------------------------
    # MONTHLY SPENDING
    # --------------------------------------------------------

    "monthly_spending": [
        "monthly_spending",
        "monthly_expense",
        "spending_per_month",
        "expense_per_month",
        "monthly_expenditure",
        "monthly_expenses"
    ],


    # --------------------------------------------------------
    # PURCHASE FREQUENCY
    # --------------------------------------------------------

    "purchase_frequency": [
        "purchase_frequency",
        "purchase_freq",
        "frequency",
        "buying_frequency",
        "customer_purchase_frequency",
        "purchase_rate",
        "purchase_ratio",
        "purchase_frequency_score"
    ],


    # --------------------------------------------------------
    # PURCHASE FREQUENCY - PERCENTAGE
    # --------------------------------------------------------

    "purchase_frequency_percent": [
        "purchase_frequency_percent",
        "purchase_frequency_percentage",
        "purchase_freq_percent",
        "purchase_freq_percentage",
        "frequency_percent",
        "frequency_percentage",
        "purchase_rate_percent",
        "purchase_rate_percentage"
    ],


    # --------------------------------------------------------
    # PURCHASE COUNT
    # --------------------------------------------------------

    "purchase_count": [
        "purchase_count",
        "purchases",
        "number_of_purchases",
        "num_purchases",
        "annual_purchase_count",
        "yearly_purchase_count",
        "purchases_per_year",
        "purchases_yearly",
        "purchase_number",
        "total_purchases"
    ],


    # --------------------------------------------------------
    # PURCHASE AMOUNT
    # --------------------------------------------------------

    "purchase_amount": [
        "purchase_amount",
        "total_purchase_amount",
        "purchase_value",
        "transaction_amount",
        "transaction_value",
        "amount_per_purchase",
        "average_purchase_amount",
        "average_transaction_amount"
    ]
}


# ============================================================
# FIND COLUMN
# ============================================================

def find_column(df, aliases):

    normalized_columns = {
        normalize_column_name(column): column
        for column in df.columns
    }

    for alias in aliases:

        alias_normalized = normalize_column_name(alias)

        if alias_normalized in normalized_columns:

            return normalized_columns[alias_normalized]

    return None


# ============================================================
# CLEAN NUMERIC VALUES
# ============================================================

def clean_numeric(series):
    """
    Convert formatted numeric values into numbers.

    Examples:
        ₹82,468 -> 82468
        $50,000 -> 50000
        82.5    -> 82.5
    """

    return pd.to_numeric(
        series.astype(str)
        .str.replace(",", "", regex=False)
        .str.replace("₹", "", regex=False)
        .str.replace("$", "", regex=False)
        .str.replace("€", "", regex=False)
        .str.replace("£", "", regex=False)
        .str.strip(),
        errors="coerce"
    )


# ============================================================
# PREPARE CUSTOMER DATA
# ============================================================

def prepare_customer_data(df):

    # --------------------------------------------------------
    # COPY ORIGINAL DATA
    # --------------------------------------------------------

    df = df.copy()


    # --------------------------------------------------------
    # NORMALIZE COLUMN NAMES
    # --------------------------------------------------------

    df.columns = [
        normalize_column_name(column)
        for column in df.columns
    ]


    # Model-ready dataframe
    result = pd.DataFrame(
        index=df.index
    )


    # Mapping information
    mapping = {}


    # ========================================================
    # AGE
    # ========================================================

    age_col = find_column(
        df,
        COLUMN_ALIASES["age"]
    )

    if age_col:

        result["age"] = clean_numeric(
            df[age_col]
        )

        mapping["age"] = age_col


    # ========================================================
    # INCOME
    # ========================================================

    income_col = find_column(
        df,
        COLUMN_ALIASES["income"]
    )

    income_lpa_col = find_column(
        df,
        COLUMN_ALIASES["income_lpa"]
    )

    monthly_income_col = find_column(
        df,
        COLUMN_ALIASES["monthly_income"]
    )


    # --------------------------------------------------------
    # Income already in rupees
    # --------------------------------------------------------

    if income_col:

        result["income"] = clean_numeric(
            df[income_col]
        )

        mapping["income"] = income_col


    # --------------------------------------------------------
    # Income in LPA
    # --------------------------------------------------------

    elif income_lpa_col:

        result["income"] = (
            clean_numeric(
                df[income_lpa_col]
            ) * 100000
        )

        mapping["income"] = (
            f"{income_lpa_col} → converted from LPA"
        )


    # --------------------------------------------------------
    # Monthly income
    # --------------------------------------------------------

    elif monthly_income_col:

        result["income"] = (
            clean_numeric(
                df[monthly_income_col]
            ) * 12
        )

        mapping["income"] = (
            f"{monthly_income_col} → converted from monthly income"
        )


    # ========================================================
    # PURCHASE FREQUENCY - GET RAW VALUE FIRST
    # ========================================================

    frequency_col = find_column(
        df,
        COLUMN_ALIASES["purchase_frequency"]
    )

    frequency_percent_col = find_column(
        df,
        COLUMN_ALIASES["purchase_frequency_percent"]
    )

    purchase_count_col = find_column(
        df,
        COLUMN_ALIASES["purchase_count"]
    )


    # --------------------------------------------------------
    # Raw frequency for annual-spending calculation
    # --------------------------------------------------------

    raw_frequency = None


    if purchase_count_col:

        raw_frequency = clean_numeric(
            df[purchase_count_col]
        )

        mapping["frequency_source"] = (
            purchase_count_col
        )


    elif frequency_col:

        raw_frequency = clean_numeric(
            df[frequency_col]
        )

        mapping["frequency_source"] = (
            frequency_col
        )


    elif frequency_percent_col:

        raw_frequency = (
            clean_numeric(
                df[frequency_percent_col]
            ) / 100
        )

        mapping["frequency_source"] = (
            frequency_percent_col
        )


    # ========================================================
    # ANNUAL SPENDING
    # ========================================================

    annual_spending_col = find_column(
        df,
        COLUMN_ALIASES["annual_spending"]
    )

    annual_spending_lakh_col = find_column(
        df,
        COLUMN_ALIASES["annual_spending_lakh"]
    )

    monthly_spending_col = find_column(
        df,
        COLUMN_ALIASES["monthly_spending"]
    )

    purchase_amount_col = find_column(
        df,
        COLUMN_ALIASES["purchase_amount"]
    )


    # --------------------------------------------------------
    # Case 1: Annual spending already provided
    # --------------------------------------------------------

    if annual_spending_col:

        result["annual_spending"] = clean_numeric(
            df[annual_spending_col]
        )

        mapping["annual_spending"] = (
            annual_spending_col
        )


    # --------------------------------------------------------
    # Case 2: Annual spending in lakhs
    # --------------------------------------------------------

    elif annual_spending_lakh_col:

        result["annual_spending"] = (
            clean_numeric(
                df[annual_spending_lakh_col]
            ) * 100000
        )

        mapping["annual_spending"] = (
            f"{annual_spending_lakh_col} → converted from lakhs"
        )


    # --------------------------------------------------------
    # Case 3: Monthly spending
    # --------------------------------------------------------

    elif monthly_spending_col:

        result["annual_spending"] = (
            clean_numeric(
                df[monthly_spending_col]
            ) * 12
        )

        mapping["annual_spending"] = (
            f"{monthly_spending_col} → converted from monthly spending"
        )


    # --------------------------------------------------------
    # Case 4: Purchase amount × purchase frequency
    # --------------------------------------------------------

    elif purchase_amount_col:

        purchase_amount = clean_numeric(
            df[purchase_amount_col]
        )


        if raw_frequency is not None:

            # IMPORTANT:
            #
            # purchase_amount = amount per transaction
            # raw_frequency = purchases per year
            #
            # Therefore:
            #
            # annual_spending =
            # purchase_amount × purchase_frequency

            result["annual_spending"] = (
                purchase_amount
                * raw_frequency
            )

            mapping["annual_spending"] = (
                f"{purchase_amount_col} × "
                f"{mapping['frequency_source']} "
                f"→ annual spending"
            )


        else:

            # Cannot calculate annual spending without
            # purchase frequency.

            result["annual_spending"] = pd.NA

            mapping["annual_spending"] = (
                f"{purchase_amount_col} requires "
                "purchase frequency"
            )


    # ========================================================
    # CONVERT PURCHASE FREQUENCY TO MODEL FORMAT
    # ========================================================

    if raw_frequency is not None:

        frequency_values = raw_frequency.copy()

        max_frequency = frequency_values.max()


        # ----------------------------------------------------
        # Percentage input
        # ----------------------------------------------------

        if frequency_percent_col:

            result["purchase_frequency"] = (
                frequency_values
            )

            mapping["purchase_frequency"] = (
                f"{frequency_percent_col} → "
                "converted from percentage"
            )


        # ----------------------------------------------------
        # Frequency already between 0 and 1
        # ----------------------------------------------------

        elif (
            pd.notna(max_frequency)
            and max_frequency <= 1
        ):

            result["purchase_frequency"] = (
                frequency_values
            )

            mapping["purchase_frequency"] = (
                mapping["frequency_source"]
            )


        # ----------------------------------------------------
        # Frequency is a purchase count
        #
        # Example:
        # 18 → 0.82
        # 12 → 0.55
        # 22 → 1.00
        # ----------------------------------------------------

        else:

            if (
                pd.notna(max_frequency)
                and max_frequency > 0
            ):

                result["purchase_frequency"] = (
                    frequency_values
                    / max_frequency
                )

            else:

                result["purchase_frequency"] = (
                    frequency_values
                )


            mapping["purchase_frequency"] = (
                f"{mapping['frequency_source']} → "
                "normalized to 0–1"
            )


    # ========================================================
    # VALIDATION
    # ========================================================

    required_columns = [
        "age",
        "income",
        "purchase_frequency",
        "annual_spending"
    ]


    missing_columns = [
        column
        for column in required_columns
        if column not in result.columns
    ]


    # --------------------------------------------------------
    # Missing required features
    # --------------------------------------------------------

    if missing_columns:

        return (
            None,
            mapping,
            missing_columns
        )


    # ========================================================
    # NUMERIC CONVERSION
    # ========================================================

    for column in required_columns:

        result[column] = pd.to_numeric(
            result[column],
            errors="coerce"
        )


    # ========================================================
    # INVALID VALUES
    # ========================================================

    invalid_rows = (
        result[
            required_columns
        ]
        .isnull()
        .any(axis=1)
    )


    if invalid_rows.any():

        result = result.loc[
            ~invalid_rows
        ].copy()


    # ========================================================
    # AGE VALIDATION
    # ========================================================

    result.loc[
        (result["age"] < 0)
        | (result["age"] > 120),
        "age"
    ] = pd.NA


    # Remove rows made invalid by age validation
    result = result.dropna(
        subset=required_columns
    )


    # ========================================================
    # PURCHASE FREQUENCY RANGE
    # ========================================================

    result["purchase_frequency"] = (
        result["purchase_frequency"]
        .clip(0, 1)
    )


    # ========================================================
    # FINAL CLEANUP
    # ========================================================

    result = result[
        required_columns
    ].reset_index(
        drop=True
    )


    return (
        result,
        mapping,
        []
    )