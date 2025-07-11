import os
from typing import Optional
import requests
import fitz  # PyMuPDF
from io import BytesIO
import docx2txt
import tempfile
import logging

logger = logging.getLogger(__name__)

def extract_text_from_url(file_url: str) -> Optional[str]:
    try:
        logger.info(f"Fetching file from: {file_url}")
        response = requests.get(file_url)
        response.raise_for_status()

        content_type = response.headers.get("Content-Type", "").lower()
        if file_url.lower().endswith(".pdf") or "application/pdf" in content_type:
            return _extract_pdf(response.content)
        elif file_url.lower().endswith(".docx") or "officedocument.wordprocessingml.document" in content_type:
            return _extract_docx(response.content)
        else:
            raise ValueError("Unsupported file type. Only PDF and DOCX are supported.")
    except Exception as e:
        logger.error(f"[Extractor Error] {e}")
        raise

def _extract_pdf(data: bytes) -> str:
    try:
        pdf_stream = BytesIO(data)
        doc = fitz.open(stream=pdf_stream, filetype="pdf")
        return "\n".join(page.get_text() for page in doc).strip() # type: ignore
    except Exception as e:
        logger.error(f"PDF extraction failed: {e}")
        raise ValueError("PDF extraction failed.")

def _extract_docx(data: bytes) -> str:
    tmp_path = None
    try:
        with tempfile.NamedTemporaryFile(delete=False, suffix=".docx") as tmp:
            tmp.write(data)
            tmp.flush()
            tmp_path = tmp.name

        text = docx2txt.process(tmp_path)
        return text.strip()

    except Exception as e:
        logger.error(f"DOCX extraction failed: {e}")
        raise ValueError("DOCX extraction failed.")

    finally:
        if tmp_path and os.path.exists(tmp_path):
            try:
                os.remove(tmp_path)
            except Exception as cleanup_error:
                logger.warning(f"Failed to remove temp DOCX file: {cleanup_error}")
