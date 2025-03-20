from PyPDF2 import PdfReader
from pathlib import Path
import io
from PIL import Image


def extract_images(input_path, output_dir=None, min_size=100, formats=None):
    """
    Extract images from a PDF file using PyPDF2

    Args:
        input_path: Path to the PDF file
        output_dir: Dir to extracted images (if None, uses filename_imgs)
        min_size: Minimum size (width or height) for images to extract
        formats: Image format(s) to save as (default: original format or PNG)
    """
    # If output_dir is None, create directory based on input filename
    if output_dir is None:
        base_name = Path(input_path).stem
        output_dir = f"{base_name}_imgs"

    Path(output_dir).mkdir(parents=True, exist_ok=True)

    if formats and not isinstance(formats, list):
        formats = [formats.lower()]

    try:
        reader = PdfReader(input_path)
        base_filename = Path(input_path).stem
        image_count = 0

        for page_num, page in enumerate(reader.pages):
            if not hasattr(page, 'images') or not page.images:
                continue

            for img_index, img_file_obj in enumerate(page.images):
                # image_name = img_file_obj.name
                image_data = img_file_obj.data

                # Use PIL to process and check the image
                try:
                    image = Image.open(io.BytesIO(image_data))
                    width, height = image.size

                    # Skip small images (likely icons, etc.)
                    if width < min_size or height < min_size:
                        continue

                    # Determine image format
                    original_format = image.format or "PNG"

                    # Save in requested format(s) or original
                    if formats:
                        for fmt in formats:
                            img_filename = f"{base_filename}_p" + \
                                f"{page_num+1}_img{img_index+1}.{fmt}"
                            output_path = Path(output_dir) / img_filename
                            image.save(output_path, format=fmt.upper())
                    else:
                        # Use original format or default to PNG
                        ext = original_format.lower()
                        img_filename = f"{base_filename}_p" + \
                            f"{page_num+1}_img{img_index+1}.{ext}"
                        output_path = Path(output_dir) / img_filename
                        image.save(output_path)

                    image_count += 1
                except Exception as img_err:
                    # Skip problematic images
                    print(
                        "Warning: Could not process image on page " +
                        f"{page_num+1}: {str(img_err)}")

        if image_count == 0:
            print("No images found or all images were below " +
                  "minimum size threshold.")

        return image_count
    except Exception as e:
        raise RuntimeError(f"Image extraction failed: {str(e)}")
