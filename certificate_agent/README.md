# Automated Certificate Generation Agent

## Overview
This agent automates the process of generating certificates for students from an Excel dataset using a visual template. It automatically detects the Excel and template files, processes student records, robustly positions text, adapts font size for long names, and generates final PDF certificates preserving the original template's quality.

## Input
Simply place the following in the project root:
1. One Excel file containing student data (e.g., `certificate_student_data.xlsx`)
2. One Certificate sample/template (e.g., `Certificate.png` or a PDF)

## Automatic Detection
You do not need to configure any filenames. The agent will automatically scan the current directory to discover the `.xlsx` and template (`.pdf`, `.png`, `.jpg`, etc.) files.

## Excel Format
The Excel file must contain columns for Registration Number and Name.
Supported column variations include:
- Reg No: `Reg No`, `RegNo`, `REG NO`, `Registration No`, `Registration Number`, `Reg Number`
- Name: `Name`, `Student Name`, `StudentName`, `Student_Name`

Optional columns:
- University/Honors: Anything with `university` or `honors` in the header
- Date: Anything with `awarded` or `date` in the header

## Template Support
Supported formats: `.pdf`, `.png`, `.jpg`, `.jpeg`
The agent uses PyMuPDF (`pymupdf`) to process templates. If an image is provided, it is automatically converted into a high-quality PDF page of the exact aspect ratio and dimensions, acting as a visual background layer with the dynamic text rendered natively on top.

## Font Handling
The agent dynamically calculates text width and gradually reduces font size to accommodate exceptionally long student names or registration numbers, ensuring they never overflow the designated areas or overlap with borders.

## Validation
After generation, each PDF is validated to ensure:
- The file exists and is not empty.
- The page count and dimensions strictly match the template.
- The expected dynamic student name and registration number text is successfully extractable from the generated PDF.

## Running
From the directory containing the excel and template files, simply run:
```bash
python certificate_agent/main.py
```

## Output
All generated certificates will be stored safely in the `./certificates/` directory.

## Errors and Reporting
A comprehensive report is generated at `./certificates/generation_report.csv` detailing the outcome for every student record, including the specific failure reason if an issue occurs.
