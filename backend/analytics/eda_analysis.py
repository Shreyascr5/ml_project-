import pandas as pd


def basic_eda(df):
    print("\n===== SHAPE =====")
    print(df.shape)

    print("\n===== INFO =====")
    print(df.info())

    print("\n===== MISSING VALUES =====")
    print(df.isnull().sum())

    print("\n===== SUMMARY STATS =====")
    print(df.describe())

    print("\n===== TOP STATES BY AVG PASS % =====")
    print(
        df.groupby("State")["Pass_Percentage"]
        .mean()
        .sort_values(ascending=False)
        .head(10)
    )

    print("\n===== BOTTOM STATES BY AVG PASS % =====")
    print(
        df.groupby("State")["Pass_Percentage"]
        .mean()
        .sort_values()
        .head(10)
    )


if __name__ == "__main__":
    df = pd.read_csv("data/processed/master_state_dataset.csv")

    basic_eda(df)