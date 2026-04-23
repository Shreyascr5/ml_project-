import pandas as pd
import numpy as np

from extract_2019 import get_2019_data
from extract_2021 import get_2021_data

from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler
from sklearn.linear_model import LinearRegression
from sklearn.metrics import mean_absolute_error, r2_score


# =========================
# 📁 FILE PATHS
# =========================
file_2019 = "data/AISHE Final Report 2019-20.xlsx"
file_2021 = "data/AISHE Final Report 2021-22.xlsx"


# =========================
# 📊 LOAD DATA
# =========================
df_2019 = get_2019_data(file_2019)
df_2021 = get_2021_data(file_2021)

# Combine datasets
df_final = pd.concat([df_2019, df_2021], ignore_index=True)

print("Final Dataset Shape:", df_final.shape)


# =========================
# 🧹 CLEANING
# =========================
df_final = df_final.dropna()

# Remove extreme GER values (noise handling)
df_final = df_final[(df_final["ger"] > 5) & (df_final["ger"] < 60)]


# =========================
# ⚙️ FEATURE ENGINEERING
# =========================
df_final["students_per_uni"] = df_final["students"] / df_final["universities"]
df_final["faculty_per_student"] = df_final["faculty"] / df_final["students"]

# Handle division issues
df_final.replace([np.inf, -np.inf], np.nan, inplace=True)
df_final = df_final.dropna()


# =========================
# 🎯 FEATURES & TARGET
# =========================
X = df_final[[
    "students_per_uni",
    "faculty_per_student",
    # "universities"   # added for better performance
]]

y = df_final["ger"]


# =========================
# 📉 TRAIN-TEST SPLIT
# =========================
X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.2, random_state=42
)


# =========================
# 🔄 SCALING
# =========================
scaler = StandardScaler()
X_train = scaler.fit_transform(X_train)
X_test = scaler.transform(X_test)


# =========================
# 🤖 MODEL
# =========================
model = LinearRegression()
model.fit(X_train, y_train)

pred = model.predict(X_test)


# =========================
# 📊 EVALUATION
# =========================
mae = mean_absolute_error(y_test, pred)
r2 = r2_score(y_test, pred)

# Safe MAPE
y_safe = y_test.replace(0, np.nan)
mape = np.nanmean(np.abs((y_test - pred) / y_safe)) * 100


print("\n--- MODEL PERFORMANCE ---")
print("MAE:", round(mae, 3))
print("R2:", round(r2, 3))
print("MAPE:", round(mape, 2))


# =========================
# 🔍 INTERPRETATION
# =========================
print("\nFeature Coefficients:")
print(pd.Series(model.coef_, index=X.columns).sort_values(ascending=False))