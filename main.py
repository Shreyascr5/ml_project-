import pandas as pd

# Define file path
file = "data/AISHE Final Report 2019-20.xlsx"

# Load GER sheet
df = pd.read_excel(file, sheet_name="19GER", skiprows=2)

# Check columns first
print("Columns:\n", df.columns)

# Rename only required columns
df = df.rename(columns={
    "Unnamed: 1": "state",
    "Total.2": "ger"
})

# Keep only relevant columns
df = df[["state", "ger"]]

# Remove invalid rows
df = df[df["state"].notna()]
df = df[~df["state"].str.contains("All India", case=False, na=False)]

# Convert GER to numeric
df["ger"] = pd.to_numeric(df["ger"], errors="coerce")

# Drop missing GER
df = df.dropna(subset=["ger"])

print("\nCleaned Data:")
print(df.head())

print("\nShape:", df.shape)

