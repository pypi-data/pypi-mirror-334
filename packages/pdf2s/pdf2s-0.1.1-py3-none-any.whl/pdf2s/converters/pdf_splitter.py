from PyPDF2 import PdfReader, PdfWriter
from pathlib import Path
import re


def split_pdf(input_path, output_dir, chunk_size=None, ranges=None):
    """Split PDF with enhanced range handling and defaults"""
    Path(output_dir).mkdir(parents=True, exist_ok=True)

    try:
        with open(input_path, 'rb') as file:
            reader = PdfReader(file)
            total_pages = len(reader.pages)

            if ranges:
                if ranges.lower() == 'all':
                    ranges = f"1-{total_pages}"

                for i, rng in enumerate(ranges.split(',')):
                    if '-' in rng:
                        start, end = map(int, rng.split('-'))
                    else:  # Single page
                        start = end = int(rng)

                    start = max(1, min(start, total_pages))
                    end = max(start, min(end, total_pages))

                    writer = PdfWriter()
                    for page_num in range(start-1, end):
                        writer.add_page(reader.pages[page_num])

                    output_path = Path(
                        output_dir) / f"{Path(input_path).stem}_part_{i+1}.pdf"
                    with open(output_path, 'wb') as out_file:
                        writer.write(out_file)

            else:
                chunk_size = chunk_size or 1  # Default to 1 if not specified
                for i in range(0, total_pages, chunk_size):
                    writer = PdfWriter()
                    for page_num in range(i, min(i+chunk_size, total_pages)):
                        writer.add_page(reader.pages[page_num])

                    output_path = Path(output_dir) / (
                        f"{Path(input_path).stem}_"
                        f"{i+1:03d}-{min(i+chunk_size, total_pages):03d}.pdf"
                    )
                    with open(output_path, 'wb') as out_file:
                        writer.write(out_file)

    except Exception as e:
        raise RuntimeError(f"PDF split failed: {str(e)}")
