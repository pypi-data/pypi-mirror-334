import pdfplumber


def convert_pdf_to_md(input_path, output_path):
    """Convert PDF to basic Markdown format"""
    try:
        with pdfplumber.open(input_path) as pdf, open(output_path, 'w') as md_file:
            for page in pdf.pages:
                text = page.extract_text()
                md_file.write(f"# Page {page.page_number}\n\n{text}\n\n")
    except Exception as e:
        raise RuntimeError(f"PDF to MD conversion failed: {str(e)}")
