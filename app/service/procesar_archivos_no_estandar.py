# PATH: app/service/procesar_archivos_no_estandar.py

import os
import re
import shutil
import logging
from app.service.leer_pdf_easyocr import extract_orden_operacion

def procesar_archivos_no_estandar(archivos_no_estandar):
    for ruta_archivo in archivos_no_estandar:
        dir_path, archivo = os.path.split(ruta_archivo)
        dir_errores = os.path.join(dir_path, 'Errores OCR')
        if not os.path.exists(dir_errores):
            try:
                os.makedirs(dir_errores)
            except OSError as e:
                logging.error(f"Error al crear el directorio de errores: {e}")
                continue  # Saltar al siguiente archivo si no se puede crear el directorio

        logging.info(f"Leyendo {archivo}")
        try:
            texto_orden, texto_operacion = extract_orden_operacion(ruta_archivo)
            logging.info(f"Leído Orden: {texto_orden} y Operación: {texto_operacion}")
        except Exception as e:
            logging.error(f"Error al extraer orden y operación de {archivo}: {e}")
            # Mueve el archivo a 'Errores OCR'
            destino = os.path.join(dir_errores, archivo)
            try:
                if os.path.exists(destino):
                    logging.info(f"Eliminando archivo existente en Errores OCR: {archivo}")
                    os.remove(destino)
                logging.info(f"Moviendo {archivo} a Errores OCR debido a un error de extracción")
                shutil.move(ruta_archivo, destino)
            except PermissionError as e:
                logging.error(f"No se pudo mover {archivo} a Errores OCR debido a un error de permisos: {e}")
            except FileNotFoundError as e:
                logging.error(f"Archivo no encontrado durante la operación de mover {archivo}: {e}")
            except Exception as e:
                logging.error(f"Error desconocido al mover {archivo} a Errores OCR: {e}")
            continue  # Continúa con el siguiente archivo

        try:
            if not (re.match(r'\d{10}', texto_orden) and re.match(r'\d{4}', texto_operacion)):
                destino = os.path.join(dir_errores, archivo)
                try:
                    if os.path.exists(destino):
                        logging.info(f"Eliminando archivo existente en Errores OCR: {archivo}")
                        os.remove(destino)
                    logging.info(f"Moviendo {archivo} a Errores OCR")
                    shutil.move(ruta_archivo, destino)
                except PermissionError as e:
                    logging.error(f"No se pudo mover {archivo} a Errores OCR debido a un error de permisos: {e}")
                except FileNotFoundError as e:
                    logging.error(f"Archivo no encontrado durante la operación de mover {archivo}: {e}")
                except Exception as e:
                    logging.error(f"Error desconocido al mover {archivo} a Errores OCR: {e}")
            else:
                nuevo_nombre = f"{texto_orden}-{texto_operacion}.pdf"
                nuevo_destino = os.path.join(dir_path, nuevo_nombre)
                try:
                    if os.path.exists(nuevo_destino):
                        logging.info(f"Eliminando archivo duplicado: {archivo}")
                        os.remove(ruta_archivo)
                    else:
                        logging.info(f"Cambiando nombre de {archivo} a {nuevo_nombre}")
                        os.rename(ruta_archivo, nuevo_destino)
                except PermissionError as e:
                    logging.error(f"No se pudo renombrar {archivo} debido a un error de permisos: {e}")
                except FileNotFoundError as e:
                    logging.error(f"No se encontró {archivo} durante la operación: {e}")
                except Exception as e:
                    logging.error(f"Error desconocido al procesar {archivo}: {e}")
        except Exception as e:
            logging.error(f"Error inesperado al procesar el archivo {archivo}: {e}")
