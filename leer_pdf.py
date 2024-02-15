import fitz  # PyMuPDF
import pytesseract
from PIL import Image
import re
import io

# Configura el path al ejecutable de Tesseract en tu sistema
pytesseract.pytesseract.tesseract_cmd = r"C:\Program Files\Tesseract-OCR\tesseract.exe"  # Ajusta según tu sistema

def extract_text_from_pdf(pdf_path):
    # Abre el archivo PDF
    doc = fitz.open(pdf_path)
    
    texto_orden = ""
    texto_operacion = ""

    # Itera sobre cada página del PDF
    for page_num in range(len(doc)):
        # Extrae la imagen de la página actual
        page = doc.load_page(page_num)
        pix = page.get_pixmap()
        img = Image.open(io.BytesIO(pix.tobytes()))
        
        # Usa OCR para extraer texto de la imagen
        text = pytesseract.image_to_string(img, config='--psm 6')
        
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

    # Cierra el documento PDF
    doc.close()
    
    return texto_orden, texto_operacion

# Reemplaza 'ruta_al_archivo.pdf' con la ruta real al archivo PDF
pdf_path = '1000003309-3577.pdf'
orden, operacion = extract_text_from_pdf(pdf_path)
print(orden)
print(operacion)
