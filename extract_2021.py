import pandas as pd

def get_2021_data(file):

    # GER
    df_ger = pd.read_excel(file, sheet_name="19GER(2011)", skiprows=2)
    df_ger = df_ger.rename(columns={
        df_ger.columns[1]: "state",
        df_ger.columns[-1]: "ger"
    })
    df_ger = df_ger[["state", "ger"]]
    df_ger = df_ger[df_ger["state"].notna()]
    df_ger["state"] = df_ger["state"].astype(str)
    df_ger = df_ger[df_ger["state"].str.contains("[A-Za-z]", regex=True)]
    df_ger["ger"] = pd.to_numeric(df_ger["ger"], errors="coerce")
    df_ger = df_ger.dropna()

    print("GER:", df_ger.shape)


    # STUDENTS
    df_students = pd.read_excel(file, sheet_name="6TotalEnr", skiprows=4, header=None)
    df_students = df_students.rename(columns={1: "state", 28: "students"})
    df_students = df_students[["state", "students"]]
    df_students = df_students[df_students["state"].notna()]
    df_students["state"] = df_students["state"].astype(str)
    df_students = df_students[df_students["state"].str.contains("[A-Za-z]", regex=True)]
    df_students["students"] = pd.to_numeric(df_students["students"], errors="coerce")
    df_students = df_students.dropna()

    print("STUDENTS:", df_students.shape)


    # UNIVERSITIES
    df_uni = pd.read_excel(file, sheet_name="40NoUni", skiprows=4, header=None)

    df_uni = df_uni.rename(columns={
    1: "state",                      # ← shifted
    df_uni.columns[-1]: "universities"   # ← always last column
    })
    df_uni = df_uni[["state", "universities"]]
    df_uni = df_uni[df_uni["state"].notna()]
    df_uni["state"] = df_uni["state"].astype(str)
    df_uni = df_uni[df_uni["state"].str.contains("[A-Za-z]", regex=True)]
    df_uni["universities"] = pd.to_numeric(df_uni["universities"], errors="coerce")
    df_uni = df_uni.dropna()

    print("UNIVERSITIES:", df_uni.shape)


    # FACULTY
    df_fac = pd.read_excel(file, sheet_name="22TeacherPost", skiprows=4, header=None)
    df_fac = df_fac.rename(columns={1: "state", 22: "faculty"})
    df_fac = df_fac[["state", "faculty"]]
    df_fac = df_fac[df_fac["state"].notna()]
    df_fac["state"] = df_fac["state"].astype(str)
    df_fac = df_fac[df_fac["state"].str.contains("[A-Za-z]", regex=True)]
    df_fac["faculty"] = pd.to_numeric(df_fac["faculty"], errors="coerce")
    df_fac = df_fac.dropna()

    print("FACULTY:", df_fac.shape)


    # TRY MERGE STEP BY STEP
    df_temp = df_ger.merge(df_students, on="state", how="inner")
    print("After GER + STUDENTS:", df_temp.shape)

    df_temp = df_temp.merge(df_uni, on="state", how="inner")
    print("After + UNIVERSITIES:", df_temp.shape)

    df_temp = df_temp.merge(df_fac, on="state", how="inner")
    print("After + FACULTY:", df_temp.shape)

    df_temp["year"] = 2021

    return df_temp