import pandas as pd

# EDA Engine: Generates a comprehensive report based on the detected schema and the DataFrame
def generate_eda_report(df: pd.DataFrame, schema: dict):
    report = {}

    numeric_cols = schema["numeric_columns"]

    # Basic Summary
    report["summary_statistics"] = df.describe().to_dict()

    # Correlation Matrix
    if len(numeric_cols) >= 2:
        report["correlation_matrix"] = df[numeric_cols].corr().to_dict()
    else:
        report["correlation_matrix"] = {}

    # Missing Values
    report["missing_values"] = df.isnull().sum().to_dict()

    # Unique Counts
    report["unique_values"] = {
        col: int(df[col].nunique()) for col in df.columns
    }

    return report