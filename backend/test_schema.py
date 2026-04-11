from ingestion.file_router import parse_file
from analytics.schema_detector import detect_schema

df = parse_file("sample.csv")

schema = detect_schema(df)

print(schema)