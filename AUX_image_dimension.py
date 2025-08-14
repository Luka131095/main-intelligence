import fitz  # PyMuPDF

# === CONFIGURATION ===
pdf_path = "/Users/lvrzogic/Documents/Dokumenti/Project Management/Downstream Project and Portfolio Management_cleaned.pdf"
page_index = 3  # Page 2 (indexing starts at 0)

doc = fitz.open(pdf_path)
page = doc[page_index]

# Extract page content as a structured dictionary
blocks = page.get_text("dict")["blocks"]

image_count = 0

for block in blocks:
    if block["type"] == 1:  # type 1 = image block
        image_count += 1
        bbox = block["bbox"]
        width = bbox[2] - bbox[0]
        height = bbox[3] - bbox[1]
        
        print(f"🖼 Image {image_count}:")
        print(f"   - BBox: {bbox}")
        print(f"   - Width x Height: {width:.2f} x {height:.2f}\n")

doc.close()

print(f"🔍 Total images found on page 2: {image_count}")