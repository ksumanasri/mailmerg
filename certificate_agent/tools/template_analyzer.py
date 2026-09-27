import fitz
import os
import glob

def find_serif_font():
    current_dir = os.path.dirname(__file__)
    font_path = os.path.join(current_dir, "..", "fonts", "Georgia.ttf")
    if os.path.exists(font_path):
        return font_path
    return None


def find_signature_font():
    windows_dir = os.environ.get('WINDIR', r'C:\Windows')
    font_dir = os.path.join(windows_dir, 'Fonts')
    for filename in ('VIVALDII.TTF', 'KUNSTLER.TTF', 'BRUSHSCI.TTF', 'segoesc.ttf'):
        signature_path = os.path.join(font_dir, filename)
        if os.path.exists(signature_path):
            return signature_path
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
    signature_font_path = find_signature_font()
    
    coords = {
        'name': {'x': 575.0, 'y': 317.0, 'align': 'center', 'size': 38, 'max_width': width * 0.62},
        'university': {'x': 575.0, 'y': 436.0, 'align': 'center', 'size': 30, 'max_width': width * 0.72},
        'left_signatory': {'x': 264.0, 'y': 530.0, 'align': 'center', 'size': 22, 'max_width': width * 0.28},
        'right_signatory': {'x': 920.0, 'y': 530.0, 'align': 'center', 'size': 22, 'max_width': width * 0.28},
        'reg_no': {'x': 264.0, 'y': 664.0, 'align': 'center', 'size': 23, 'max_width': width * 0.28},
        'date': {'x': 920.0, 'y': 664.0, 'align': 'center', 'size': 23, 'max_width': width * 0.28}
    }
    
    return {
        'width': width,
        'height': height,
        'coords': coords,
        'is_image': template_path.lower().endswith(('.png', '.jpg', '.jpeg')),
        'pdf_bytes': doc.write() if template_path.lower().endswith(('.png', '.jpg', '.jpeg')) else None,
        'font_path': font_path
        , 'signature_font_path': signature_font_path
    }
