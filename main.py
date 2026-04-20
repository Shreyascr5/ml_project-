import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LinearRegression
from sklearn.metrics import mean_squared_error
from sklearn.metrics import mean_absolute_error, r2_score
import numpy as np  

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

# print("\nPredictings:\n", predictions)

# print("\nActual values:")
# print(y_test.values)



#universities data:

df_uni = pd.read_excel(file, sheet_name="40NoUni", skiprows=3, header=None)

# Assign proper column names manually
df_uni.columns = [ "state", "y1", "y2", "y3", "y4","universities"]

# Keep only needed columns
df_uni = df_uni[["state", "universities"]]

# Remove junk rows
df_uni = df_uni[df_uni["state"].notna()]
df_uni["state"] = df_uni["state"].astype(str)

df_uni = df_uni[~df_uni["state"].str.contains("India", case=False, na=False)]
df_uni = df_uni[~df_uni["state"].str.isnumeric()]

# Convert to numeric
df_uni["universities"] = pd.to_numeric(df_uni["universities"], errors="coerce")

df_uni = df_uni.dropna(subset=["universities"])

# print(df_uni.head())
# print("\nShape:", df_uni.shape)


#merge with final data 

df_final=pd.merge(df_final, df_uni, on="state")

print(df_final.head())
print("\nShape:", df_final.shape)

X=df_final[["students", "universities"]]
y=df_final["ger"]

mae = mean_absolute_error(y_test, predictions)
r2 = r2_score(y_test, predictions)

print("MAE:", mae)
print("R2:", r2)


#percentage error

mape = np.mean(np.abs((y_test - predictions) / y_test)) * 100
print("MAPE:", mape)







