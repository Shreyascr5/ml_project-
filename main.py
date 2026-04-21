# ================================
# 📦 IMPORTS
# ================================
import pandas as pd
import numpy as np

from sklearn.model_selection import train_test_split
from sklearn.metrics import mean_absolute_error, r2_score
from sklearn.ensemble import RandomForestRegressor


# ================================
# 📁 FILE PATH
# ================================
file = "data/AISHE Final Report 2019-20.xlsx"


# ================================
# 📊 STEP 1: GER (TARGET)
# ================================
df_ger = pd.read_excel(file, sheet_name="19GER", skiprows=2)

df_ger = df_ger.rename(columns={
    "Unnamed: 1": "state",
    "Total.2": "ger"
})

df_ger = df_ger[["state", "ger"]]

df_ger = df_ger[df_ger["state"].notna()]
df_ger = df_ger[~df_ger["state"].str.contains("All India", case=False, na=False)]
df_ger = df_ger[~df_ger["state"].astype(str).str.isnumeric()]

df_ger["ger"] = pd.to_numeric(df_ger["ger"], errors="coerce")
df_ger = df_ger.dropna(subset=["ger"])


# ================================
# 📊 STEP 2: STUDENTS
# ================================
df_students = pd.read_excel(file, sheet_name="6TotalEnr", skiprows=4, header=None)

df_students = df_students.rename(columns={
    1: "state",
    28: "students"
})

df_students = df_students[["state", "students"]]

df_students = df_students[df_students["state"].notna()]
df_students = df_students[~df_students["state"].astype(str).str.isnumeric()]
df_students = df_students[~df_students["state"].str.contains("All India", case=False, na=False)]

df_students["students"] = pd.to_numeric(df_students["students"], errors="coerce")
df_students = df_students.dropna(subset=["students"])


# ================================
# 📊 STEP 3: UNIVERSITIES
# ================================
df_uni = pd.read_excel(file, sheet_name="40NoUni", skiprows=3, header=None)

df_uni.columns = ["state", "y1", "y2", "y3", "y4", "universities"]

df_uni = df_uni[["state", "universities"]]

df_uni = df_uni[df_uni["state"].notna()]
df_uni["state"] = df_uni["state"].astype(str)

df_uni = df_uni[~df_uni["state"].str.contains("India", case=False, na=False)]
df_uni = df_uni[~df_uni["state"].str.isnumeric()]

df_uni["universities"] = pd.to_numeric(df_uni["universities"], errors="coerce")
df_uni = df_uni.dropna(subset=["universities"])


# ================================
# 📊 STEP 4: FACULTY
# ================================
df_fac_full = pd.read_excel(file, sheet_name="22TeacherPost", skiprows=4, header=None)

df_fac = df_fac_full.rename(columns={
    1: "state",
    19: "faculty"
})

df_fac = df_fac[["state", "faculty"]]

df_fac = df_fac[df_fac["state"].notna()]
df_fac["state"] = df_fac["state"].astype(str)

df_fac = df_fac[~df_fac["state"].str.contains("India", case=False, na=False)]
df_fac = df_fac[~df_fac["state"].str.isnumeric()]

df_fac["faculty"] = pd.to_numeric(df_fac["faculty"], errors="coerce")
df_fac = df_fac.dropna(subset=["faculty"])


# ================================
# 🔗 STEP 5: MERGE + YEAR
# ================================
df_final = df_ger.merge(df_students, on="state") \
                 .merge(df_uni, on="state") \
                 .merge(df_fac, on="state")

# Add year (for future multi-year use)
df_final["year"] = 2019

print("\nFinal Dataset:")
print(df_final.head())
print("\nShape:", df_final.shape)


# ================================
# 🤖 STEP 6: MODEL TRAINING
# ================================
X = df_final[["students", "universities", "faculty", "year"]]
y = df_final["ger"]

print("\nFeatures used:", X.columns)

X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.2, random_state=42
)

model = RandomForestRegressor(n_estimators=100, random_state=42)
model.fit(X_train, y_train)

predictions = model.predict(X_test)


# ================================
# 📊 STEP 7: EVALUATION
# ================================
mae = mean_absolute_error(y_test, predictions)
r2 = r2_score(y_test, predictions)
mape = np.mean(np.abs((y_test - predictions) / y_test)) * 100

print("\n--- FINAL MODEL PERFORMANCE ---")
print("MAE:", mae)
print("R2:", r2)
print("MAPE:", mape)


# ================================
# 🔍 STEP 8: FEATURE IMPORTANCE
# ================================
importance = model.feature_importances_

print("\nFeature Importance:")
print(pd.Series(importance, index=X.columns).sort_values(ascending=False))


#Feature selection 

from itertools import combinations
from sklearn.metrics import r2_score

features = ["students", "universities", "faculty", "year"]

best_score = -999
best_features = None

for i in range(1, len(features)+1):
    for combo in combinations(features, i):
        
        X = df_final[list(combo)]
        y = df_final["ger"]

        X_train, X_test, y_train, y_test = train_test_split(
            X, y, test_size=0.2, random_state=42
        )

        model = RandomForestRegressor(n_estimators=100, random_state=42)
        model.fit(X_train, y_train)

        predictions = model.predict(X_test)
        score = r2_score(y_test, predictions)

        print(f"{combo} → R2: {score}")

        if score > best_score:
            best_score = score
            best_features = combo

print("\nBEST FEATURE SET:", best_features)
print("BEST R2:", best_score)