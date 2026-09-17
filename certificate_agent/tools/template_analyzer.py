import fitz
import os
import glob

def find_serif_font():
    fonts_dirs = [r"C:\Windows\Fonts"]
    preferred_fonts = [
        "georgia.ttf", "times.ttf", "liberationserif-regular.ttf", "dejavuserif.ttf"
    ]
    for d in fonts_dirs:
        for p in preferred_fonts:
            path = os.path.join(d, p)
            if os.path.exists(path):
                return path
    return None

def analyze_template(template_path):
    doc = fitz.open(template_path)
    
    if template_path.lower().endswith(('.png', '.jpg', '.jpeg')):
        pdf_bytes = doc.convert_to_pdf()
        doc = fitz.open("pdf", pdf_bytes)
        
    page = doc[0]
    rect = page.rect
    width, height = rect.width, rect.height
    
    font_path = find_serif_font()
    
    coords = {
        'name': {'x': 576.375, 'y': 313.0, 'align': 'center', 'size': 42},
        'university': {'x': 576.0, 'y': 430.0, 'align': 'center', 'size': 32},
        'reg_no': {'x': 264.75, 'y': 658.0, 'align': 'center', 'size': 26},
        'date': {'x': 922.875, 'y': 658.0, 'align': 'center', 'size': 26}
    }
    
    return {
        'width': width,
        'height': height,
        'coords': coords,
        'is_image': template_path.lower().endswith(('.png', '.jpg', '.jpeg')),
        'pdf_bytes': doc.write() if template_path.lower().endswith(('.png', '.jpg', '.jpeg')) else None,
        'font_path': font_path
    }
