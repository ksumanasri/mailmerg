# Automated Certificate Generation Agent

## Overview
This project creates personalized student completion certificates from an Excel file and a certificate template. It is designed around the sample certificate layout shown in the repository: the generated PDF fills the name, university, certificate ID, and award date into the same blank positions used in the design.

## Sample certificate layout
The generator is tuned for the template used in this project, which follows this structure:
- Title: CERTIFICATE OF COMPLETION
- Intro text: This is to certify that
- Student name line
- Text: Graduated with honors from
- University line
- Center award seal: Awarded / year
- Left signature: John
- Right signature: Moses
- Bottom left: Certificate ID
- Bottom right: Awarded on

## Required Excel columns
The workbook should contain these headers:
- Reg No
- Name
- Graduated with honors from
- Awarded on

The parser also accepts common variations such as:
- Registration Number / Registration No
- Student Name
- University / College / Institute
- Award Date / Awarded Date

## Features
- Streamlit web interface for upload and generation
- Automatic column detection for the sample certificate format
- Support for `.pdf`, `.png`, `.jpg`, and `.jpeg` templates
- Dynamic text placement with adjusted font sizing for longer names
- Date normalization to `DD-MM-YYYY` format
- PDF validation and generation report output
- ZIP download of all generated certificate files

## Folder structure
- `app.py` – Streamlit app entry point
- `certificate_agent/` – generator logic and utility modules
- `certificates/` – generated PDFs and CSV report
- `Certificate.png` – sample certificate template used for output layout

## Installation
```bash
pip install -r requirements.txt
```

## Run locally
```bash
streamlit run app.py
```

## Usage
1. Upload the Excel file with student details.
2. Upload the certificate template image or PDF.
3. Preview the detected records.
4. Generate and download the final PDFs.

The app reads the student data and fills the blanks into the template positions automatically. The output files are saved in the `certificates/` folder.

## Notes
- The date field is normalized to `DD-MM-YYYY` to match the template style.
- The generated filenames use the registration number and student name, for example `2026002_Priya_Sharma.pdf`.
- The two signature blanks are filled consistently with `John` on the left and `Moses` on the right.
- John and Moses use a calligraphic signature font when available on Windows, with an italic fallback on other platforms.
- This project is intended for local generation and preview. Keep student data and generated PDFs out of source control if they are private.
