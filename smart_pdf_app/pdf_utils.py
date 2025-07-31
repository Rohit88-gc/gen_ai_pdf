import fitz  # PyMuPDF

def extract_pdf_text(pdf_path):
    doc = fitz.open(pdf_path)
    text = ""
    for page in doc:
        text += page.get_text()
    doc.close()
    return text[:10000]  # Limit to 10,000 characters to avoid token limits