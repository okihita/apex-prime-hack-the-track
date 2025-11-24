import os
from pathlib import Path

try:
    from pdf2image import convert_from_path
    has_pdf2image = True
except ImportError:
    has_pdf2image = False
    print("pdf2image not installed. Trying PyMuPDF...")
    
try:
    import fitz  # PyMuPDF
    has_pymupdf = True
except ImportError:
    has_pymupdf = False

if not has_pdf2image and not has_pymupdf:
    print("Installing PyMuPDF...")
    os.system("pip install PyMuPDF")
    import fitz
    has_pymupdf = True

pdf_files = list(Path('.').glob('*.pdf'))

for pdf_file in pdf_files:
    output_name = pdf_file.stem + '.png'
    print(f"Extracting {pdf_file} -> {output_name}")
    
    if has_pymupdf:
        doc = fitz.open(pdf_file)
        page = doc[0]
        pix = page.get_pixmap(dpi=300)
        pix.save(output_name)
        doc.close()
    elif has_pdf2image:
        images = convert_from_path(pdf_file, dpi=300)
        images[0].save(output_name, 'PNG')

print("Done extracting images!")
