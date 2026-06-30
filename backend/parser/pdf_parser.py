import fitz  # PyMuPDF


def extract_text(pdf_path: str) -> str:
    """
    Extracts all text from a PDF blood report.

    Args:
        pdf_path (str): Path to the uploaded PDF.

    Returns:
        str: Extracted text.
    """

    text = ""

    try:
        doc = fitz.open(pdf_path)

        for page in doc:
            text += page.get_text()

        doc.close()

        return text.strip()

    except Exception as e:
        raise Exception(f"Error reading PDF: {e}")

