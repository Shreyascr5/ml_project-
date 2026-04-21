# ================================
# 📦 IMPORTS
# ================================
import pandas as pd
import numpy as np

from sklearn.model_selection import train_test_split
from sklearn.linear_model import LinearRegression
from sklearn.metrics import mean_absolute_error, r2_score
from sklearn.ensemble import RandomForestRegressor


# ================================
# 📁 FILE PATH
# ================================
file = "data/AISHE Final Report 2019-20.xlsx"


# ================================
# 📊 STEP 1: LOAD & CLEAN GER (TARGET VARIABLE)
# ================================
df_ger = pd.read_excel(file, sheet_name="19GER", skiprows=2)

# Rename useful columns
df_ger = df_ger.rename(columns={
    "Unnamed: 1": "state",
    "Total.2": "ger"
})

# Keep only relevant columns
df_ger = df_ger[["state", "ger"]]

# Clean data
df_ger = df_ger[df_ger["state"].notna()]
df_ger = df_ger[~df_ger["state"].str.contains("All India", case=False, na=False)]
df_ger = df_ger[~df_ger["state"].astype(str).str.isnumeric()]

# Convert to numeric
df_ger["ger"] = pd.to_numeric(df_ger["ger"], errors="coerce")
df_ger = df_ger.dropna(subset=["ger"])


# ================================
# 📊 STEP 2: LOAD & CLEAN STUDENTS DATA
# ================================
df_students = pd.read_excel(file, sheet_name="6TotalEnr", skiprows=4, header=None)

df_students = df_students.rename(columns={
    1: "state",
    28: "students"
})

df_students = df_students[["state", "students"]]

# Clean
df_students = df_students[df_students["state"].notna()]
df_students = df_students[~df_students["state"].astype(str).str.isnumeric()]
df_students = df_students[~df_students["state"].str.contains("All India", case=False, na=False)]

df_students["students"] = pd.to_numeric(df_students["students"], errors="coerce")
df_students = df_students.dropna(subset=["students"])


# ================================
# 📊 STEP 3: LOAD & CLEAN UNIVERSITIES DATA
# ================================
df_uni = pd.read_excel(file, sheet_name="40NoUni", skiprows=3, header=None)

df_uni.columns = ["state", "y1", "y2", "y3", "y4", "universities"]

df_uni = df_uni[["state", "universities"]]

# Clean
df_uni = df_uni[df_uni["state"].notna()]
df_uni["state"] = df_uni["state"].astype(str)

df_uni = df_uni[~df_uni["state"].str.contains("India", case=False, na=False)]
df_uni = df_uni[~df_uni["state"].str.isnumeric()]

df_uni["universities"] = pd.to_numeric(df_uni["universities"], errors="coerce")
df_uni = df_uni.dropna(subset=["universities"])


# ================================
# 📊 STEP 4: LOAD & PROCESS COLLEGES DATA (FEATURE ENGINEERING)
# ================================
df_col = pd.read_excel(file, sheet_name="3Collegerange", skiprows=4, header=None)

# Assign column names
df_col.columns = ["sl_no", "state"] + [f"c{i}" for i in range(len(df_col.columns)-2)]

# Remove unnecessary column
df_col = df_col.drop(columns=["sl_no"])

# Clean
df_col = df_col[df_col["state"].notna()]
df_col["state"] = df_col["state"].astype(str)

df_col = df_col[~df_col["state"].str.contains("India", case=False, na=False)]
df_col = df_col[~df_col["state"].str.isnumeric()]

# Convert all range columns to numeric
for col in df_col.columns[1:]:
    df_col[col] = pd.to_numeric(df_col[col], errors="coerce")

# 🔥 IMPORTANT: Compute total colleges (feature engineering)
df_col["colleges"] = df_col.iloc[:, 1:].sum(axis=1)

df_col = df_col[["state", "colleges"]]


# ================================
# 🔗 STEP 5: MERGE ALL DATASETS
# ================================
df_final = df_ger.merge(df_students, on="state") \
                 .merge(df_uni, on="state") \
                 .merge(df_col, on="state")

print("\nFinal Dataset:")
print(df_final.head())
print("\nShape:", df_final.shape)


# ================================
# 🤖 STEP 6: TRAIN ML MODEL
# ================================

# Features (X) and Target (y)
X = df_final[["students", "universities"]]
y = df_final["ger"]

print("\nFeatures used:", X.columns)

# Split data
X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.2, random_state=42
)

# Train model
model = RandomForestRegressor()
model.fit(X_train, y_train)

# Predict
predictions = model.predict(X_test)


# ================================
# 📊 STEP 7: EVALUATE MODEL
# ================================
mae = mean_absolute_error(y_test, predictions)
r2 = r2_score(y_test, predictions)

# MAPE (percentage error)
mape = np.mean(np.abs((y_test - predictions) / y_test)) * 100

print("\n--- MODEL PERFORMANCE ---")
print("MAE:", mae)
print("R2:", r2)
print("MAPE:", mape)


# ================================
# 🔍 STEP 8: MODEL INTERPRETATION
# ================================
# print("\nModel Coefficients:", model.coef_)
print("Feature Names:", X.columns)