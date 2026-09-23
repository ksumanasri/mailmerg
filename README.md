# Automated Certificate Generation Agent

## Overview
This agent automates the process of generating certificates for students from an Excel dataset using a visual template. It provides a user-friendly Streamlit web application where users can upload an Excel file and a certificate template to dynamically generate personalized PDF certificates. 

## Features
- **Web UI:** Streamlit-based interface for easy file uploads and downloading results.
- **Robust Field Detection:** Intelligently maps Excel columns (Reg No, Name, University, Date).
- **Template Support:** Supports `.pdf`, `.png`, `.jpg`, `.jpeg` formats.
- **Adaptive Text:** Automatically calculates text width and scales font sizes.
- **Validation:** Every generated PDF is validated to ensure correctness.
- **Bulk Download:** Provides a ZIP file of all generated certificates.

## Architecture
- **Framework:** Streamlit
- **PDF Processing:** PyMuPDF (`pymupdf`)
- **Data Handling:** pandas, openpyxl
- **Deployment:** Streamlit Community Cloud (Linux compatible)

## Installation & Local Run
Clone the repository and install dependencies:
```bash
pip install -r requirements.txt
```
Run the application locally:
```bash
streamlit run app.py
```

## Streamlit Deployment Instructions
This project is fully compatible with Streamlit Community Cloud.
1. Connect your GitHub repository to Streamlit Cloud.
2. Select `app.py` as the main file path.
3. Deploy! The application uses local fonts and dynamic paths. No Windows-specific logic or local absolute paths are required. GitHub Pages is NOT used for running this Python application.

## Security & Privacy
- Uploaded files are processed in a temporary directory and are not stored permanently.
- Never commit private `.env` files, API keys, student Excel data, or generated PDFs to the repository. The `.gitignore` is configured to ignore these files.
