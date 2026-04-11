from ingestion.file_router import parse_file

df = parse_file("sample.csv")
print(df.head())