import pandas as pd
import re


def _normalize_date(value):
    if value is None or (isinstance(value, float) and pd.isna(value)):
        return ""

    if isinstance(value, pd.Timestamp):
        return value.strftime('%d-%m-%Y')

    text = str(value).strip()
    if not text or text.lower() in {'nan', 'none'}:
        return ""

    try:
        parsed = pd.to_datetime(text, dayfirst=True)
        return parsed.strftime('%d-%m-%Y')
    except Exception:
        return text


def read_students(excel_path):
    df = pd.read_excel(excel_path)
    cols = df.columns
    reg_col = None
    name_col = None
    univ_col = None
    date_col = None

    for c in cols:
        c_str = str(c).strip().lower()
        c_clean = re.sub(r'[^a-z0-9]', '', c_str)

        if c_clean in ['regno', 'registrationno', 'registrationnumber', 'regnumber', 'certificateno', 'certificatenumber']:
            reg_col = c
        elif c_clean in ['name', 'studentname']:
            name_col = c
        elif ('graduated' in c_str and 'honor' in c_str) or 'university' in c_str or 'college' in c_str or 'institute' in c_str:
            univ_col = c
        elif ('awarded' in c_str and ('on' in c_str or 'date' in c_str or 'datein' in c_str)) or 'date' in c_str or 'awarddate' in c_clean:
            date_col = c

    if not reg_col or not name_col:
        raise ValueError(f"Could not find required columns in Excel. Found: {list(cols)}")

    records = []
    seen_reg = {}

    for _, row in df.iterrows():
        reg = str(row[reg_col]).strip()
        name = str(row[name_col]).strip()
        if not reg or not name or reg.lower() == 'nan' or name.lower() == 'nan':
            continue

        name = re.sub(r'\s+', ' ', name)

        base_reg = reg
        counter = 1
        while reg in seen_reg:
            counter += 1
            reg = f"{base_reg}_{counter}"
        seen_reg[reg] = True

        univ = str(row[univ_col]).strip() if univ_col and pd.notna(row[univ_col]) else ""
        date = _normalize_date(row[date_col]) if date_col and pd.notna(row[date_col]) else ""

        records.append({
            'reg_no': reg,
            'name': name,
            'university': univ,
            'date': date
        })

    return records
