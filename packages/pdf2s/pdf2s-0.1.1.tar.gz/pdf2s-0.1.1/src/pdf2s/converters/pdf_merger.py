import re
from pathlib import Path
from PyPDF2 import PdfReader, PdfWriter


def merge_pdfs(directory, output, regex_filter=None, sort=True):
    """Improved PDF merger with better file handling"""
    pdf_files = []
    dir_path = Path(directory)

    # Validate directory
    if not dir_path.is_dir():
        raise ValueError(f"Directory '{directory}' does not exist")

    # Find and filter PDF files
    for f in dir_path.glob('*.pdf'):
        if f.is_file():
            if not regex_filter or re.search(regex_filter, f.name):
                pdf_files.append(f)

    if not pdf_files:
        raise ValueError("No matching PDF files found")

    # Sort files if requested
    if sort:
        pdf_files.sort(key=lambda x: x.name.lower())

    # Merge PDFs
    writer = PdfWriter()
    for pdf_path in pdf_files:
        try:
            reader = PdfReader(pdf_path)
            for page in reader.pages:
                writer.add_page(page)
        except Exception as e:
            raise RuntimeError(f"Error processing {pdf_path.name}: {str(e)}")

    # Ensure output directory exists
    output_path = Path(output)
    output_path.parent.mkdir(parents=True, exist_ok=True)

    with open(output_path, 'wb') as f:
        writer.write(f)
