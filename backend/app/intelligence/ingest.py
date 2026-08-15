"""Turn any uploaded file into plain text.

Add a new file type by adding one branch. Everything downstream only ever
sees a string, so nothing else needs to change.
"""

import io
import pandas as pd


def read_file(name: str, data: bytes) -> str:
    lower = name.lower()

    if lower.endswith(".pdf"):
        return _pdf(data)
    if lower.endswith(".docx"):
        return _docx(data)
    if lower.endswith((".xlsx", ".xls")):
        return _excel(data)
    if lower.endswith(".csv"):
        return pd.read_csv(io.BytesIO(data)).to_csv(index=False)
    # txt, md, json, anything else text-shaped
    return data.decode("utf-8", errors="ignore")


def _pdf(data: bytes) -> str:
    from pypdf import PdfReader

    reader = PdfReader(io.BytesIO(data))
    pages = []
    for number, page in enumerate(reader.pages, start=1):
        text = page.extract_text() or ""
        pages.append(f"[page {number}]\n{text}")
    joined = "\n\n".join(pages)
    if len(joined.strip()) < 50 * len(reader.pages):
        # Almost no text per page means it is a scanned image, not a text PDF.
        joined += "\n\n[WARNING: little text extracted - this PDF is probably scanned and needs OCR]"
    return joined


def _docx(data: bytes) -> str:
    from docx import Document

    doc = Document(io.BytesIO(data))
    return "\n".join(p.text for p in doc.paragraphs if p.text.strip())


def _excel(data: bytes) -> str:
    sheets = pd.read_excel(io.BytesIO(data), sheet_name=None)
    out = []
    for sheet_name, frame in sheets.items():
        out.append(f"[sheet: {sheet_name}]\n{frame.to_csv(index=False)}")
    return "\n\n".join(out)


def chunk(text: str, size: int = 1200, overlap: int = 200) -> list[str]:
    """Split on paragraphs, then pack into chunks of roughly `size` characters.

    Overlap stops a sentence that straddles a boundary from being lost.
    """
    paragraphs = [p.strip() for p in text.split("\n\n") if p.strip()]

    # A PDF page often has no blank lines at all, which would make the whole
    # page one paragraph. Hard-split anything longer than the target size.
    split_paragraphs = []
    for paragraph in paragraphs:
        while len(paragraph) > size:
            cut = paragraph.rfind("\n", 0, size)
            if cut < size // 2:
                cut = size
            split_paragraphs.append(paragraph[:cut].strip())
            paragraph = paragraph[cut:]
        if paragraph.strip():
            split_paragraphs.append(paragraph.strip())
    paragraphs = split_paragraphs

    chunks, current = [], ""

    for paragraph in paragraphs:
        if len(current) + len(paragraph) < size:
            current += paragraph + "\n\n"
        else:
            if current:
                chunks.append(current.strip())
            current = current[-overlap:] + paragraph + "\n\n" if overlap else paragraph + "\n\n"

    if current.strip():
        chunks.append(current.strip())
    return chunks
