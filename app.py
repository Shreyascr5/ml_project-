import streamlit as st
import numpy as np
import pandas as pd
from sklearn.preprocessing import StandardScaler
from sklearn.linear_model import LinearRegression

# =========================
# LOAD YOUR TRAINED DATA
# =========================
df = pd.read_csv("final_dataset.csv")   # save your df_final as csv

# Feature engineering
df["students_per_uni"] = df["students"] / df["universities"]
df["faculty_per_student"] = df["faculty"] / df["students"]

df = df.dropna()

X = df[["students_per_uni", "faculty_per_student"]]
y = df["ger"]

# scaling
scaler = StandardScaler()
X_scaled = scaler.fit_transform(X)

# model
model = LinearRegression()
model.fit(X_scaled, y)

# =========================
# UI
# =========================
st.title("🎓 GER Predictor (AISHE ML Model)")

st.write("Predict Gross Enrollment Ratio based on infrastructure")

students = st.number_input("Number of Students", value=100000)
universities = st.number_input("Number of Universities", value=50)
faculty = st.number_input("Number of Faculty", value=5000)

# feature engineering
students_per_uni = students / universities if universities != 0 else 0
faculty_per_student = faculty / students if students != 0 else 0

input_data = np.array([[students_per_uni, faculty_per_student]])
input_scaled = scaler.transform(input_data)

prediction = model.predict(input_scaled)

if st.button("Predict GER"):
    st.success(f"Predicted GER: {prediction[0]:.2f}")