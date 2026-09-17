import csv
import os

def generate_report(output_dir, results):
    report_path = os.path.join(output_dir, "generation_report.csv")
    with open(report_path, 'w', newline='', encoding='utf-8') as f:
        writer = csv.writer(f)
        writer.writerow(['Reg No', 'Name', 'Status', 'Output File', 'Message'])
        for r in results:
            writer.writerow([r['reg_no'], r['name'], r['status'], r['output_file'], r['message']])
            
    return report_path
