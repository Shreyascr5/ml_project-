import pandas as pd


def clean_state_dataset(df, level):
    appeared_col = [col for col in df.columns if "Appeared" in col][0]
    qualified_col = [col for col in df.columns if "Qualified" in col][0]

    pass_cols = [col for col in df.columns if "Pass %" in col]

    melted = df.melt(
        id_vars=["State", appeared_col, qualified_col, "Latitude", "Longitude"],
        value_vars=pass_cols,
        var_name="Year",
        value_name="Pass_Percentage"
    )

    melted["Year"] = melted["Year"].str.extract(r'(\d{4})').astype(int)
    melted["Level"] = level

    melted.rename(columns={
        appeared_col: "Students_Appeared",
        qualified_col: "Students_Qualified"
    }, inplace=True)

    return melted
# cleaning the region dataset:

def clean_region_dataset(df, level):
    year_cols = [col for col in df.columns if col.isdigit()]

    melted = df.melt(
        id_vars=["Region", "Latitude", "Longitude"],
        value_vars=year_cols,
        var_name="Year",
        value_name="Pass_Percentage"
    )

    melted["Year"] = melted["Year"].astype(int)
    melted["Level"] = level

    return melted

def clean_literacy_dataset(df):
    df = df.iloc[3:].copy()

    df = df[[df.columns[0], df.columns[-1]]]

    df.columns = ["State", "Literacy_Rate"]

    df = df.dropna()

    return df

# merge datasets and save master datasets
from backend.data_processing.load_data import load_datasets


if __name__ == "__main__":
    datasets = load_datasets()

    state_10 = clean_state_dataset(datasets["state_10th"], 10)
    state_12 = clean_state_dataset(datasets["state_12th"], 12)

    region_10 = clean_region_dataset(datasets["region_10th"], 10)
    region_12 = clean_region_dataset(datasets["region_12th"], 12)

    literacy = clean_literacy_dataset(datasets["literacy"])

    master_state = pd.concat([state_10, state_12], ignore_index=True)
    master_region = pd.concat([region_10, region_12], ignore_index=True)

    master_state = master_state.merge(
        literacy,
        on="State",
        how="left"
    )

    master_state.to_csv("data/processed/master_state_dataset.csv", index=False)
    master_region.to_csv("data/processed/master_region_dataset.csv", index=False)

    print("Master datasets created successfully.")