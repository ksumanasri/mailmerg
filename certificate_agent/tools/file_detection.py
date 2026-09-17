import os
import glob

def find_files():
    # Find Excel files
    excel_candidates = glob.glob("*.xlsx") + glob.glob("*.xls")
    excel_candidates = [f for f in excel_candidates if not f.startswith("~$")]
    
    # Find template files
    template_candidates = glob.glob("*.pdf") + glob.glob("*.png") + glob.glob("*.jpg") + glob.glob("*.jpeg") + glob.glob("*.docx")
    # Filter out generated test files we made
    template_candidates = [f for f in template_candidates if f not in ['test_cert.pdf', 'test_cert.png', 'test_cert2.png', 'test_cert3.png', 'test_cert4.png']]
    
    if not excel_candidates:
        raise FileNotFoundError("No Excel file found in the current directory.")
    if len(excel_candidates) > 1:
        raise ValueError(f"Ambiguous Excel files found: {excel_candidates}. Please ensure only one data file exists.")
        
    if not template_candidates:
        raise FileNotFoundError("No template file found in the current directory.")
    if len(template_candidates) > 1:
        # Prefer PDF if multiple
        pdf_cands = [f for f in template_candidates if f.endswith('.pdf')]
        if len(pdf_cands) == 1:
            template_file = pdf_cands[0]
        else:
            raise ValueError(f"Ambiguous template files found: {template_candidates}.")
    else:
        template_file = template_candidates[0]
        
    return excel_candidates[0], template_file
