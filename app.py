import streamlit as st
import os
import sys
import tempfile
import zipfile
import pandas as pd
from pathlib import Path
import time
import base64

# Add certificate_agent to path so we can import from it
sys.path.append(os.path.join(os.path.dirname(__file__), "certificate_agent"))

from tools.excel_reader import read_students
from tools.template_analyzer import analyze_template
from tools.certificate_generator import generate_certificate
from tools.pdf_validator import validate_pdf
from tools.report_generator import generate_report

# Setup Page
st.set_page_config(page_title="Certificate Generation Agent", page_icon="🎓", layout="wide")

# Custom CSS for Modern SaaS UI
css = """
<style>
    /* Main Layout */
    .stApp {
        background-color: #f8fafc;
        font-family: 'Inter', -apple-system, BlinkMacSystemFont, sans-serif;
    }
    
    /* Top Navigation (Faked) */
    .top-nav {
        display: flex;
        justify-content: space-between;
        align-items: center;
        padding: 10px 0 20px 0;
        margin-bottom: 20px;
        border-bottom: 1px solid #e2e8f0;
    }
    .top-nav a {
        text-decoration: none;
        color: #475569;
        font-weight: 500;
        margin-right: 20px;
        transition: color 0.2s;
    }
    .top-nav a:hover {
        color: #3b82f6;
    }
    
    /* Hero Section */
    .hero {
        background: linear-gradient(135deg, #eff6ff 0%, #f5f3ff 100%);
        border-radius: 16px;
        padding: 40px;
        text-align: center;
        box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.05), 0 2px 4px -1px rgba(0, 0, 0, 0.03);
        margin-bottom: 30px;
        border: 1px solid #e0e7ff;
    }
    .hero h1 {
        background: -webkit-linear-gradient(45deg, #3b82f6, #8b5cf6);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        font-size: 3em;
        font-weight: 800;
        margin-bottom: 10px;
    }
    .hero p {
        color: #475569;
        font-size: 1.2em;
        max-width: 600px;
        margin: 0 auto;
    }
    
    /* Cards */
    div[data-testid="stVerticalBlock"] > div > div > div[data-testid="stVerticalBlock"] {
        background-color: white;
        border-radius: 12px;
        padding: 24px;
        box-shadow: 0 1px 3px 0 rgba(0, 0, 0, 0.1), 0 1px 2px 0 rgba(0, 0, 0, 0.06);
        border: 1px solid #e2e8f0;
        transition: transform 0.2s, box-shadow 0.2s;
    }
    div[data-testid="stVerticalBlock"] > div > div > div[data-testid="stVerticalBlock"]:hover {
        box-shadow: 0 10px 15px -3px rgba(0, 0, 0, 0.1), 0 4px 6px -2px rgba(0, 0, 0, 0.05);
    }
    
    /* Upload Areas */
    .stFileUploader {
        border-radius: 12px;
    }
    
    /* Buttons */
    .stButton > button {
        background: linear-gradient(to right, #3b82f6, #8b5cf6) !important;
        color: white !important;
        border: none !important;
        border-radius: 8px !important;
        padding: 0.5rem 2rem !important;
        font-weight: 600 !important;
        box-shadow: 0 4px 6px -1px rgba(59, 130, 246, 0.3) !important;
        transition: all 0.3s ease !important;
    }
    .stButton > button:hover {
        transform: translateY(-2px) !important;
        box-shadow: 0 6px 8px -1px rgba(59, 130, 246, 0.4) !important;
    }
    
    /* Steps */
    .step-indicator {
        display: flex;
        justify-content: center;
        align-items: center;
        gap: 15px;
        margin: 20px 0 40px 0;
        font-weight: 500;
        color: #64748b;
    }
    .step-active {
        color: #3b82f6;
        font-weight: 700;
    }
    .step-done {
        color: #10b981;
    }
    
    /* Footer */
    .sidebar-footer {
        margin-top: auto;
        padding-top: 20px;
        text-align: center;
        color: #64748b;
        font-size: 0.85em;
    }
    
    .ready-card {
        background-color: #ecfdf5;
        border: 1px solid #10b981;
        border-radius: 12px;
        padding: 20px;
        text-align: center;
        margin-top: 20px;
    }
</style>
"""
st.markdown(css, unsafe_allow_html=True)

# State initialization
if 'temp_dir' not in st.session_state:
    st.session_state.temp_dir = tempfile.mkdtemp()
if 'history' not in st.session_state:
    st.session_state.history = []
if 'page' not in st.session_state:
    st.session_state.page = "Generate Certificates"
if 'last_results' not in st.session_state:
    st.session_state.last_results = None
if 'zip_path' not in st.session_state:
    st.session_state.zip_path = None
if 'report_path' not in st.session_state:
    st.session_state.report_path = None

# Top Navigation Faked UI
st.markdown("""
<div class="top-nav">
    <div>
        <strong>🎓 Certificate Generation Agent</strong> | <em>Automate • Personalize • Deliver</em>
    </div>
    <div>
        <a href="#">Home</a>
        <a href="#">How to Use</a>
        <a href="#">About</a>
        <a href="https://github.com/ksumanasri/mailmerg" target="_blank">View on GitHub</a>
    </div>
</div>
""", unsafe_allow_html=True)

# Sidebar
with st.sidebar:
    st.header("Navigation")
    if st.button("🏠 Generate Certificates", use_container_width=True):
        st.session_state.page = "Generate Certificates"
    if st.button("🖼 Preview & Validate", use_container_width=True):
        st.session_state.page = "Preview & Validate"
    if st.button("⬇ Downloads", use_container_width=True):
        st.session_state.page = "Downloads"
    if st.button("🕘 History", use_container_width=True):
        st.session_state.page = "History"
    if st.button("❓ Help & FAQ", use_container_width=True):
        st.session_state.page = "Help & FAQ"
    if st.button("ℹ️ About", use_container_width=True):
        st.session_state.page = "About"
        
    st.markdown("""
    <div class="sidebar-footer">
        <p>"Every achievement deserves a certificate."<br/>"Let's make it happen!"</p>
        <p>Built with ❤️<br/>for students & educators</p>
    </div>
    """, unsafe_allow_html=True)

# Main Content Routing
page = st.session_state.page

def show_step_indicator(step):
    steps = [
        "1 Upload Files",
        "2 Preview & Validate",
        "3 Generate",
        "4 Download"
    ]
    html = '<div class="step-indicator">'
    for i, s in enumerate(steps):
        if i + 1 < step:
            html += f'<span class="step-done">{s} ✓</span>'
        elif i + 1 == step:
            html += f'<span class="step-active">{s}</span>'
        else:
            html += f'<span>{s}</span>'
        if i < 3:
            html += ' <span>→</span> '
    html += '</div>'
    st.markdown(html, unsafe_allow_html=True)

if page == "Generate Certificates":
    st.markdown("""
    <div class="hero">
        <h1>Certificate Generation Agent</h1>
        <p>Automatically generate personalized PDF certificates from student Excel data and a certificate template.</p>
    </div>
    """, unsafe_allow_html=True)
    
    show_step_indicator(1)
    
    col1, col2 = st.columns(2)
    with col1:
        st.markdown("### 📊 1. Upload Student Excel File")
        st.markdown("Upload your Excel file containing student details.")
        excel_file = st.file_uploader("Drag & drop your Excel file here or click to browse", type=["xlsx", "xls"], key="excel")
        if excel_file:
            st.success(f"Uploaded: {excel_file.name} ({excel_file.size} bytes)")
            
    with col2:
        st.markdown("### 🖼 2. Upload Certificate Template")
        st.markdown("Upload your certificate template image or PDF.")
        template_file = st.file_uploader("Drag & drop template here or click to browse", type=["png", "jpg", "jpeg", "pdf"], key="template")
        if template_file:
            st.success(f"Uploaded: {template_file.name} ({template_file.size} bytes)")
            
    if excel_file and template_file:
        st.markdown("""
        <div class="ready-card">
            <h3 style="color: #047857; margin-top:0;">🚀 Ready to Generate!</h3>
            <p style="color: #065f46;">Upload both files to preview and validate your data.</p>
            <p style="font-size: 0.9em; color: #10b981;">🔒 Your files are processed securely and are not stored permanently.</p>
        </div>
        """, unsafe_allow_html=True)
        if st.button("Preview & Validate Data →", use_container_width=True):
            st.session_state.excel_file = excel_file
            st.session_state.template_file = template_file
            st.session_state.page = "Preview & Validate"
            st.rerun()

elif page == "Preview & Validate":
    show_step_indicator(2)
    st.markdown("## 3. Preview Student Records")
    st.markdown("Review the extracted student data. Make sure the required columns are correctly detected.")
    
    excel_file = st.session_state.get('excel_file', None)
    template_file = st.session_state.get('template_file', None)
    
    if excel_file is None or template_file is None:
        st.warning("Please upload both Excel and Template files on the 'Generate Certificates' page first.")
        st.button("← Back to Upload", on_click=lambda: st.session_state.update(page="Generate Certificates"))
    else:
        temp_excel_path = os.path.join(st.session_state.temp_dir, excel_file.name)
        with open(temp_excel_path, "wb") as f:
            f.write(excel_file.getvalue())
            
        try:
            records = read_students(temp_excel_path)
            st.markdown("<span style='background-color:#d1fae5; color:#065f46; padding: 4px 8px; border-radius: 4px; font-weight:bold;'>✓ Columns detected automatically!</span>", unsafe_allow_html=True)
            
            st.button("Refresh Preview")
            
            col1, col2 = st.columns([3, 1])
            with col1:
                df = pd.DataFrame(records)
                st.dataframe(df, use_container_width=True)
            
            with col2:
                st.markdown("### Statistics")
                st.info(f"**{len(records)}**\nTotal Students")
                st.success(f"**{len(records)}**\nValid Records")
                st.error(f"**0**\nInvalid Records")
                
            st.markdown("---")
            if st.button("⚙ Generate Certificates →"):
                # Run Generation
                temp_template_path = os.path.join(st.session_state.temp_dir, template_file.name)
                with open(temp_template_path, "wb") as f:
                    f.write(template_file.getvalue())
                    
                out_dir = os.path.join(st.session_state.temp_dir, "certificates")
                os.makedirs(out_dir, exist_ok=True)
                
                template_info = analyze_template(temp_template_path)
                
                progress_container = st.container()
                with progress_container:
                    st.markdown("### Generating Certificates...")
                    p_text = st.empty()
                    p_bar = st.progress(0)
                    
                    p_text.markdown("Step 1: Reading student data ✓<br/>Step 2: Analyzing certificate template ✓<br/>Step 3: Generating certificates ⟳", unsafe_allow_html=True)
                    
                    results = []
                    success_count = 0
                    fail_count = 0
                    
                    for i, rec in enumerate(records):
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
                                    'Error Message': '',
                                    'Path': out_path
                                })
                                success_count += 1
                            else:
                                results.append({
                                    'Student': rec['name'],
                                    'Reg No': rec['reg_no'],
                                    'Output File': os.path.basename(out_path),
                                    'Status': 'FAILED',
                                    'Validation': 'FAIL',
                                    'Error Message': msg,
                                    'Path': out_path
                                })
                                fail_count += 1
                        except Exception as e:
                            results.append({
                                'Student': rec['name'],
                                'Reg No': rec['reg_no'],
                                'Output File': '',
                                'Status': 'FAILED',
                                'Validation': 'FAIL',
                                'Error Message': str(e),
                                'Path': ''
                            })
                            fail_count += 1
                            
                        p_bar.progress((i + 1) / len(records))
                        
                p_text.markdown(f"Step 4: Validating PDFs ✓<br/><br/>**{success_count} / {len(records)} certificates generated**", unsafe_allow_html=True)
                
                # Create Report & ZIP
                report_path = os.path.join(out_dir, "generation_report.csv")
                df_results = pd.DataFrame(results)
                df_export = df_results[['Reg No', 'Student', 'Output File', 'Status', 'Validation', 'Error Message']].copy()
                df_export = df_export.rename(columns={'Student': 'Name', 'Validation': 'Validation Status'})
                df_export.to_csv(report_path, index=False)
                
                zip_path = os.path.join(st.session_state.temp_dir, "generated_certificates.zip")
                with zipfile.ZipFile(zip_path, 'w', zipfile.ZIP_DEFLATED) as zipf:
                    for root, _, files in os.walk(out_dir):
                        for file in files:
                            if file.endswith('.pdf'):
                                zipf.write(os.path.join(root, file), os.path.join("certificates", file))
                                
                st.session_state.last_results = results
                st.session_state.zip_path = zip_path
                st.session_state.report_path = report_path
                
                st.session_state.history.append({
                    'date': time.strftime('%d %b %Y %H:%M'),
                    'total': len(records),
                    'passed': success_count,
                    'failed': fail_count
                })
                
                st.session_state.page = "Downloads"
                st.rerun()
                
        except Exception as e:
            st.error(f"Error reading Excel: {str(e)}")

elif page == "Downloads":
    show_step_indicator(4)
    if st.session_state.last_results is None:
        st.warning("No generated certificates available. Please generate them first.")
    else:
        results = st.session_state.last_results
        success_count = sum(1 for r in results if r['Validation'] == 'PASS')
        
        st.markdown(f"""
        <div class="ready-card" style="background-color:#eff6ff; border-color:#3b82f6;">
            <h2 style="color:#1d4ed8; margin-top:0;">🎉 Certificates Generated Successfully!</h2>
            <p>{len(results)} certificates generated</p>
            <p>{success_count} certificates validated</p>
        </div>
        """, unsafe_allow_html=True)
        
        st.markdown("### Download All")
        col1, col2 = st.columns(2)
        with col1:
            with open(st.session_state.zip_path, "rb") as f:
                st.download_button("⬇ Download All ZIP", f, file_name="generated_certificates.zip", mime="application/zip", use_container_width=True)
        with col2:
            with open(st.session_state.report_path, "rb") as f:
                st.download_button("⬇ Download Report CSV", f, file_name="generation_report.csv", mime="text/csv", use_container_width=True)
                
        st.markdown("### PDF Validation Results")
        
        val_df = pd.DataFrame(results)[['Student', 'Output File', 'Status', 'Validation']]
        val_df['Validation'] = val_df['Validation'].apply(lambda x: '✓ PASS' if x == 'PASS' else '✕ FAILED')
        st.dataframe(val_df, use_container_width=True)
        
        st.markdown(f"**Summary:** Generated: {len(results)} | Passed: {success_count} | Failed: {len(results)-success_count}")
        
        st.markdown("### Individual Certificates")
        for r in results:
            if r['Status'] == 'SUCCESS':
                with open(r['Path'], "rb") as f:
                    st.download_button(f"⬇ {r['Output File']}", f, file_name=r['Output File'], mime="application/pdf", key=r['Output File'])

elif page == "History":
    st.markdown("## 🕘 Session History")
    if not st.session_state.history:
        st.info("No certificates generated in this session yet.")
    else:
        for i, run in enumerate(reversed(st.session_state.history)):
            st.markdown(f"""
            <div style="border:1px solid #e2e8f0; border-radius:8px; padding:15px; margin-bottom:10px;">
                <h4>Generation #{len(st.session_state.history) - i}</h4>
                <p><strong>Date:</strong> {run['date']}</p>
                <p>{run['total']} certificates | {run['passed']} passed | {run['failed']} failed</p>
            </div>
            """, unsafe_allow_html=True)
            
elif page == "Help & FAQ":
    st.markdown("## ❓ Help & FAQ")
    
    with st.expander("How do I prepare the Excel file?"):
        st.write("Ensure your Excel file has a column for the student's name and registration number. The system will auto-detect columns with similar keywords.")
        
    with st.expander("What columns are required?"):
        st.write("Required: Name (e.g., 'Student Name'), Registration Number (e.g., 'Reg No'). Optional: University, Date.")
        
    with st.expander("What certificate templates are supported?"):
        st.write("We support `.png`, `.jpg`, `.jpeg`, and `.pdf` files. Images are converted into high-quality PDFs preserving proportions.")
        
    with st.expander("Where are generated certificates downloaded?"):
        st.write("Certificates are generated in a temporary session directory and can be downloaded immediately as a ZIP file or individually.")
        
    with st.expander("Are uploaded files stored?"):
        st.write("No. Uploaded files and generated PDFs exist only temporarily while the server is processing them, ensuring data security.")
        
    with st.expander("What happens if a student record is invalid?"):
        st.write("Invalid rows are safely ignored, or if a PDF generation fails validation, it will be marked as 'FAILED' in the Generation Report.")

elif page == "About":
    st.markdown("## ℹ️ About Certificate Generation Agent")
    st.write("""
    An automated certificate-generation system that combines Excel student data with a certificate template to produce personalized PDF certificates.
    
    **Features:**
    - ✓ Automatic Excel column detection
    - ✓ Template-based certificate generation
    - ✓ PDF validation
    - ✓ Batch generation
    - ✓ ZIP download
    - ✓ CSV generation report
    - ✓ Secure temporary processing
    """)
    st.markdown("[View on GitHub](https://github.com/ksumanasri/mailmerg)", unsafe_allow_html=True)
