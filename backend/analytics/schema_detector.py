import pandas as pd


def detect_schema(df: pd.DataFrame):
    schema = {
        "numeric_columns": [],
        "categorical_columns": [],
        "date_columns": [],
        "geographic_columns": [],
        "potential_targets": [],
        "missing_values": {},
        "shape": df.shape
    }

    geo_keywords = [
        "state",
        "region",
        "district",
        "city",
        "country",
        "location"
    ]

    for col in df.columns:
        dtype = df[col].dtype

        # Missing Values
        schema["missing_values"][col] = int(df[col].isnull().sum())

        # Numeric Detection
        if pd.api.types.is_numeric_dtype(dtype):
            schema["numeric_columns"].append(col)

        # Date Detection
        elif "year" in col.lower() or "date" in col.lower():
            schema["date_columns"].append(col)

        # Geographic Detection
        elif any(keyword in col.lower() for keyword in geo_keywords):
            schema["geographic_columns"].append(col)

        # Categorical Detection
        else:
            schema["categorical_columns"].append(col)

    # Potential Targets
    for col in schema["numeric_columns"]:
        if "pass" in col.lower() or "score" in col.lower() or "target" in col.lower():
            schema["potential_targets"].append(col)

    return schema
