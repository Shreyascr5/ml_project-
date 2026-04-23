import pandas as pd

def get_2019_data(file):

    # =========================
# GER (2019 FINAL FIX)
# =========================
    df_ger = pd.read_excel(
        file,
        sheet_name="19GER",
        header=[0, 1]   # multi-level header
    )

    # rename properly
    df_ger = df_ger.rename(columns={
        ('Unnamed: 1_level_0', 'Unnamed: 1_level_1'): 'state',
        ('All Categories', 'Total'): 'ger'
    })

    df_ger = df_ger[['state', 'ger']]

    df_ger = df_ger[df_ger["state"].notna()]
    df_ger["state"] = df_ger["state"].astype(str).str.strip()

    df_ger = df_ger[df_ger["state"].str.contains("[A-Za-z]", regex=True)]

    df_ger["ger"] = pd.to_numeric(df_ger["ger"], errors="coerce")
    df_ger = df_ger.dropna()

    # STUDENTS
    df_students = pd.read_excel(file, sheet_name="6TotalEnr", skiprows=4, header=None)
    df_students = df_students.rename(columns={1: "state", 28: "students"})
    df_students = df_students[["state", "students"]]
    df_students["state"] = df_students["state"].astype(str)
    df_students = df_students[df_students["state"].str.contains("[A-Za-z]")]
    df_students["students"] = pd.to_numeric(df_students["students"], errors="coerce")
    df_students = df_students.dropna()

    # UNIVERSITIES
    df_uni = pd.read_excel(file, sheet_name="40NoUni", skiprows=3, header=None)
    df_uni = df_uni.rename(columns={0: "state", 5: "universities"})
    df_uni = df_uni[["state", "universities"]]
    df_uni["state"] = df_uni["state"].astype(str)
    df_uni = df_uni[df_uni["state"].str.contains("[A-Za-z]")]
    df_uni["universities"] = pd.to_numeric(df_uni["universities"], errors="coerce")
    df_uni = df_uni.dropna()

    # FACULTY
    df_fac = pd.read_excel(file, sheet_name="22TeacherPost", skiprows=4, header=None)
    df_fac = df_fac.rename(columns={1: "state", 22: "faculty"})
    df_fac = df_fac[["state", "faculty"]]
    df_fac["state"] = df_fac["state"].astype(str)
    df_fac = df_fac[df_fac["state"].str.contains("[A-Za-z]")]
    df_fac["faculty"] = pd.to_numeric(df_fac["faculty"], errors="coerce")
    df_fac = df_fac.dropna()

    df = df_ger.merge(df_students, on="state") \
               .merge(df_uni, on="state") \
               .merge(df_fac, on="state")

    df["year"] = 2019
    return df