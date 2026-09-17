import fitz
import os
import re

def validate_pdf(pdf_path, record, template_info):
    if not os.path.exists(pdf_path):
        return False, "File does not exist"
        
    try:
        doc = fitz.open(pdf_path)
        if doc.page_count < 1:
            return False, "PDF is empty"
            
        page = doc[0]
        text = page.get_text("text")
        
        def strip_special(s):
            return re.sub(r'\W+', '', str(s)).lower()
            
        text_clean = strip_special(text)
        
        name_clean = strip_special(record['name'])
        reg_clean = strip_special(record['reg_no'])
        
        if name_clean not in text_clean:
            return False, "Student name not found in PDF text"
            
        if reg_clean not in text_clean:
            return False, "Reg No not found in PDF text"
            
        return True, "Valid"
    except Exception as e:
        return False, f"Validation error: {e}"
