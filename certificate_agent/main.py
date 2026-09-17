import os
import sys

from tools.file_detection import find_files
from tools.excel_reader import read_students
from tools.template_analyzer import analyze_template
from tools.certificate_generator import generate_certificate
from tools.pdf_validator import validate_pdf
from tools.report_generator import generate_report

def main():
    print("Starting Automated Certificate Generation Agent...")
    
    # 1. Detect Files
    try:
        excel_file, template_file = find_files()
        print(f"Detected Excel: {excel_file}")
        print(f"Detected Template: {template_file}")
    except Exception as e:
        print(f"Error finding files: {e}")
        sys.exit(1)
        
    # 2. Read Students
    try:
        records = read_students(excel_file)
        print(f"Students found/Valid records: {len(records)}")
    except Exception as e:
        print(f"Error reading Excel: {e}")
        sys.exit(1)
        
    if not records:
        print("No valid student records found.")
        sys.exit(1)
        
    # 3. Analyze Template
    try:
        template_info = analyze_template(template_file)
        print(f"Template analyzed. Dimensions: {template_info['width']}x{template_info['height']}")
    except Exception as e:
        print(f"Error analyzing template: {e}")
        sys.exit(1)
        
    # 4. Output Directory
    out_dir = os.path.join(os.getcwd(), "certificates")
    if not os.path.exists(out_dir):
        os.makedirs(out_dir)
        
    # 5. Generate and Validate
    results = []
    success_count = 0
    fail_count = 0
    
    print("Generating certificates...")
    for rec in records:
        try:
            out_path = generate_certificate(rec, template_file, template_info, out_dir)
            is_valid, msg = validate_pdf(out_path, rec, template_info)
            
            if is_valid:
                results.append({
                    'reg_no': rec['reg_no'],
                    'name': rec['name'],
                    'status': 'Success',
                    'output_file': os.path.basename(out_path),
                    'message': ''
                })
                success_count += 1
            else:
                results.append({
                    'reg_no': rec['reg_no'],
                    'name': rec['name'],
                    'status': 'Failed',
                    'output_file': os.path.basename(out_path),
                    'message': msg
                })
                fail_count += 1
                
        except Exception as e:
            results.append({
                'reg_no': rec['reg_no'],
                'name': rec['name'],
                'status': 'Failed',
                'output_file': '',
                'message': f"Generation error: {e}"
            })
            fail_count += 1
            
    # 6. Report
    report_file = generate_report(out_dir, results)
    
    # 7. Final Summary
    print("\nCertificate generation completed" + (" with errors." if fail_count > 0 else "."))
    print(f"Students found:       {len(records)}")
    print(f"Valid records:        {len(records)}")
    print(f"Certificates created: {success_count}")
    print(f"Failed:               {fail_count}")
    print(f"\nTemplate:\n{template_file}")
    print(f"\nOutput directory:\n./certificates/")
    if fail_count == 0:
        print(f"\nReport:\n./certificates/generation_report.csv")
        print("\nAll certificates successfully generated and validated.")
    else:
        print(f"\nReview:\n./certificates/generation_report.csv")

if __name__ == "__main__":
    main()
