# ocr-escaneos.py

import os
import re
import shutil
from app.service.leer_pdf_easyocr import extract_orden_operacion
from app.config.config import obtener_configuracion

def listar_archivos_no_estandar(dir_path):
    archivos = [f for f in os.listdir(dir_path) if os.path.isfile(os.path.join(dir_path, f))]
    archivos_no_estandar = [f for f in archivos if not re.match(r'\d{10}-\d{4}\.pdf', f)]
    return archivos_no_estandar, archivos

def procesar_archivos_no_estandar(dir_path, archivos_no_estandar, archivos):
    dir_errores = os.path.join(dir_path, 'Errores OCR')
    if not os.path.exists(dir_errores):
        os.makedirs(dir_errores)
    
    for archivo in archivos_no_estandar:
        print(f"Leyendo {archivo}")
        ruta_archivo = os.path.join(dir_path, archivo)
        texto_orden, texto_operacion = extract_orden_operacion(ruta_archivo)
        print(f"Leído Orden: {texto_orden} y Operación {texto_operacion}")
        
        # Modificación aquí para manejar archivos que el OCR no leyó correctamente
        if not (re.match(r'\d{10}', texto_orden) and re.match(r'\d{4}', texto_operacion)):
            # OCR ha leído mal
            destino = os.path.join(dir_errores, archivo)  # Usa el nombre original del archivo
            if os.path.exists(destino):
                print(f"Eliminando archivo existente en Errores OCR: {archivo}")
                os.remove(destino)  # Elimina el archivo existente
            print(f"Moviendo {archivo} a Errores OCR")
            shutil.move(ruta_archivo, destino)
        else:
            # OCR probablemente ha leído bien
            nuevo_nombre = f"{texto_orden}-{texto_operacion}.pdf"
            if nuevo_nombre in archivos:
                print(f"Eliminando archivo duplicado: {archivo}")
                os.remove(ruta_archivo)
            else:
                nuevo_destino = os.path.join(dir_path, nuevo_nombre)
                print(f"Cambiando nombre de {archivo} a {nuevo_nombre}")
                os.rename(ruta_archivo, nuevo_destino)
                archivos.remove(archivo)  # Elimina el antiguo de la lista
                archivos.append(nuevo_nombre)  # Añade el nuevo

if __name__ == "__main__":
    configuracion = obtener_configuracion()
    dir_pdfs = configuracion.DIR_PDFs
    archivos_no_estandar, array_pdfs = listar_archivos_no_estandar(dir_pdfs)
    procesar_archivos_no_estandar(dir_pdfs, archivos_no_estandar, array_pdfs)
