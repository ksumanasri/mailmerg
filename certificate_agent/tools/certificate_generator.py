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
    signature_font_path = template_info.get('signature_font_path')
    
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

    signature_fontname = 'times-italic'
    signature_font = None
    if signature_font_path and os.path.exists(signature_font_path):
        page.insert_font(fontname='S0', fontfile=signature_font_path)
        signature_fontname = 'S0'
        signature_font = fitz.Font(fontfile=signature_font_path)
            
    def draw_text(key, text_val):
        if not text_val:
            return

        c = coords[key]
        x, y = c['x'], c['y']
        align = c.get('align', 'center')
        size = c.get('size', 28)
        max_w = c.get('max_width', template_info['width'] * 0.8)
        field_fontname = use_fontname
        field_get_len = lambda text, fontsize: get_len(text, fontsize)

        if key in {'left_signatory', 'right_signatory'}:
            field_fontname = signature_fontname
            if signature_font:
                field_get_len = lambda text, fontsize: signature_font.text_length(
                    text, fontsize=fontsize
                )
            else:
                field_get_len = lambda text, fontsize: fitz.get_text_length(
                    text, fontname=signature_fontname, fontsize=fontsize
                )

        tw = field_get_len(text_val, fontsize=size)
        while tw > max_w and size > 18:
            size -= 1
            tw = field_get_len(text_val, fontsize=size)

        if align == 'center':
            draw_x = x - tw / 2
        else:
            draw_x = x

        page.insert_text(
            fitz.Point(draw_x, y),
            text_val,
            fontname=field_fontname,
            fontsize=size,
            color=(0, 0, 0),
        )
    draw_text('name', name)
    draw_text('university', univ)
    draw_text('left_signatory', 'John')
    draw_text('right_signatory', 'Moses')
    draw_text('reg_no', reg)
    draw_text('date', date)
        
    safe_name = clean_filename(name).replace(" ", "_")
    safe_reg = clean_filename(reg)
    filename = f"{safe_reg}_{safe_name}.pdf"
    out_path = os.path.join(output_dir, filename)
    
    doc.save(out_path)
    doc.close()
    
    return out_path
