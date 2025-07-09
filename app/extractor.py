from typing import Optional
import requests
import fitz  # PyMuPDF
from io import BytesIO

def extract_pdf_text_from_url(file_url: str) -> Optional[str]:
    try:
        response = requests.get(file_url)
        response.raise_for_status()

        pdf_stream = BytesIO(response.content)
        doc: fitz.Document = fitz.open(stream=pdf_stream, filetype="pdf")

        full_text = ""
        for page in doc:
            full_text += page.get_text()  # type: ignore
        return full_text.strip()

    except Exception as e:
        print(f"[Extractor Error] Failed to extract PDF text: {e}")
        return None
