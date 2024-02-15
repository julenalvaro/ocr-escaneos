from pdf2image import convert_from_path
import easyocr
import re
import numpy as np

from pdf2image import convert_from_path
import easyocr
import re

def extract_orden_operacion(pdf_path):
    # Convertir las páginas del PDF a imágenes
    pages = convert_from_path(pdf_path, dpi=300)

    reader = easyocr.Reader(['es'])  # Asume español; ajusta según sea necesario

    texto_orden = ""
    texto_operacion = ""

    # Procesar cada página para buscar texto
    for img in pages:
        # Usa OCR para extraer texto de la imagen
        results = reader.readtext(np.array(img), detail=0)

        for text in results:
            # Busca las palabras clave y los números después de ellas
            match_orden = re.search(r'Orden:\s*(\d{10})', text)
            match_operacion = re.search(r'Operación:\s*(\d{4})', text)

            if match_orden:
                texto_orden = match_orden.group(0)
            if match_operacion:
                texto_operacion = match_operacion.group(0)

            # Si ambos textos son encontrados, no es necesario seguir buscando
            if texto_orden and texto_operacion:
                break

        if texto_orden and texto_operacion:
            break

    return texto_orden, texto_operacion

# Ruta al archivo PDF
pdf_path = '1000003309-3577.pdf'
orden, operacion = extract_orden_operacion(pdf_path)
print("Orden encontrada:", orden)
print("Operación encontrada:", operacion)
