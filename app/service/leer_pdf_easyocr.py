# PATH: app/service/leer_pdf_easyocr.py

from pdf2image import convert_from_path
import easyocr
import re
import numpy as np

def extract_orden_operacion(pdf_path):
    # Convertir las páginas del PDF a imágenes
    pages = convert_from_path(pdf_path, dpi=300)

    # Asume español e inglés; ajusta según sea necesario
    reader = easyocr.Reader(['es', 'en'])

    texto_orden = ""
    texto_operacion = ""

    # Procesar cada página para buscar texto
    for img in pages:
        # Usa OCR para extraer texto de la imagen
        results = reader.readtext(np.array(img), detail=0)

        for text in results:
            # Busca las palabras clave y los números después de ellas
            # Modificación aquí para capturar solo los dígitos y para soportar inglés
            match_orden = re.search(r'(Orden|Order):\s*(\d{10})', text)
            match_operacion = re.search(r'(Operación|Operation):\s*(\d{4})', text)

            if match_orden:
                # Devuelve solo el grupo de dígitos capturado
                texto_orden = match_orden.group(2)
            if match_operacion:
                # Devuelve solo el grupo de dígitos capturado
                texto_operacion = match_operacion.group(2)

            # Si ambos textos son encontrados, no es necesario seguir buscando
            if texto_orden and texto_operacion:
                break

        if texto_orden and texto_operacion:
            break

    return texto_orden, texto_operacion


if __name__ == "__main__":
    # Ruta al archivo PDF
    pdf_path = '1000003309-3577.pdf'
    orden, operacion = extract_orden_operacion(pdf_path)
    print("Orden encontrada:", orden)
    print("Operación encontrada:", operacion)
