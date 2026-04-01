"""
Serviço de parsing de arquivos PDF e XLS/XLSX.
Extrai dados tabulares brutos para processamento posterior.
"""

import pdfplumber
import pandas as pd


def parse_uploaded_file(file_path: str, extension: str) -> dict:
    """Roteia o parsing conforme extensão do arquivo."""
    if extension == ".pdf":
        return _parse_pdf(file_path)
    elif extension in (".xls", ".xlsx"):
        return _parse_excel(file_path)
    else:
        raise ValueError(f"Extensão não suportada: {extension}")


def _parse_pdf(file_path: str) -> dict:
    """Extrai tabelas e texto de PDFs usando pdfplumber."""
    tables = []
    full_text = []

    with pdfplumber.open(file_path) as pdf:
        for i, page in enumerate(pdf.pages):
            text = page.extract_text()
            if text:
                full_text.append(text)

            page_tables = page.extract_tables()
            for table in page_tables:
                if table and len(table) > 1:
                    headers = [str(h).strip() if h else f"col_{j}" for j, h in enumerate(table[0])]
                    rows = []
                    for row in table[1:]:
                        rows.append({
                            headers[k]: (str(cell).strip() if cell else "")
                            for k, cell in enumerate(row)
                            if k < len(headers)
                        })
                    tables.append({
                        "page": i + 1,
                        "headers": headers,
                        "rows": rows,
                    })

    return {
        "source": "pdf",
        "text": "\n".join(full_text),
        "tables": tables,
        "total_pages": len(full_text),
    }


def _parse_excel(file_path: str) -> dict:
    """Extrai dados de planilhas XLS/XLSX via pandas."""
    xls = pd.ExcelFile(file_path)
    sheets = {}

    for sheet_name in xls.sheet_names:
        df = pd.read_excel(xls, sheet_name=sheet_name)
        df = df.dropna(how="all")
        df.columns = [str(c).strip() for c in df.columns]

        sheets[sheet_name] = {
            "headers": df.columns.tolist(),
            "rows": df.fillna("").to_dict(orient="records"),
            "row_count": len(df),
        }

    return {
        "source": "excel",
        "sheets": sheets,
        "total_sheets": len(sheets),
    }
