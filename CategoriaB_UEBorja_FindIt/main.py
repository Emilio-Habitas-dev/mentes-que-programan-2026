"""FIND IT - Objetos perdidos y encontrados del colegio.

Punto de entrada: crea la ventana y arranca la aplicación.
Ejecutar con:  python main.py
"""
import tkinter as tk

from app.ventana import Ventana


def main():
    root = tk.Tk()
    Ventana(root)
    root.mainloop()


if __name__ == "__main__":
    main()
