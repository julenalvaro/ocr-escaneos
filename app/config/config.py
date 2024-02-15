# app/config/config.py

from dotenv import load_dotenv
import os

# Carga las variables de entorno desde .env
load_dotenv()

# Obtiene el entorno actual
entorno_actual = os.getenv("ENTORNO", "dev")

# Configuraciones base
class Config:
    DIR_PDFs = ""

# Configuraciones para desarrollo
class DesarrolloConfig(Config):
    DIR_PDFs = os.getenv("DIR_PDFs_DEV")

# Configuraciones para producción
class ProduccionConfig(Config):
    DIR_PDFs = os.getenv("DIR_PDFs_PROD", "\\")

# Función para obtener la configuración actual
def obtener_configuracion():
    if entorno_actual == "dev":
        return DesarrolloConfig()
    elif entorno_actual == "prod":
        return ProduccionConfig()
    else:
        raise ValueError("Entorno no configurado correctamente.")

# Uso
configuracion_actual = obtener_configuracion()
print(configuracion_actual.DIR_PDFs)
