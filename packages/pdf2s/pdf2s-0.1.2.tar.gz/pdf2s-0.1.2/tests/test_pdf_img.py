#!/usr/bin/env python3
"""
Test script for the pdf_img.py module.
"""
import sys
import os
from pathlib import Path

# Add the src directory to the Python path
sys.path.insert(0, str(Path(__file__).parent.parent))

from src.pdf2s.converters.pdf_img import extract_images


def main():
    """Test the extract_images function with a provided PDF file."""
    if len(sys.argv) < 2:
        print("Usage: python test_pdf_img.py <pdf_file_path> [output_dir] [min_size] [formats]")
        print("Example: python test_pdf_img.py sample.pdf output_folder 100 png,jpg")
        return 1
    
    pdf_path = sys.argv[1]
    if not os.path.exists(pdf_path):
        print(f"Error: File '{pdf_path}' does not exist")
        return 1
    
    # Parse optional arguments
    output_dir = sys.argv[2] if len(sys.argv) > 2 else None
    min_size = int(sys.argv[3]) if len(sys.argv) > 3 else 100
    formats = sys.argv[4].split(',') if len(sys.argv) > 4 else None
    
    print(f"Testing PDF image extraction on: {pdf_path}")
    print(f"Output directory: {output_dir or 'auto-generated'}")
    print(f"Minimum image size: {min_size}")
    print(f"Output formats: {formats or 'original'}")
    print("-" * 50)
    
    # Run the extraction
    try:
        count = extract_images(pdf_path, output_dir, min_size, formats)
        print("-" * 50)
        print(f"Test completed: {count} images extracted")
        return 0
    except Exception as e:
        print(f"Test failed with error: {str(e)}")
        import traceback
        traceback.print_exc()
        return 1


if __name__ == "__main__":
    sys.exit(main())