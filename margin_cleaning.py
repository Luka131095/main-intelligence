import fitz  # PyMuPDF
import os

# === CONFIGURATION ===
pdf_path = "/Users/lvrzogic/Documents/Dokumenti/Project Management/Downstream Project and Portfolio Management.pdf"
output_path = "/Users/lvrzogic/Documents/Dokumenti/Project Management/Downstream Project and Portfolio Management_cleaned.pdf"

doc = fitz.open(pdf_path)

for page_num in range(len(doc)):
    page = doc[page_num]
    width, height = page.rect.width, page.rect.height

    is_landscape = width > height

    if is_landscape:
        top_limit = 74.2
        bottom_limit = 530.7
    else:
        top_limit = 74
        bottom_limit = 775

    # Create redaction rectangles
    top_rect = fitz.Rect(0, 0, width, top_limit)
    bottom_rect = fitz.Rect(0, bottom_limit, width, height)

    # Add redactions to page
    page.add_redact_annot(top_rect, fill=(1, 1, 1))
    page.add_redact_annot(bottom_rect, fill=(1, 1, 1))

    # ✅ Apply redactions on this page
    page.apply_redactions()

# Save cleaned PDF
doc.save(output_path, garbage=4, deflate=True, clean=True)
doc.close()

print(f"✅ Cleaned PDF saved to:\n{output_path}")