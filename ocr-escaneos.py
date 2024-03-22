import os
import re
import shutil
from app.service.leer_pdf_easyocr import extract_orden_operacion
from app.config.config import obtener_configuracion

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


def procesar_archivos_no_estandar(archivos_no_estandar):
    for ruta_archivo in archivos_no_estandar:
        dir_path, archivo = os.path.split(ruta_archivo)
        dir_errores = os.path.join(dir_path, 'Errores OCR')
        if not os.path.exists(dir_errores):
            os.makedirs(dir_errores)

        print(f"Leyendo {archivo}")
        texto_orden, texto_operacion = extract_orden_operacion(ruta_archivo)
        print(f"Leído Orden: {texto_orden} y Operación: {texto_operacion}")
        
        try:
            if not (re.match(r'\d{10}', texto_orden) and re.match(r'\d{4}', texto_operacion)):
                destino = os.path.join(dir_errores, archivo)
                if os.path.exists(destino):
                    print(f"Eliminando archivo existente en Errores OCR: {archivo}")
                    os.remove(destino)
                print(f"Moviendo {archivo} a Errores OCR")
                shutil.move(ruta_archivo, destino)
            else:
                nuevo_nombre = f"{texto_orden}-{texto_operacion}.pdf"
                nuevo_destino = os.path.join(dir_path, nuevo_nombre)
                if os.path.exists(nuevo_destino):
                    print(f"Eliminando archivo duplicado: {archivo}")
                    os.remove(ruta_archivo)
                else:
                    print(f"Cambiando nombre de {archivo} a {nuevo_nombre}")
                    os.rename(ruta_archivo, nuevo_destino)
        except PermissionError as e:
            print(f"No se pudo acceder a {archivo} debido a un error de permisos: {e}")
        except FileNotFoundError as e:
            print(f"No se encontró {archivo} durante la operación: {e}")
        except Exception as e:
            print(f"Error al procesar {archivo}: {e}")


if __name__ == "__main__":
    configuracion = obtener_configuracion()
    dir_pdfs = configuracion.DIR_PDFs
    archivos_no_estandar, _ = listar_archivos_no_estandar(dir_pdfs)
    procesar_archivos_no_estandar(archivos_no_estandar)
