import streamlit as st
import os
import sys
import tempfile
import zipfile
import pandas as pd
from pathlib import Path

# Add certificate_agent to path so we can import from it
sys.path.append(os.path.join(os.path.dirname(__file__), "certificate_agent"))

from tools.excel_reader import read_students
from tools.template_analyzer import analyze_template
from tools.certificate_generator import generate_certificate
from tools.pdf_validator import validate_pdf
from tools.report_generator import generate_report

st.set_page_config(page_title="Certificate Generation Agent", layout="wide")

st.title("Certificate Generation Agent")
st.write("Automatically generate personalized PDF certificates from student Excel data and a certificate template.")

# Temporary directory for session
if 'temp_dir' not in st.session_state:
    st.session_state.temp_dir = tempfile.mkdtemp()

st.header("1. Upload Student Excel File")
excel_file = st.file_uploader("Upload Excel (.xlsx, .xls)", type=["xlsx", "xls"])

st.header("2. Upload Certificate Template")
template_file = st.file_uploader("Upload Template (.png, .jpg, .jpeg, .pdf)", type=["png", "jpg", "jpeg", "pdf"])

records = []
if excel_file is not None:
    # Save excel to temp
    temp_excel_path = os.path.join(st.session_state.temp_dir, excel_file.name)
    with open(temp_excel_path, "wb") as f:
        f.write(excel_file.getbuffer())
    
    try:
        records = read_students(temp_excel_path)
        st.header("3. Preview Student Records")
        st.write(f"Detected {len(records)} valid student records.")
        st.dataframe(pd.DataFrame(records))
    except Exception as e:
        st.error(f"Error reading Excel: {str(e)}")
        records = []

if excel_file is not None and template_file is not None and len(records) > 0:
    st.header("4. Generate Certificates")
    
    if st.button("Generate Certificates"):
        temp_template_path = os.path.join(st.session_state.temp_dir, template_file.name)
        with open(temp_template_path, "wb") as f:
            f.write(template_file.getbuffer())
            
        out_dir = os.path.join(st.session_state.temp_dir, "certificates")
        os.makedirs(out_dir, exist_ok=True)
        
        try:
            template_info = analyze_template(temp_template_path)
        except Exception as e:
            st.error(f"Error analyzing template: {e}")
            st.stop()
            
        progress_bar = st.progress(0)
        status_text = st.empty()
        
        results = []
        success_count = 0
        fail_count = 0
        
        for i, rec in enumerate(records):
            status_text.text(f"Generating certificate {i+1} of {len(records)}...")
            try:
                out_path = generate_certificate(rec, temp_template_path, template_info, out_dir)
                is_valid, msg = validate_pdf(out_path, rec, template_info)
                
                if is_valid:
                    results.append({
                        'Student': rec['name'],
                        'Reg No': rec['reg_no'],
                        'Output File': os.path.basename(out_path),
                        'Status': 'SUCCESS',
                        'Validation': 'PASS',
                        'Error Message': ''
                    })
                    success_count += 1
                else:
                    results.append({
                        'Student': rec['name'],
                        'Reg No': rec['reg_no'],
                        'Output File': os.path.basename(out_path),
                        'Status': 'FAILED',
                        'Validation': 'FAIL',
                        'Error Message': msg
                    })
                    fail_count += 1
                    
            except Exception as e:
                results.append({
                    'Student': rec['name'],
                    'Reg No': rec['reg_no'],
                    'Output File': '',
                    'Status': 'FAILED',
                    'Validation': 'FAIL',
                    'Error Message': f"Generation error: {e}"
                })
                fail_count += 1
                
            progress_bar.progress((i + 1) / len(records))
            
        status_text.text(f"Generation complete! {success_count} generated, {fail_count} failed.")
        
        # Save CSV report manually matching requested columns
        report_path = os.path.join(out_dir, "generation_report.csv")
        df_results = pd.DataFrame(results)
        # Rename to match prompt: Reg No, Name, Output File, Status, Validation Status, Error Message
        df_results = df_results.rename(columns={'Student': 'Name', 'Validation': 'Validation Status'})
        df_results = df_results[['Reg No', 'Name', 'Output File', 'Status', 'Validation Status', 'Error Message']]
        df_results.to_csv(report_path, index=False)
        
        st.header("5. Validation Results")
        st.dataframe(df_results)
        
        st.header("6. Download Generated Certificates")
        
        # Create ZIP
        zip_path = os.path.join(st.session_state.temp_dir, "generated_certificates.zip")
        with zipfile.ZipFile(zip_path, 'w', zipfile.ZIP_DEFLATED) as zipf:
            for root, _, files in os.walk(out_dir):
                for file in files:
                    if file.endswith('.pdf'):
                        file_path = os.path.join(root, file)
                        # Add to certificates folder in zip
                        zipf.write(file_path, os.path.join("certificates", file))
        
        with open(zip_path, "rb") as f:
            st.download_button(
                label="Download All Certificates (ZIP)",
                data=f,
                file_name="generated_certificates.zip",
                mime="application/zip"
            )
            
        with open(report_path, "rb") as f:
            st.download_button(
                label="Download Generation Report (CSV)",
                data=f,
                file_name="generation_report.csv",
                mime="text/csv"
            )
