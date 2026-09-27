import fitz
import os
import glob

cert_files = glob.glob('certificates/*.pdf')
print(f"Found {len(cert_files)} PDFs in certificates/")

for pdf_file in cert_files:
    basename = os.path.basename(pdf_file)
    doc = fitz.open(pdf_file)
    page = doc[0]
    
    # Render to PNG
    pix = page.get_pixmap(dpi=150)
    png_path = pdf_file.replace('.pdf', '_rendered.png')
    pix.save(png_path)
    
    doc.close()
print("Rendered all.")
