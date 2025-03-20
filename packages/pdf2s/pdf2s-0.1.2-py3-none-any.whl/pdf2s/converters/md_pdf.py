from weasyprint import HTML
import markdown2


def convert_md_to_pdf(input_path, output_path, style_sheet=None):
    """Convert Markdown to PDF with optional CSS styling"""
    try:
        with open(input_path, 'r') as md_file:
            html_content = markdown2.markdown(
                md_file.read(), extras=['tables'])

        html = HTML(string=html_content)
        css = [style_sheet] if style_sheet and Path(
            style_sheet).exists() else None
        html.write_pdf(output_path, stylesheets=css)
    except Exception as e:
        raise RuntimeError(f"MD to PDF conversion failed: {str(e)}")
