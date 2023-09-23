import os
import csv
import json
import shutil
from io import StringIO
from pathlib import Path
from PIL import Image
from pdf2image import convert_from_path
import fitz  # Módulo PyMuPDF


# 12. poppler path
poppler_path = "/home/dani-boy/miniconda3/envs/tables-detr/bin"


# 1. Funcao de conversao e resize do documento
def convertResize(doc2convert, document_path, image_resized_path):
    
    """# 1. remocao do sufixo .pdf
    if doc2convert.split(".")[1].islower():
        nameImage= doc2convert.removesuffix(".pdf")
    else:
        nameImage= doc2convert.removesuffix(".PDF")"""
    
    # 2. construo um novo nome para o documento imagem
    image_resized_name = os.path.join(f'{image_resized_path}/{str(doc2convert)}.jpg')
    
    # 3. Conversao para imagem
    pages = convert_from_path(document_path, 500, poppler_path=poppler_path)
    
    # 4. Verifica se ha mais que uma pagina
    if len(pages) > 1:
        raise ValueError("Erro, documento com mais de uma página")
    else:
        # 5. Iterar pelas páginas e redimensionar
        resized_pages = []
        for page in pages:
            resized_page = page.resize((2067, 2923))
            resized_pages.append(resized_page)
            
        resized_pages[0].save(image_resized_name, 'JPEG')
        
    return resized_pages[0], image_resized_name


def convertResizeAnalise_1page(doc2convert, document_path, image_resized_path):
    
    """# 1. remocao do sufixo .pdf
    if doc2convert.split(".")[1].islower():
        nameImage= doc2convert.removesuffix(".pdf")
    else:
        nameImage= doc2convert.removesuffix(".PDF")"""
    
    # 2. construo um novo nome para o documento imagem
    image_resized_name = os.path.join(f'{image_resized_path}/{str(doc2convert)}.jpg')
    
    # 3. Conversao para imagem
    pages = convert_from_path(document_path, 500, poppler_path=poppler_path)
    
    resized_pages = []
    for page in pages:
        resized_page = page.resize((2067, 2923))
        resized_pages.append(resized_page)
        resized_pages[0].save(image_resized_name, 'JPEG')
        
    return resized_pages[0], image_resized_name


# Funcao de conversao e resize do documento
def convertResize_analise(nome_documento, document_path, image_resized_path):
    
    """# 1. remocao do sufixo .pdf
    if doc2convert.split(".")[1].islower():
        nameImage= doc2convert.removesuffix(".pdf")
    else:
        nameImage= doc2convert.removesuffix(".PDF")"""
    
    # 2. construo um novo nome para o documento imagem
    image_resized_name = os.path.join(f'{image_resized_path}/{str(nome_documento)}.jpg')
    
    # 3. Conversao para imagem
    pages = convert_from_path(document_path, 500, poppler_path=poppler_path)
    
    # 4. Verifica se ha mais que uma pagina
    if len(pages) > 1:
        raise ValueError("Erro, documento com mais de uma página")
    else:
        # 5. Iterar pelas páginas e redimensionar
        resized_pages = []
        for page in pages:
            resized_page = page.resize((2067, 2923))
            resized_pages.append(resized_page)
            
        resized_pages[0].save(image_resized_name, 'JPEG')
        
    return resized_pages[0], image_resized_name