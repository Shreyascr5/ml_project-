from scipy.stats import pearsonr

## Stats Engine: Performs statistical tests and analyses based on the detected schema and the DataFrame
def correlation_test(df, col1, col2):
    corr, p_value = pearsonr(df[col1], df[col2])

    return {
        "correlation": corr,
        "p_value": p_value,
        "significant": p_value < 0.05
    }