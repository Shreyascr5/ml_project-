from ingestion.file_router import parse_file
from analytics.schema_detector import detect_schema
from analytics.eda_engine import generate_eda_report

df = parse_file("sample.csv")
schema = detect_schema(df)

report = generate_eda_report(df, schema)

print(report)