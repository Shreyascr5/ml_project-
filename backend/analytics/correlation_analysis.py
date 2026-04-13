import pandas as pd


def correlation_analysis(df):
    numeric_cols = [
        "Students_Appeared",
        "Students_Qualified",
        "Literacy_Rate",
        "Pass_Percentage",
        "Latitude",
        "Longitude",
        "Year"
    ]

    corr_matrix = df[numeric_cols].corr()

    print("\n===== CORRELATION MATRIX =====")
    print(corr_matrix)

    print("\n===== CORRELATION WITH PASS % =====")
    print(
        corr_matrix["Pass_Percentage"]
        .sort_values(ascending=False)
    )


if __name__ == "__main__":
    df = pd.read_csv("data/processed/master_state_dataset.csv")

    correlation_analysis(df)