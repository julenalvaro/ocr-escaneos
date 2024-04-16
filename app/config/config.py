# PATH: app/config/config.py

from dotenv import load_dotenv
import os

# Carga las variables de entorno desde .env
load_dotenv()

# Obtiene el entorno actual
entorno_actual = os.getenv("ENTORNO")

def solicitar_confirmacion(config_obj):
    # Imprime las variables relevantes
    for key in dir(config_obj):
        if not key.startswith("__") and not callable(getattr(config_obj, key)):
            print(f"{key}: {getattr(config_obj, key)}")
    
    # Solicita confirmación
    respuesta = input("¿Quieres continuar con estos ajustes? (s/n): ")
    if respuesta.lower() != 's':
        exit("Ejecución cancelada por el usuario.")

# Configuraciones base
class Config:
    def __init__(self):
        self.DIR_PDFs = ""

class DesarrolloConfig(Config):
    def __init__(self):
        super().__init__()
        self.DIR_PDFs = os.getenv("DIR_PDFs_DEV")
        print("Configuración de Desarrollo cargada.")
        solicitar_confirmacion(self)

class PruebasConfig(Config):
    def __init__(self):
        super().__init__()
        self.DIR_PDFs = os.getenv("DIR_PDFs_PRUEBAS")
        print("Configuración de Pruebas cargada.")
        solicitar_confirmacion(self)

class ProduccionConfig(Config):
    def __init__(self):
        super().__init__()
        self.DIR_PDFs = os.getenv("DIR_PDFs_PROD")
        print("Configuración de Producción cargada.")
        # Aquí podrías decidir si quieres o no solicitar confirmación en producción

# Función para obtener la configuración actual
def obtener_configuracion():
    config_obj = None
    if entorno_actual == "dev":
        config_obj = DesarrolloConfig()
    elif entorno_actual == "prod":
        config_obj = ProduccionConfig()
    elif entorno_actual == "pruebas":
        config_obj = PruebasConfig()
    else:
        raise ValueError("Entorno no configurado correctamente.")
    return config_obj

# ejemplo de uso: 

# configuracion_actual = obtener_configuracion()
# print(f"DIR_PDFs: {configuracion_actual.DIR_PDFs}")


