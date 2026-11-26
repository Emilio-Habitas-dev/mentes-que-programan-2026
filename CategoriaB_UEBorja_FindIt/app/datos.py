"""Leer, guardar y restablecer los datos en archivos JSON locales (no usa internet).

- datos_iniciales.json: los 10 objetos de prueba del reto. Nunca se modifica.
- datos.json: copia de trabajo donde se guardan los cambios (persisten al cerrar la app).
"""
import json
import shutil
import sys
from pathlib import Path

# Rutas calculadas desde este archivo: funciona en cualquier carpeta o equipo
CARPETA_DATOS = Path(__file__).resolve().parent.parent / "data"

if getattr(sys, "frozen", False):
    # Ejecutable (PyInstaller): los datos se guardan en una carpeta «data» junto al ejecutable,
    # porque dentro del ejecutable no se puede escribir. La primera vez se copian los archivos iniciales.
    empaquetados = Path(sys._MEIPASS) / "data"
    CARPETA_DATOS = Path(sys.executable).resolve().parent / "data"
    CARPETA_DATOS.mkdir(exist_ok=True)
    for nombre in ("datos_iniciales.json", "credenciales_demo.json"):
        if not (CARPETA_DATOS / nombre).exists():
            shutil.copyfile(empaquetados / nombre, CARPETA_DATOS / nombre)

RUTA_INICIALES = CARPETA_DATOS / "datos_iniciales.json"
RUTA_DATOS = CARPETA_DATOS / "datos.json"
RUTA_CREDENCIALES = CARPETA_DATOS / "credenciales_demo.json"
CARPETA_FOTOS = CARPETA_DATOS / "fotos"  # Fotos subidas en los reportes


def cargar():
    """Devuelve los datos. La primera vez crea datos.json copiando los datos iniciales."""
    if not RUTA_DATOS.exists():
        restablecer()
    with open(RUTA_DATOS, encoding="utf-8") as archivo:
        datos = json.load(archivo)
    # Compatibilidad con archivos creados antes de existir estas listas
    for lista in ("reportes", "usuarios", "mensajes"):
        datos.setdefault(lista, [])
    return datos


def guardar(datos):
    """Escribe los datos en datos.json para que no se pierdan al cerrar."""
    with open(RUTA_DATOS, "w", encoding="utf-8") as archivo:
        json.dump(datos, archivo, ensure_ascii=False, indent=2)


def restablecer():
    """Vuelve a los 10 objetos de prueba originales (borra los cambios)."""
    shutil.copyfile(RUTA_INICIALES, RUTA_DATOS)


def cargar_credenciales():
    """Credenciales ficticias del administrador para la demostración."""
    with open(RUTA_CREDENCIALES, encoding="utf-8") as archivo:
        return json.load(archivo)


def siguiente_id(lista):
    """Id nuevo: el mayor id existente + 1."""
    return max((elemento["id"] for elemento in lista), default=0) + 1


def guardar_foto(ruta_origen, nombre_base):
    """Copia la foto elegida a data/fotos/ y devuelve su nombre (se guarda ese nombre en el JSON)."""
    CARPETA_FOTOS.mkdir(exist_ok=True)
    nombre = f"{nombre_base}{Path(ruta_origen).suffix.lower()}"
    shutil.copyfile(ruta_origen, CARPETA_FOTOS / nombre)
    return nombre


def ruta_foto(nombre):
    """Ruta completa de una foto guardada, o None si no existe."""
    if not nombre:
        return None
    ruta = CARPETA_FOTOS / nombre
    return ruta if ruta.exists() else None
