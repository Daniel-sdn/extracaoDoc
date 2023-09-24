import os
import cv2
from PIL import Image
import pytesseract
import fitz  # Módulo PyMuPDF
import PyPDF2


def extract_fields_box(modelo, father_value, section):

    data_box_valores = {}
    data_box_valores['secao'] = section
    filtered_boxes_info = field_boxes_info[(field_boxes_info['father'] == father_value) & (field_boxes_info['model'] == modelo)]
    # Iterate nas informações dos boxes de fields e extraia o texto de cada field
    for index_field, row_field in filtered_boxes_info.iterrows():
        x0, y0, x1, y1 = row_field['x0'], row_field['y0'], row_field['x1'], row_field['y1']
        extracted_text_box = extract_text_from_frame(image_2work, (x0, y0, x1, y1), tessdata_dir_config)
        #print("{:<5} {:<10} {:<30} {:<20} {:<20} {:<7} {:<7} {:<7} {:<7}".format(row_field['seq'], row_field['model'], row_field['father'], row_field['label'], row_field['reference'], row_field['x0'], row_field['y0'], row_field['x1'], row_field['y1'] ))
        # Divida o texto por nova linha e mantenha apenas a última parte (assume que o valor está sempre no final)
        value = extracted_text_box.split('\n')[-1]
        # Remova qualquer espaço em branco à esquerda ou à direita
        value = value.strip()
        if row_field['t_value'] == 'number':
            # Formate o valor usando a função format_number
            #print("vou verificar valor")
            value = format_number2(value)
            #print(value)
        # Armazene o texto extraído com o rótulo correspondente
        label = row_field['label']
        data_box_valores[label] = value
        
    return data_box_valores


# 3. Efetua OCR no documento (area parao do texto da NF)
def ocr_RasterPDF(image_name):
    
    analise_pesquisa_nf = {}
    # 1. Definindo as coordenadas do frame
    x0 = 406
    y0 = 0
    x1= 1540
    y1 = 380

    # 2. Definir frame_image
    frame_image = image_name.crop((x0, y0, x1, y1))

    # 3. Extraia texto usando OCR com configuração de idioma padrão para este frame
    extracted_text_frame = pytesseract.image_to_string(frame_image, lang='por', config=tessdata_dir_config).strip()

    # 4. Divida o texto por nova linha e mantenha apenas a última parte (assume que o valor está sempre no final)
    values = extracted_text_frame.split('\n')
    return values, extracted_text_frame 



# 2. Efetua OCR no documento (area parao do texto da NF)
def ocr_RasterPDF_free(image_name, vx0, vy0, vx1, vy1):
    
    analise_pesquisa_nf = {}
    # 1. Definindo as coordenadas do frame
    x0 = vx0
    y0 = vy0
    x1= vx1
    y1 = vy1

    # 2. Definir frame_image
    frame_image = image_name.crop((x0, y0, x1, y1))

    # 3. Extraia texto usando OCR com configuração de idioma padrão para este frame
    extracted_text_frame = pytesseract.image_to_string(frame_image, lang='por', config=tessdata_dir_config).strip()

    # 4. Divida o texto por nova linha e mantenha apenas a última parte (assume que o valor está sempre no final)
    values = extracted_text_frame.split('\n')
    return values, extracted_text_frame 


# 2. Pesquisa prefeitura no documento
def pequisaModel(image_name):

    # 1. Definindo as coordenadas do frame
    x0 = 406
    y0 = 0
    x1= 1540
    y1 = 380

    # 2. Definir frame_image
    frame_image = image_name.crop((x0, y0, x1, y1))

    # 3. Extraia texto usando OCR com configuração de idioma padrão para este frame
    extracted_text_frame = pytesseract.image_to_string(frame_image, lang='por', config=tessdata_dir_config).strip()

    # 4. Divida o texto por nova linha e mantenha apenas a última parte (assume que o valor está sempre no final)
    values = extracted_text_frame.split('\n')

    # 5. Interacao para pesquisar prefeitura
    for value in values:
        nome_prefeitura_match = re.search(r'PREFEITURA (.+)', value)
        if nome_prefeitura_match:
            nome_prefeitura = "PREFEITURA " + nome_prefeitura_match.group(1) 
            return  nome_prefeitura        
     

# 1. Interacao para pesquisar prefeitura
def pesquisa_texto(texto):
    nome_prefeitura_match = re.search(r'PREFEITURA (.+)', texto)
    if nome_prefeitura_match:
        is_prefeitura = "PREFEITURA " + nome_prefeitura_match.group(1)
        
        return  is_prefeitura
    else:
        raise ValueError("Nao consegui pesquisar")
    
    
    # 5. Verifica se PDF e pesquisavel ou nao e grava metadados dele
def is_pdf_searchable_analise(pdf_path):
    try:
        pdf_document = fitz.open(pdf_path)
        pages = pdf_document.page_count
        is_searchable = all(page.get_text("text") != "" for page in pdf_document)
        dados_pdf = pdf_document.metadata
        pdf_document.close()
        return is_searchable, dados_pdf, pages
    except Exception as e:
        print(f"Erro ao verificar o PDF: {e}")
        return False
    
    
# 2. Extracao OCR
def extract_text_from_coordinates(image, coordinates, config):
    x0, y0, x1, y1 = coordinates
    frame_image = image.crop((x0, y0, x1, y1))
    extracted_text = pytesseract.image_to_string(frame_image, lang='por', config=config).strip()
    return extracted_text

# 1. funçao basica de modelo 
def executa_model_frame(model, secao, father_name):

    data_dados_frame = {}
    
    tipo = "frame"
    filtered_frames_nf_v4_df = frames_nf_v4_df[(frames_nf_v4_df['model'] == model) & (frames_nf_v4_df['label'] == f_frame_name) & (frames_nf_v4_df['type'] == tipo)]

    for index_frame, row_frame in filtered_frames_nf_v4_df.iterrows():
        
        x0, y0, x1, y1 = row_frame['x0'], row_frame['y0'], row_frame['x1'], row_frame['y1']
        extracted_text_frame = extract_text_from_coordinates(image_2work, (x0, y0, x1, y1), tessdata_dir_config)
        
        frame_seq = row_frame['seq']
        frame_model = row_frame['model']
        frame_label = row_frame['label']
        frame_type = row_frame['type']
        frame_section = row_frame['section_json']
        frame_reference = row_frame['reference']
        frame_father = row_frame['father']
        frame_id = row_frame['id']
        #print(f'\fid: {frame_id:>3} | seq: {frame_seq:>3} | model: {frame_model:>8} | type: {frame_type:>15} | Father: {frame_father} label: {frame_label:>30} | section: {frame_section:>20} {frame_reference:>30}')
        
    return extracted_text_frame



# Sao iguais 
def extract_text_from_frame(image, coordinates, config):
    x0, y0, x1, y1 = coordinates
    frame_image = image.crop((x0, y0, x1, y1))
    extracted_text = pytesseract.image_to_string(frame_image, lang='por', config=config).strip()
    return extracted_text    
    