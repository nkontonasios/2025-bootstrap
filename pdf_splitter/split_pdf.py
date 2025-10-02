import fitz  # PyMuPDF
from PIL import Image
import io

# Configuration
input_pdf = r"pdfs\CSD.pdf"
output_pattern = r"pdfs\output_part_{}.pdf"
pixel_range = ((40, 70), (60, 120))  # top-left (x1, y1) and bottom-right (x2, y2)
target_color = (197, 216, 241)  # RGB color to trigger a split

# Open the PDF
doc = fitz.open(input_pdf)

start_page = 0
part_number = 1

def save_part(start, end, number):
    """Save a PDF from start to end pages (inclusive)"""
    if end < start:
        return  # nothing to save
    new_pdf = fitz.open()
    for p in range(start, end + 1):
        new_pdf.insert_pdf(doc, from_page=p, to_page=p)
    new_pdf.save(output_pattern.format(number))
    new_pdf.close()

def pixel_in_range(img, top_left, bottom_right, target):
    """Check if the target color exists in the rectangle"""
    x1, y1 = top_left
    x2, y2 = bottom_right
    for x in range(x1, x2 + 1):
        for y in range(y1, y2 + 1):
            if img.getpixel((x, y))[:3] == target:
                return True
    return False

for page_number in range(len(doc)):
    page = doc[page_number]

    # Render page to image
    pix = page.get_pixmap()
    img = Image.open(io.BytesIO(pix.tobytes()))

    # Check if the target color exists in the range
    if pixel_in_range(img, pixel_range[0], pixel_range[1], target_color):
        # Save pages from start_page to page before current
        save_part(start_page, page_number - 1, part_number)
        part_number += 1
        # New part starts from current page
        start_page = page_number

# Save remaining pages after last split
save_part(start_page, len(doc) - 1, part_number)

doc.close()
print("Done splitting PDF.")
