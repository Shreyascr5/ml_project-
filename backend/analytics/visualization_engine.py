def generate_visualization_data(df, schema):
    visuals = {}

    numeric_cols = schema["numeric_columns"]

    # Histogram / Distribution Data
    visuals["distributions"] = {
        col: df[col].dropna().tolist()
        for col in numeric_cols
    }

    # Correlation Heatmap Data
    if len(numeric_cols) >= 2:
        corr_matrix = df[numeric_cols].corr()

        visuals["correlation_heatmap"] = {
            "labels": numeric_cols,
            "matrix": corr_matrix.values.tolist()
        }

    # Missing Values
    visuals["missing_values"] = {
        col: int(df[col].isnull().sum())
        for col in df.columns
    }

    # Geographic Data
    geo_cols = schema["geographic_columns"]
    if geo_cols:
        visuals["geo_data"] = df[geo_cols].to_dict(orient="records")

    return visuals