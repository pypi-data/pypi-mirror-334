from PyPDF2 import PdfReader
from pathlib import Path
import io
import os
import hashlib
from PIL import Image
import pdfplumber


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

    # Track extracted images by content hash to avoid duplicates
    extracted_hashes = set()
    total_image_count = 0
    errors = []

    # Helper function to compute image data hash
    def get_image_hash(data):
        return hashlib.md5(data).hexdigest()

    # default method: Use PyPDF2
    try:
        reader = PdfReader(input_path)
        base_filename = Path(input_path).stem

        for page_num, page in enumerate(reader.pages):
            # Skip pages with no images
            if not hasattr(page, 'images') or not page.images:
                continue

            # Process each image on the page
            for img_index, img_file_obj in enumerate(page.images):
                # Extract raw image data
                image_data = img_file_obj.data
                image_hash = get_image_hash(image_data)

                # Skip if we've already extracted this image
                if image_hash in extracted_hashes:
                    continue

                # Create unique filename for this image
                raw_filename = f"{base_filename}_p" + \
                    f"{page_num+1}_img{img_index+1}.raw"
                raw_path = Path(output_dir) / raw_filename

                # First, save the raw data (as fallback)
                try:
                    with open(raw_path, 'wb') as f:
                        f.write(image_data)

                    # Now try to process with PIL
                    try:
                        # First, try to open directly
                        img = Image.open(io.BytesIO(image_data))
                        width, height = img.size

                        # Skip small images
                        if width < min_size or height < min_size:
                            # Remove the raw file for small images
                            os.remove(raw_path)
                            continue

                        # Save in requested format(s) or original format
                        if formats:
                            for fmt in formats:
                                img_filename = f"{base_filename}_p" + \
                                    f"{page_num+1}_img{img_index+1}.{fmt}"
                                output_path = Path(output_dir) / img_filename
                                img.save(output_path, format=fmt.upper())

                            # Remove raw file if we saved in proper format
                            os.remove(raw_path)
                        else:
                            # Use original format or PNG as fallback
                            fmt = img.format.lower() if img.format else "png"
                            img_filename = f"{base_filename}_p" + \
                                f"{page_num+1}_img{img_index+1}.{fmt}"
                            output_path = Path(output_dir) / img_filename
                            img.save(output_path)

                            # Remove raw file if we successfully saved
                            os.remove(raw_path)

                        # Record that we've extracted this image
                        extracted_hashes.add(image_hash)
                        total_image_count += 1

                    except Exception as img_err:
                        # Keep the raw file if we had an error
                        errors.append(
                            "Warning: Saved raw image data " +
                            f"for image on page {page_num+1}: {str(img_err)}")
                        # Record that we've extracted this image
                        extracted_hashes.add(image_hash)
                        total_image_count += 1  # Count the raw image

                except Exception as raw_err:
                    errors.append(
                        "Warning: Failed to save image on page " +
                        f"{page_num+1}: {str(raw_err)}")

    except Exception as e:
        errors.append(f"Warning: Issue with PyPDF2 extraction: {str(e)}")
        print(
            "Note: Primary extraction had issues, " +
            "falling back to alternative method"
        )

    # Second method: Always try pdfplumber for additional images
    try:
        with pdfplumber.open(input_path) as pdf:
            base_filename = Path(input_path).stem
            plumber_count = 0
            print("Using pdfplumber to look for additional images...")

            # Process all pages
            for page_num, page in enumerate(pdf.pages):
                # Check if this page has images
                if not hasattr(page, 'images') or not page.images:
                    continue

                print(
                    f"Processing page {page_num+1} with pdfplumber," +
                    f"found {len(page.images)} images")

                # Process each image on the page
                for img_index, img in enumerate(page.images):
                    try:
                        # Get raw image data
                        image_data = img["stream"].get_data()
                        image_hash = get_image_hash(image_data)

                        # Skip if we've already extracted this image
                        if image_hash in extracted_hashes:
                            continue

                        # Create unique filename for this image
                        raw_filename = f"{base_filename}_plumber_p" + \
                            f"{page_num+1}_img{img_index+1}.raw"
                        raw_path = Path(output_dir) / raw_filename

                        # First save the raw data
                        with open(raw_path, 'wb') as f:
                            f.write(image_data)

                        # Try to process with PIL
                        try:
                            # Try to open as a standard image
                            pil_img = Image.open(io.BytesIO(image_data))
                            width, height = pil_img.size

                            # Skip small images
                            if width < min_size or height < min_size:
                                os.remove(raw_path)
                                continue

                            # Save as PNG (most reliable format)
                            img_filename = f"{base_filename}_plumber_p" + \
                                f"{page_num+1}_img{img_index+1}.png"
                            output_path = Path(output_dir) / img_filename
                            pil_img.save(output_path, format="PNG")

                            # Remove raw file if we successfully saved
                            os.remove(raw_path)

                            # Record that we've extracted this image
                            extracted_hashes.add(image_hash)
                            plumber_count += 1

                        except Exception as pil_err:
                            # If standard image processing fails,
                            # try to convert image based on its dimensions
                            try:
                                # Get image dimensions from pdfplumber metadata
                                width = int(img.get("width", 0))
                                height = int(img.get("height", 0))

                                if width > min_size and height > min_size:
                                    # Try to create an image from raw bytes
                                    # with explicit dimensions
                                    try:
                                        # Mode depends on image data,
                                        # try common formats
                                        for mode in ["RGB", "RGBA", "L"]:
                                            try:
                                                pil_img = Image.frombytes(
                                                    mode, (width, height),
                                                    image_data)
                                                img_filename = \
                                                    f"{base_filename}_" + \
                                                    "plumber_p" + \
                                                    f"{page_num+1}_" + \
                                                    f"img{img_index+1}" + \
                                                    f"_{mode}.png"
                                                output_path = Path(
                                                    output_dir) / img_filename
                                                pil_img.save(
                                                    output_path, format="PNG")
                                                # Remove raw file on success
                                                os.remove(raw_path)
                                                # Record extracted image
                                                extracted_hashes.add(image_hash)
                                                plumber_count += 1
                                                break
                                            except BaseException:
                                                continue
                                    except BaseException:
                                        # Keep raw data as fallback
                                        errors.append(
                                            "Warning: Saved raw image for pg" +
                                            f"{page_num+1}")
                                        # Record that we've extracted this image
                                        extracted_hashes.add(image_hash)
                                        plumber_count += 1
                                else:
                                    # Remove raw file for small images
                                    os.remove(raw_path)
                            except BaseException:
                                # Keep the raw file if processing failed
                                errors.append(
                                    "Warning: Saved raw image data for image" +
                                    f" on pg{page_num+1}: {str(pil_err)}")
                                # Record that we've extracted this image
                                extracted_hashes.add(image_hash)
                                plumber_count += 1  # Count the raw image

                    except Exception as extract_err:
                        errors.append(
                            "Warning: Failed to extract image on pg" +
                            f"{page_num+1}: {str(extract_err)}")

            if plumber_count > 0:
                print(
                    f"PDFPlumber extracted {plumber_count} additional images")
                total_image_count += plumber_count

    except Exception as plumber_err:
        errors.append(
            f"Warning: Issue with pdfplumber extraction: {str(plumber_err)}")

    # Print warnings but don't fail
    for error in errors:
        print(error)

    # Summary
    if total_image_count == 0:
        print("No images found or all images were below minimum size.")
    else:
        print(f"Successfully extracted {total_image_count} unique images.")
        if len(errors) > 0:
            print(
                f"Note: {len(errors)} warning(s) occurred during extraction.")
            print("Some images may be saved in raw format.")

    return total_image_count
