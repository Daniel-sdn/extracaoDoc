import os
import csv
import json
import shutil
from io import StringIO
from pathlib import Path

import pandas as pd




def criaDictiModel(excelpatch):

    #Le a planilha e cria do DF
    frames_nf_v4_df = pd.read_excel(excelpatch)

    # Cria dicionários para armazenar diferentes tipos de elementos do modelo
    document_info = frames_nf_v4_df[frames_nf_v4_df['type'] == 'document'].iloc[0]
    boundaries_info = frames_nf_v4_df[frames_nf_v4_df['type'] == 'boundaries']
    sections_info = frames_nf_v4_df[frames_nf_v4_df['type'] == 'section']
    frames_info = frames_nf_v4_df[frames_nf_v4_df['type'] == 'frame']
    sframe_fields_info = frames_nf_v4_df[frames_nf_v4_df['type'] == 'sframe_field']
    field_boxes_info = frames_nf_v4_df[frames_nf_v4_df['type'] == 'field_box']






def cria_dict_cnae(exelpath):
    name = normalize('NFKD', name).encode('ASCII', 'ignore').decode('ASCII')
    # Creating a dictionary for CNAE codes and descriptions
    cnae_dict = dict(zip(mage_cnae_x_item_servico_df['cnae'], mage_cnae_x_item_servico_df['descricao_cnae']))
    item_servico_dict = dict(zip(mage_cnae_x_item_servico_df['item_servico'], mage_cnae_x_item_servico_df['descricao_item_servico']))




    
# 2. Leitura do arquivo CSV e criação do dicionário modelos
def create_model_dictionary(model_dict_path):
    model_dictionary = {}
    with open(model_dict_path, 'r') as csvfile:
        csvreader = csv.DictReader(csvfile)
        for row in csvreader:
            prefeitura_name = row['prefeitura']
            model_name = row['model']

            if prefeitura_name not in model_dictionary:
                model_dictionary[prefeitura_name] = model_name
            
            #model_dictionary[prefeitura_name].append(model_name)
    
    return model_dictionary    
    