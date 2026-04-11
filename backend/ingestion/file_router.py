import os

from ingestion.csv_parser import parse_csv
from ingestion.excel_parser import parse_excel
from ingestion.pdf_parser import parse_pdf
from ingestion.image_parser import parse_image


def parse_file(file_path):
    ext = os.path.splitext(file_path)[1].lower()

    if ext == ".csv":
        return parse_csv(file_path)

    elif ext in [".xls", ".xlsx"]:
        return parse_excel(file_path)

    elif ext == ".pdf":
        return parse_pdf(file_path)

    elif ext in [".png", ".jpg", ".jpeg"]:
        return parse_image(file_path)

    else:
        raise ValueError("Unsupported file type")