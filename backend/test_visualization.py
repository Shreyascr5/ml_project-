from backend.ingestion.file_router import parse_file
from backend.analytics.schema_detector import detect_schema
from backend.analytics.visualization_engine import generate_visualization_data
df = parse_file("sample.csv")
schema = detect_schema(df)

visuals = generate_visualization_data(df, schema)

print(visuals)