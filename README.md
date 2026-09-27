# Certificate Mail Merge

Generate polished, personalized PDF certificates from one Excel workbook and a reusable certificate template.

![Sample certificate template](Certificate.png)

## What it does

The Streamlit app reads each student record, places the values into the certificate template, validates the generated PDF, and provides individual downloads plus a ZIP archive.

The current template fills:

- Student name
- University or institution
- Certificate ID
- Award date
- Left signature: John
- Right signature: Moses

Long names are resized to stay inside the certificate layout. Dates are normalized to `DD-MM-YYYY`.

## Input format

Use an `.xlsx` or `.xls` workbook with these columns:

| Column | Example |
| --- | --- |
| `Reg No` | `2026002` |
| `Name` | `Priya Sharma` |
| `Graduated with honors from` | `Vignan University` |
| `Awarded on` | `17-09-2026` |

Common alternatives such as `Registration Number`, `Student Name`, `University`, `College`, `Institute`, `Award Date`, and `Awarded Date` are also detected automatically.

## Quick start

```bash
git clone https://github.com/ksumanasri/mailmerg.git
cd mailmerg
python -m venv .venv
```

Activate the environment:

```powershell
.venv\Scripts\Activate.ps1
```

Install dependencies and start the app:

```bash
pip install -r requirements.txt
streamlit run app.py
```

Open the local Streamlit URL, upload the student workbook and template, review the detected records, and select **Generate Certificates**.

## Supported templates

The app accepts `.pdf`, `.png`, `.jpg`, and `.jpeg` certificate templates. The included `Certificate.png` shows the layout used by the coordinate-based sample generator.

## Project structure

```text
app.py                              Streamlit interface
certificate_agent/tools/            Excel, template, PDF, and report utilities
Certificate.png                     Public sample template
tests/                              Automated generation tests
requirements.txt                    Python dependencies
```

Generated PDFs and reports are written to a session output directory by the web app. The command-line workflow in `certificate_agent/main.py` writes to `certificates/`.

## Testing

Run the self-contained test suite from the project root:

```bash
python -m unittest discover -s tests -v
```

The tests cover Excel field mapping, date normalization, PDF generation, required output text, signatures, and font fallback behavior.

## Design details

- PDF processing uses PyMuPDF.
- Excel parsing uses pandas and openpyxl.
- Signature rendering prefers an installed calligraphic font and falls back to an italic built-in font.
- Generated PDFs are checked before they are reported as successful.
- Output filenames follow the pattern `REG_NO_Name.pdf`, for example `2026002_Priya_Sharma.pdf`.

## Privacy and Git hygiene

Student workbooks and generated certificates may contain personal information. Do not commit them to GitHub. The repository ignores private Excel files, generated PDFs, previews, and temporary verification folders. Only the public sample template is included for demonstration.
