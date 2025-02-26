import io
import fitz  # PyMuPDF
import docx


def extract_text_from_file(file_bytes: bytes, filename: str) -> str:
    """Extract text from PDF or DOCX file."""
    # Identify file extension
    file_ext = filename.split(".")[-1].lower()

    # Handle PDF
    if file_ext == "pdf":
        return _extract_text_from_pdf(file_bytes)
    
    # Handle DOCX
    elif file_ext == "docx":
        return _extract_text_from_docx(file_bytes)
    
    else:
        raise ValueError("Unsupported file type. Please upload a PDF or DOCX.")


def _extract_text_from_pdf(file_bytes: bytes) -> str:
    """Extract text from a PDF using PyMuPDF."""
    text = ""
    with fitz.open(stream=file_bytes, filetype="pdf") as doc:
        for page in doc:
            text += page.get_text()
    return text


def _extract_text_from_docx(file_bytes: bytes) -> str:
    """Extract text from a DOCX file."""
    text = ""
    file_stream = io.BytesIO(file_bytes)
    doc = docx.Document(file_stream)
    for paragraph in doc.paragraphs:
        text += paragraph.text + "\n"
    return text
