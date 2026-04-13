import pandas as pd


def load_datasets():
    datasets = {
        "state_10th": pd.read_excel("data/raw/10th_cbse_with_latlon.xlsx"),
        "state_12th": pd.read_excel("data/raw/12th_cbse_with_latlon.xlsx"),
        "region_10th": pd.read_csv("data/raw/regionwise_10th_final.csv"),
        "region_12th": pd.read_csv("data/raw/regionwise_12th_final.csv"),
        "literacy": pd.read_excel("data/raw/tab8.5 (1).xlsx"),
    }

    return datasets


if __name__ == "__main__":
    data = load_datasets()

    for name, df in data.items():
        print("\n" + "="*50)
        print(name.upper())
        print("="*50)
        print("Shape:", df.shape)
        print("Columns:", list(df.columns))
        print(df.head())