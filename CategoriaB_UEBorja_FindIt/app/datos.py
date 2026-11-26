"""Leer, guardar y restablecer los datos en archivos JSON locales (no usa internet).

- datos_iniciales.json: los 10 objetos de prueba del reto. Nunca se modifica.
- datos.json: copia de trabajo donde se guardan los cambios (persisten al cerrar la app).
"""
import json
import shutil
from pathlib import Path

# Rutas calculadas desde este archivo: funciona en cualquier carpeta o equipo
CARPETA_DATOS = Path(__file__).resolve().parent.parent / "data"
RUTA_INICIALES = CARPETA_DATOS / "datos_iniciales.json"
RUTA_DATOS = CARPETA_DATOS / "datos.json"
RUTA_CREDENCIALES = CARPETA_DATOS / "credenciales_demo.json"


def cargar():
    """Devuelve los datos. La primera vez crea datos.json copiando los datos iniciales."""
    if not RUTA_DATOS.exists():
        restablecer()
    with open(RUTA_DATOS, encoding="utf-8") as archivo:
        datos = json.load(archivo)
    datos.setdefault("reportes", [])  # Compatibilidad con archivos creados antes de existir los reportes
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
