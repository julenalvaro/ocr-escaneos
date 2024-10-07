# PATH: app/service/listar_archivos_no_estandar.py

import os
import re

def listar_archivos_no_estandar(dir_path):
    archivos_no_estandar = []
    archivos = []
    for root, dirs, files in os.walk(dir_path, topdown=True):
        # Ignora los directorios 'Errores OCR'
        dirs[:] = [d for d in dirs if d != 'Errores OCR']
        
        for file in files:
            if file.endswith(".pdf"):
                archivo_completo = os.path.join(root, file)
                archivos.append(archivo_completo)

                # Verifica si el archivo ya cumple con el formato estándar
                if re.match(r'\d{10}-\d{4}\.pdf', file):
                    continue  # Ignora el archivo, ya está en el formato correcto

                # Verifica si el archivo tiene el patrón pero con caracteres adicionales
                match = re.match(r'(\d{10}-\d{4}).*\.pdf$', file)
                if match:
                    nuevo_nombre = f"{match.group(1)}.pdf"
                    nuevo_destino = os.path.join(root, nuevo_nombre)
                    try:
                        # Reemplaza el archivo si el nuevo nombre ya existe
                        if os.path.exists(nuevo_destino):
                            os.remove(nuevo_destino)
                        os.rename(archivo_completo, nuevo_destino)
                        print(f"Cambiado el nombre de {archivo_completo} a {nuevo_destino}")
                    except Exception as e:
                        print(f"Error al procesar {archivo_completo}: {e}")
                else:
                    # El archivo no cumple con los formatos esperados y se considera no estándar
                    archivos_no_estandar.append(archivo_completo)

    return archivos_no_estandar, archivos