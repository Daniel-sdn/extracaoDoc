import os
import re


# Função para extrair número da string
def extract_number(text):
    match = re.search(r'\b\d+(\.\d+)?\b', text)
    if match:
        return match.group(0)
    else:
        return None
    
    
# Funcao importante - process_line
def process_line(value, reference, label):
    name_match = re.search(fr'{reference} (.+)', value)
    if name_match:
        extracted_value = reference + " " + name_match.group(1)
        return {label: extracted_value}
    return None


def format_number(number_str):
    # Check for percentage and handle it
    if '%' in number_str:
        number_str = number_str.replace('%', '')
        return float(number_str)  # You can multiply by 100 here if needed

    # Check if the string contains "R$" or a comma, indicating the original format
    if 'R$' in number_str or ',' in number_str:
        # Original format: Remove 'R$', replace dots with nothing, and replace commas with dots
        number_str = number_str.replace('R$', '').replace('.', '').replace(',', '.')
    else:
        # New format: Extract only the numeric part using regex
        number_str = re.findall(r'[\d\.]+', number_str)[-1]

    return float(number_str)

# Funçao de formatacao de numeros
def format_number2(number_str):
    number_str = number_str.replace('R$', '').replace('.', '').replace(',', '.')
    if '%' in number_str:
        number_str = number_str.replace('%', '')
        return float(number_str)  # multiplica por 100 para fields %
    return float(number_str)



def texto_extraido(texto):
    #0. Tratamento da string
    text_splited = texto.split('\n')
    text_splited = [s.replace(":", "") for s in text_splited]
    text_splited = [x for x in text_splited if x.strip()]
    text_splited = [s.replace(";", "").strip() for s in text_splited] #depende da situaçao
    return text_splited


#1. funcao: find_value_after_keyword_out_frame_up
def find_value_after_keyword_out_frame_up(keyword, text_list, default_keyword_list=None):
    try:
        index = text_list.index(keyword)
        # Verifica se o valor seguinte não é outra keyword da lista default_keyword_list
        if text_list[index + 1] not in default_keyword_list:
            return text_list[index + 1]
        else:
            return None
    except ValueError:
        if default_keyword_list:
            for default_keyword in default_keyword_list:
                if default_keyword in text_list:
                    # Caso especial para 'Nome/Razão Social:'
                    if keyword == 'Nome/Razão Social:':
                        return text_list[0]
        return None
    
#2. find_value_after_keyword_out_frame_down  
def find_value_after_keyword_out_frame_down(keyword, text_list, default_keyword_list=None):
    try:
        index = text_list.index(keyword)
        # Verifica se o índice seguinte está dentro da lista
        if index + 1 < len(text_list):
            # Verifica se o valor seguinte não é outra keyword da lista default_keyword_list
            if text_list[index + 1] not in default_keyword_list:
                return text_list[index + 1]
            else:
                return None
        else:
            return None
    except ValueError:
        if default_keyword_list:
            try:
                index = text_list.index(default_keyword_list[-1])
                return text_list[index - 1]
            except ValueError:
                return None
        else:
            return None
        
#3. find_value_after_keyword_fuzz
def find_value_after_keyword_fuzz(keyword, text_list, default_keyword_list=None, fuzziness_threshold=80):
    closest_match = None
    closest_match_score = 0
    
    for i, text in enumerate(text_list):
        score = fuzz.ratio(keyword, text)
        
        if score > closest_match_score:
            closest_match_score = score
            closest_match = text
        
        if closest_match_score > fuzziness_threshold:
            break

    if closest_match_score > fuzziness_threshold:
        index = text_list.index(closest_match)
        if index + 1 < len(text_list):
            if text_list[index + 1] not in default_keyword_list:
                return text_list[index + 1]
            else:
                return None
        else:
            return None
    else:
        return None  
    



def pesquisa_keyword(string_pesquisa, text_splited, keyword_list):

    resultado_extraido_fuzz = find_value_after_keyword_fuzz(string_pesquisa, text_splited, keyword_list)

    if resultado_extraido_fuzz == None:
        resultado_extraido_frame_up = find_value_after_keyword_out_frame_up(string_pesquisa, text_splited, keyword_list)
        if resultado_extraido_frame_up == None:
            resultado_extraido_frame_down = find_value_after_keyword_out_frame_down(string_pesquisa, text_splited, keyword_list)
            resultado_extraido = resultado_extraido_frame_down
        else:
            resultado_extraido = resultado_extraido_frame_up
    else:
        resultado_extraido = resultado_extraido_fuzz           
    #print(resultado_extraido)
    return resultado_extraido


def cabecalho_prefeitura():
    valor_dict = {}
    dados_prefeitura = {}
    f_frame_name = "1_frame_prefeitura_nf"
    # 1. funçao basica de modelo 
    texto = executa_model_frame(model, secao, f_frame_name)
    text_splited = texto.split('\n')
    
    valor_dict = extract_prefeitura(model, f_frame_name, text_splited)
    if valor_dict:
        dados_prefeitura.update(valor_dict)
        
        
    return dados_prefeitura 
                
def cabecalho_dados():

    valor = {}   
    f_frame_name = "1_frame_dados_nf"
    
    dadinho_dados_nf = {}
    
    # 1. funçao basica de modelo 
    texto = executa_model_frame(model, secao, f_frame_name)    
    text_splited = texto_extraido(texto)
    keyword_list = ['Número da Nota:', 'Competência:', 'Data e Hora da Emissão:', 'Código Verificação:']

    string_pesquisa = "Número da Nota:"
    texto = pesquisa_keyword(string_pesquisa, text_splited, keyword_list)         
    dadinho_dados_nf['numero_nota_fiscal'] = texto


    string_pesquisa = "Competência:"
    texto = pesquisa_keyword(string_pesquisa, text_splited, keyword_list)
    dadinho_dados_nf['competencia'] = texto
    
    
    string_pesquisa = "ata e Hora da Emissão:"
    texto = pesquisa_keyword(string_pesquisa, text_splited, keyword_list)
    dadinho_dados_nf['dt_hr_emissao'] = texto
    
    
    string_pesquisa = "Código Verificação:"
    texto = pesquisa_keyword(string_pesquisa, text_splited, keyword_list)
    dadinho_dados_nf['codigo_verificacao'] = texto
    
    return dadinho_dados_nf   


def extract_fields_prestador_cnpj(text): # Função para extrair campos e valores dentro de um retângulo
    
    
    nf_data_prestador_cnpj = {}
    # Extrair CPF/CNPJ com máscara 1
    if "CPF/CNPJ:" in text:
        cpf_cnpj_formatado_match = re.search(r'(\d{2}\.\d{3}\.\d{3}/\d{4}-\d{2})', text)
        if cpf_cnpj_formatado_match:
                        nf_data_prestador_cnpj['cpf_cnpj_com_mascara'] = cpf_cnpj_formatado_match.group(1)
                        nf_data_prestador_cnpj['cpf_cnpj_sem_mascara'] = re.sub(r'\D', '', cpf_cnpj_formatado_match.group(1))


    # Extrair Telefone
    telefone_str = None
    
    #telefone_match = re.search(r'Telefone:\s+([0-9.\s-])', text)
    telefone_match = re.search(r'Telefone:\s+([0-9.\s-]+)', text)
    if telefone_match: 
        telefone_str = telefone_match.group(1)
        # Remover quebras de linha
        telefone_str = telefone_str.replace('.', '')
        telefone_str = telefone_str.replace('\n', '')
                
        nf_data_prestador_cnpj['telefone'] = telefone_str
    else:
        nf_data_prestador_cnpj['telefone'] = None   
    
    
    return nf_data_prestador_cnpj 


def extract_fields_tomador_cnpj(text):
    nf_data_tomador_cnpj = {}
    
    # Extrair CPF/CNPJ com máscara 1
    if "CPF/CNPJ:" in text:
        cpf_cnpj_formatado_match = re.search(r'(\d{2}\.\d{3}\.\d{3}/\d{4}-\d{2})', text)
        if cpf_cnpj_formatado_match:
                        nf_data_tomador_cnpj['cpf_cnpj_com_mascara'] = cpf_cnpj_formatado_match.group(1)
                        nf_data_tomador_cnpj['cpf_cnpj_sem_mascara'] = re.sub(r'\D', '', cpf_cnpj_formatado_match.group(1))

    
    # Extrair Telefone
    telefone_match = re.search(r'Telefone:\s+(.+)', text)
    if telefone_match:
        telefone_str = telefone_match.group(1)
        if telefone_str == 'Inscrição Estadual:':
            nf_data_tomador_cnpj['telefone'] = None  # Valor padrão quando não há correspondência
        elif telefone_str == '':
            nf_data_tomador_cnpj['telefone'] = None  # Valor padrão quando não há correspondência
                    
        else:    
            nf_data_tomador_cnpj['telefone'] = telefone_match.group(1)
            
    
    # Extrair Inscrição Municipal
    inscricao_municipal_match = re.search(r'Inscrição Municipal:\s+(.+)', text)
    if inscricao_municipal_match:
        inscricao_municipal_str = inscricao_municipal_match.group(1)
        if inscricao_municipal_str == "Telefone:": 
            nf_data_tomador_cnpj['inscricao_municipal'] = None
        else:    
            nf_data_tomador_cnpj['inscricao_municipal'] = inscricao_municipal_str
    
    insc_municipal_match = re.search(r'INSC:MUNICIPAL:\s+(.+)', text)
    if insc_municipal_match:
        insc_municipal_str = insc_municipal_match.group(1)
        if insc_municipal_str == "Telefone:":
            nf_data_tomador_cnpj['inscricao_municipal'] = None
        else:    
            nf_data_tomador_cnpj['inscricao_municipal'] = insc_municipal_str
    else:
        nf_data_tomador_cnpj['inscricao_municipal'] = None
            
    
    return nf_data_tomador_cnpj 

def texto_extraido(texto):
    #0. Tratamento da string
    text_splited = texto.split('\n')
    text_splited = [s.replace(":", "") for s in text_splited]
    text_splited = [x for x in text_splited if x.strip()]
    text_splited = [s.replace(";", "").strip() for s in text_splited] #depende da situaçao
    return text_splited


def extract_dados_comple_obs(modelo, frame_father, section):
    
    data_dados_complementares = {}
    #frame_label = frame_father
    
    # 1. Filtrando o frames_info para buscar os dados de corte
    filtered_frames_info = frames_info[(frames_info['label'] == frame_father) & (frames_info['model'] == modelo)]

    # 2. Filtrando o sframe_fields_info para buscar os dados dos campos que estao nos frames
    filtered_sframe_fields_info = sframe_fields_info[(sframe_fields_info['father'] == frame_father) & (sframe_fields_info['model'] == modelo)]

    for index_frame, row_frame in filtered_frames_info.iterrows():
        
        x0, y0, x1, y1 = row_frame['x0'], row_frame['y0'], row_frame['x1'], row_frame['y1']
        extracted_text_box = extract_text_from_frame(image_2work, (x0, y0, x1, y1), tessdata_dir_config)
        
        print("{:<5} {:<10} {:<30} {:<20} {:<20} {:<7} {:<7} {:<7} {:<7}".format(row_frame['seq'], row_frame['model'], row_frame['father'], row_frame['label'], row_frame['reference'], row_frame['x0'], row_frame['y0'], row_frame['x1'], row_frame['y1'] ))
        for index_field, row_field in filtered_sframe_fields_info.iterrows():
            #print("{:<5} {:<10} {:<30} {:<20} {:<20}".format(row_field['seq'], row_field['model'], row_field['father'], row_field['label'], row_field['reference']))
            
            if frame_father == "5_frame_dados_complementares":
                nf_data_dados_complementares = {}
                nf_data_dados_complementares['section'] = section
                
                # Remove a primeira ocorrência de "Observação:"
                text = re.sub(r'^DADOS COMPLEMENTARES', '', extracted_text_box, count=1)
                if text == '':
                    text = None
                    nf_data_dados_complementares['dados_complementares'] = text
                else:    
                    # Extrair texto dentro do retângulo
                    nf_data_dados_complementares['dados_complementares'] = text.strip()
                    
                return nf_data_dados_complementares                
                
            elif frame_father == "5_frame_observacao":
                nf_data_observacao = {}
                nf_data_observacao['section'] = section 
                                # Remove a primeira ocorrência de "Observação:"
                text = re.sub(r'^Observação:', '', extracted_text_box, count=1)

                # Remover quebras de linha
                text = text.replace('\n', ' ')

                # Extrair texto dentro do retângulo
                nf_data_observacao['observacao'] = text.strip()
                
                return nf_data_observacao 
            
            
secao = "1 - CABECALHO"
f_frame_name = "1_frame_prefeitura_nf"


#4. Extrai prefeitura
def extract_prefeitura(model, father, values):
    
    tipo = "sframe_field"
    data_extrated_prefeitura = {}
    #print(tipo)

    filtered_frames_nf_v4_df = frames_nf_v4_df[(frames_nf_v4_df['model'] == model) & (frames_nf_v4_df['father'] == father) & (frames_nf_v4_df['type'] == tipo)]

    for index_sframe, row_sframe in filtered_frames_nf_v4_df.iterrows():
        
        label_value = row_sframe['label']
        
        #print("label_value", label_value)
        
        if label_value == "nome_prefeitura":
            reference_value = row_sframe['reference']
            for value in values:
                result = process_line(value, reference_value, label_value)
                if result:
                    data_extrated_prefeitura.update(result)
        elif label_value == "secretaria":
            reference_value = row_sframe['reference']
            for value in values:
                result = process_line(value, reference_value, label_value)
                if result:
                    data_extrated_prefeitura.update(result) 
        elif label_value == "tipo_nota_fiscal":
            reference_value = row_sframe['reference']  
            for value in values:
                result = process_line(value, reference_value, label_value)
                if result:
                    data_extrated_prefeitura.update(result)
                    
    return data_extrated_prefeitura




def processa_cnae_outros(text):
    nf_data_CNAE_match = re.search(r'CNAE\s+(.+)', text)
    if nf_data_CNAE_match:
        try:
            # Remove a primeira ocorrência de "CNAE:"
            nf_data_CNAE_str = re.sub(r'^CNAE - ', '', text, count=1)
            # Remover quebras de linha
            nf_data_CNAE_str = nf_data_CNAE_str.replace('\n', ' ')
            return nf_data_CNAE_str 
        except Exception as e:
            print(f"Erro busca cnae: {e}") 
        
    return None   



def extract_fb_outras_inf(modelo, father_value, section):

    data_box_valores = {}
    data_box_valores['secao'] = section
    filtered_boxes_info = field_boxes_info[(field_boxes_info['father'] == father_value) & (field_boxes_info['model'] == model)]
    # Iterate nas informações dos boxes de fields e extraia o texto de cada field
    for index_field, row_field in filtered_boxes_info.iterrows():
        
        string_pesquisa = row_field['reference']
        x0, y0, x1, y1 = row_field['x0'], row_field['y0'], row_field['x1'], row_field['y1']
        extracted_text_box = extract_text_from_frame(image_2work, (x0, y0, x1, y1), tessdata_dir_config)
        label = row_field['label']
        #print(f'extracted_text_box {extracted_text_box}, label {label}')
        text = extracted_text_box.replace('\n', '')
        if text.startswith(string_pesquisa):
            #print("aqui:", text)
            text = text[len(label):].strip()
            data_box_valores[label] = text
    
    return   data_box_valores      
                