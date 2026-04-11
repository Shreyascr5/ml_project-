import tabula

def parse_pdf(file_path):
    tables = tabula.read_pdf(file_path, pages='all', multiple_tables=True)
    return tables[0] if tables else None