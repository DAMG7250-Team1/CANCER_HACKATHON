# features/mistral_parser.py

import fitz  # PyMuPDF
from typing import Tuple

def pdf_mistralocr_converter(pdf_bytes: bytes, base_path: str, s3_client) -> Tuple[str, str]:
    """
    Convert PDF bytes into Markdown format text.

    Args:
        pdf_bytes (bytes): The raw PDF content.
        base_path (str): Unused but kept for compatibility.
        s3_client: Unused but kept for compatibility.

    Returns:
        Tuple[str, str]: (Plain extracted text, Markdown converted text)
    """
    doc = fitz.open(stream=pdf_bytes, filetype="pdf")

    full_text = ""
    markdown_text = ""

    for page in doc:
        page_text = page.get_text()
        full_text += page_text + "\n"

        # Simple conversion: Treat each line as paragraph
        for line in page_text.splitlines():
            line = line.strip()
            if len(line) > 0:
                if line.endswith(":"):
                    markdown_text += f"\n### {line}\n"
                else:
                    markdown_text += f"{line}\n"

    return full_text.strip(), markdown_text.strip()
