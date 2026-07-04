import fitz

def extract_text(pdf_path):

    doc = fitz.open(pdf_path)

    text = ""

    for page in doc:
        text += page.get_text()

    pages = len(doc)

    doc.close()

    return text, pages