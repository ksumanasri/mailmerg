import fitz
import os
import re

def clean_filename(name):
    return re.sub(r'[\\/*?:"<>|]', "_", name).strip()

def generate_certificate(record, template_path, template_info, output_dir):
    reg = record['reg_no']
    name = record['name']
    univ = record['university']
    date = record['date']
    
    if template_info['is_image']:
        doc = fitz.open("pdf", template_info['pdf_bytes'])
    else:
        doc = fitz.open(template_path)
        
    page = doc[0]
    coords = template_info['coords']
    font_path = template_info['font_path']
    
    if font_path and os.path.exists(font_path):
        page.insert_font(fontname="F0", fontfile=font_path)
        font = fitz.Font(fontfile=font_path)
        use_fontname = "F0"
        
        def get_len(t, s):
            return font.text_length(t, fontsize=s)
    else:
        use_fontname = "times-roman"
        def get_len(t, s):
            return fitz.get_text_length(t, fontname=use_fontname, fontsize=s)
            
    def draw_text(key, text_val):
        if not text_val: return
        c = coords[key]
        x, y, align, size = c['x'], c['y'], c['align'], c['size']
        
        tw = get_len(text_val, size)
        
        # Adaptive sizing for Name
        if key == 'name':
            max_w = template_info['width'] * 0.8
            while tw > max_w and size > 20:
                size -= 2
                tw = get_len(text_val, size)
                
        if align == 'center':
            draw_x = x - tw / 2
        else:
            draw_x = x
            
        page.insert_text(fitz.Point(draw_x, y), text_val, fontname=use_fontname, fontsize=size, color=(0,0,0))

    draw_text('name', name)
    draw_text('university', univ)
    draw_text('reg_no', reg)
    draw_text('date', date)
        
    safe_name = clean_filename(name).replace(" ", "_")
    safe_reg = clean_filename(reg)
    filename = f"{safe_reg}_{safe_name}.pdf"
    out_path = os.path.join(output_dir, filename)
    
    doc.save(out_path)
    doc.close()
    
    return out_path
