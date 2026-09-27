import os
import tempfile
import unittest

import fitz
import pandas as pd

from certificate_agent.tools.certificate_generator import generate_certificate
from certificate_agent.tools.excel_reader import read_students
from certificate_agent.tools.template_analyzer import analyze_template


ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
TEMPLATE = os.path.join(ROOT, 'Certificate.png')
class CertificateGenerationTests(unittest.TestCase):
    def _read_sample_records(self, temporary_directory):
        workbook = os.path.join(temporary_directory, 'sample_students.xlsx')
        pd.DataFrame([
            {
                'Reg No': '2026001',
                'Name': 'Ravi Kumar',
                'Graduated with honors from': 'Vignan University',
                'Awarded on': '17-09-2026',
            },
            {
                'Reg No': '2026002',
                'Name': 'Priya Sharma',
                'Graduated with honors from': 'Vignan University',
                'Awarded on': '17-09-2026',
            },
        ]).to_excel(workbook, index=False)
        return read_students(workbook)

    def test_sample_workbook_is_mapped_to_certificate_fields(self):
        with tempfile.TemporaryDirectory() as temporary_directory:
            records = self._read_sample_records(temporary_directory)

            self.assertGreaterEqual(len(records), 2)
            self.assertEqual(records[1]['reg_no'], '2026002')
            self.assertEqual(records[1]['name'], 'Priya Sharma')
            self.assertEqual(records[1]['university'], 'Vignan University')
            self.assertEqual(records[1]['date'], '17-09-2026')

    def test_generated_pdf_contains_all_personalized_fields_and_signatures(self):
        template_info = analyze_template(TEMPLATE)

        with tempfile.TemporaryDirectory() as output_dir:
            records = self._read_sample_records(output_dir)
            output_path = generate_certificate(records[1], TEMPLATE, template_info, output_dir)
            document = fitz.open(output_path)
            text = document[0].get_text().replace('\xa0', ' ').replace('\xad', '-')

            self.assertEqual(document.page_count, 1)
            for expected in ('Priya Sharma', 'Vignan University', '2026002', '17-09-2026', 'John', 'Moses'):
                self.assertIn(expected, text)
            document.close()

    def test_signature_font_falls_back_when_unavailable(self):
        template_info = analyze_template(TEMPLATE)
        self.assertIn('signature_font_path', template_info)
        self.assertTrue(template_info['signature_font_path'] is None or os.path.exists(template_info['signature_font_path']))


if __name__ == '__main__':
    unittest.main()