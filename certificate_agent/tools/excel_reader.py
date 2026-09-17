import pandas as pd
import re

def read_students(excel_path):
    df = pd.read_excel(excel_path)
    # Find columns
    cols = df.columns
    reg_col = None
    name_col = None
    univ_col = None
    date_col = None
    
    for c in cols:
        c_str = str(c).strip().lower()
        c_clean = re.sub(r'[^a-z0-9]', '', c_str)
        if c_clean in ['regno', 'registrationno', 'registrationnumber', 'regnumber']:
            reg_col = c
        elif c_clean in ['name', 'studentname']:
            name_col = c
        elif 'honors' in c_str or 'university' in c_str:
            univ_col = c
        elif 'awarded' in c_str or 'date' in c_str:
            date_col = c
            
    if not reg_col or not name_col:
        raise ValueError(f"Could not find required columns in Excel. Found: {list(cols)}")
        
    records = []
    seen_reg = {}
    
    for idx, row in df.iterrows():
        reg = str(row[reg_col]).strip()
        name = str(row[name_col]).strip()
        if not reg or not name or reg == 'nan' or name == 'nan':
            continue
            
        # Normalize inner spaces
        name = re.sub(r'\s+', ' ', name)
        
        # Handle duplicate regs
        base_reg = reg
        counter = 1
        while reg in seen_reg:
            counter += 1
            reg = f"{base_reg}_{counter}"
        seen_reg[reg] = True
        
        univ = str(row[univ_col]).strip() if univ_col and pd.notna(row[univ_col]) else ""
        date = str(row[date_col]).strip() if date_col and pd.notna(row[date_col]) else ""
        if date and "00:00:00" in date:
            date = date.split(" ")[0]
            
        records.append({
            'reg_no': reg,
            'name': name,
            'university': univ,
            'date': date
        })
        
    return records
