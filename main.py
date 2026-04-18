import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LinearRegression
from sklearn.metrics import mean_squared_error

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
df=df[~df["state"].astype(str).str.isnumeric()]
# print("\nCleaned Data:")
# print(df.head())

# print("\nShape:", df.shape)


#laod total enrollment students

df_students=pd.read_excel(file, sheet_name="6TotalEnr",header=None,skiprows=4)


# Rename columns using index
df_students = df_students.rename(columns={
    1: "state",
    28: "students"
})

# Keep only required columns
df_students = df_students[["state", "students"]]

# Remove junk rows
df_students = df_students[df_students["state"].notna()]
df_students = df_students[~df_students["state"].astype(str).str.isnumeric()]
df_students = df_students[~df_students["state"].str.contains("All India", case=False, na=False)]

# Convert students to numeric
df_students["students"] = pd.to_numeric(df_students["students"], errors="coerce")

# Drop missing values
df_students = df_students.dropna(subset=["students"])

# print("\nClean Students Data:")
# print(df_students.head())
# print("\nShape:", df_students.shape)


# Merge GER and Students
df_final = pd.merge(df, df_students, on="state")

# print("\nMerged Data:")
# print(df_final.head())

# print("\nShape:", df_final.shape)
# print(df_final.isnull().sum())


#train model :



X=df_final[["students"]]
y=df_final["ger"]


#splitting data 80-20
X_train, X_test,y_train, y_test=train_test_split(X,y, test_size=0.2, random_state=42)


#train model

model=LinearRegression()
model.fit(X_train,y_train)


#predict


predictions= model.predict(X_test)

print("\nPredictings:\n", predictions)

print("\nActual values:")
print(y_test.values)










