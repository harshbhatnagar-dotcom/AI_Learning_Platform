import fitz
from docx import Document
from pptx import Presentation
import pytesseract
from PIL import Image
import io

def extract_pdf(pdf_path: str) -> str:
    doc = fitz.open(pdf_path)
    text = "\n".join(page.get_text() for page in doc).strip()
    if text:
        return text

    print("🔍 Running OCR (Tesseract fallback)...")

    ocr_text = []
    for page in doc:
        # Convert page to image
        pix = page.get_pixmap(dpi=300)
        img = Image.open(io.BytesIO(pix.tobytes("png")))

        # Perform OCR
        text = pytesseract.image_to_string(
            img,
            lang="eng",
            config="--oem 3 --psm 6"
        )

        ocr_text.append(text)

    return "\n".join(ocr_text)

def extract_docx(file_path):
    """Extract text from DOCX."""
    doc = Document(file_path)

    text = ""

    for para in doc.paragraphs:
        text += para.text + "\n"

    return text


def extract_pptx(file_path):
    """Extract text from PPTX."""
    prs = Presentation(file_path)

    text = ""

    for slide in prs.slides:
        for shape in slide.shapes:
            if hasattr(shape, "text"):
                text += shape.text + "\n"

    return text


def extract_text(file_path):
    """
    Automatically detect file type
    and extract text.
    """

    file_path = file_path.lower()

    if file_path.endswith(".pdf"):
        return extract_pdf(file_path)

    elif file_path.endswith(".docx"):
        return extract_docx(file_path)

    elif file_path.endswith(".pptx"):
        return extract_pptx(file_path)

    else:
        raise ValueError("Unsupported file format.")