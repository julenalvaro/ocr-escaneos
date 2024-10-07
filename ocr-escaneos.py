# PATH: ocr-escaneos.py

import logging
import os
from datetime import datetime
from app.config.config import obtener_configuracion
from app.service.listar_archivos_no_estandar import listar_archivos_no_estandar
from app.service.procesar_archivos_no_estandar import procesar_archivos_no_estandar

if __name__ == "__main__":
    # Configurar el logging
    fecha_hora_actual = datetime.now().strftime("%Y%m%d_%H%M%S")
    log_filename = f"ocr_escaneos_{fecha_hora_actual}.log"
    log_dir = os.path.join(os.getcwd(), "app", "logs")
    if not os.path.exists(log_dir):
        os.makedirs(log_dir)
    log_filepath = os.path.join(log_dir, log_filename)

    logging.basicConfig(
        level=logging.INFO,
        format="%(asctime)s [%(levelname)s] %(message)s",
        handlers=[
            logging.FileHandler(log_filepath, encoding='utf-8'),
            logging.StreamHandler()  # Esto es opcional si quieres que también se muestre en consola
        ]
    )

    configuracion = obtener_configuracion()
    dir_pdfs = configuracion.DIR_PDFs
    archivos_no_estandar, _ = listar_archivos_no_estandar(dir_pdfs)
    procesar_archivos_no_estandar(archivos_no_estandar)
