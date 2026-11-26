"""Identidad visual de FIND IT: colores, fuentes, estilos y piezas reutilizables.
Cambiar el diseño de toda la app solo requiere tocar este archivo."""
import tkinter as tk
import tkinter.font as tkfont
from tkinter import ttk

# --- Colores de la marca (boceto de Inicio) ---
AMARILLO = "#FFC90E"
NEGRO = "#000000"
AZUL_BORDE = "#3B4CCA"

# --- Colores de las vistas internas (bocetos remasterizados) ---
FONDO = "#E9EEF5"
BLANCO = "#FFFFFF"
BORDE = "#D5DCE6"
MARINO = "#13294B"
AZUL = "#1D4ED8"
AZUL_OSCURO = "#1E40AF"
AZUL_SUAVE = "#DBE6F5"
TEXTO = "#0F172A"
TEXTO_SUAVE = "#64748B"
VERDE = "#15803D"
ERROR = "#B91C1C"
ERROR_FONDO = "#FDECEC"
GRIS_DESACTIVADO = "#94A3B8"

# Color de cada estado: (color fuerte para la etiqueta, color suave para la fila de la tabla)
COLORES_ESTADO = {
    "Disponible": ("#16A34A", "#E8F7EE"),
    "Reclamado": ("#D49B0B", "#FDF5DF"),
    "Entregado": ("#64748B", "#EEF1F5"),
}

# Color del ícono de cada categoría
COLORES_CATEGORIA = {"Ropa": "#2563EB", "Útiles": "#DC2626", "Tecnología": "#0F172A",
                     "Deportes": "#16A34A", "Otros": "#7C3AED"}

FUENTE = "Helvetica"  # configurar() elige la mejor fuente instalada


def fuente(tamano=11, peso="normal", estilo="roman"):
    return (FUENTE, tamano, peso, estilo)


def configurar(root):
    """Elige la fuente y define los estilos ttk (tabla, listas desplegables, campos)."""
    global FUENTE
    disponibles = set(tkfont.families(root))
    for nombre in ("Segoe UI", "Ubuntu", "Noto Sans", "DejaVu Sans"):
        if nombre in disponibles:
            FUENTE = nombre
            break

    root.configure(bg=FONDO)
    estilo = ttk.Style(root)
    estilo.theme_use("clam")
    estilo.configure(".", font=fuente(11), background=FONDO, foreground=TEXTO)

    # Tabla profesional de objetos
    estilo.configure("Treeview", background=BLANCO, fieldbackground=BLANCO, foreground=TEXTO,
                     rowheight=36, font=fuente(11), borderwidth=0)
    estilo.configure("Treeview.Heading", background=MARINO, foreground=BLANCO,
                     font=fuente(11, "bold"), padding=(8, 10), borderwidth=0, relief="flat")
    estilo.map("Treeview.Heading", background=[("active", MARINO)])
    estilo.map("Treeview", background=[("selected", AZUL)], foreground=[("selected", BLANCO)])

    # Campos de texto y listas desplegables
    for nombre in ("TEntry", "TCombobox"):
        estilo.configure(nombre, padding=8, fieldbackground=BLANCO, bordercolor=BORDE,
                         lightcolor=BORDE, darkcolor=BORDE)
    estilo.configure("Invalido.TEntry", fieldbackground=ERROR_FONDO, bordercolor=ERROR,
                     lightcolor=ERROR, darkcolor=ERROR, padding=8)
    estilo.configure("Invalido.TCombobox", fieldbackground=ERROR_FONDO, bordercolor=ERROR,
                     lightcolor=ERROR, darkcolor=ERROR, padding=8)
    estilo.map("TCombobox", fieldbackground=[("readonly", BLANCO)])
    estilo.map("Invalido.TCombobox", fieldbackground=[("readonly", ERROR_FONDO)])


# ---------- Piezas reutilizables ----------

def tarjeta(padre, relleno=24):
    """Recuadro blanco con borde fino. 'relleno' es el margen interno."""
    marco = tk.Frame(padre, bg=BLANCO, highlightthickness=1, highlightbackground=BORDE,
                     highlightcolor=BORDE, padx=relleno, pady=relleno)
    return marco


def texto(padre, contenido, tamano=11, peso="normal", color=TEXTO, fondo=BLANCO, **opciones):
    """Etiqueta de texto con la fuente de la app."""
    opciones.setdefault("justify", "left")
    opciones.setdefault("anchor", "w")
    return tk.Label(padre, text=contenido, font=fuente(tamano, peso), fg=color, bg=fondo, **opciones)


def chip_estado(padre, estado):
    """Etiqueta de color con el estado del objeto (verde, ámbar o gris)."""
    color = COLORES_ESTADO[estado][0]
    return tk.Label(padre, text=f"  {estado}  ", font=fuente(10, "bold"), fg=BLANCO, bg=color, pady=3)


def boton_primario(padre, contenido, comando):
    """Botón azul principal."""
    return tk.Button(padre, text=contenido, command=comando, font=fuente(11, "bold"), fg=BLANCO, bg=AZUL,
                     activebackground=AZUL_OSCURO, activeforeground=BLANCO, disabledforeground=BLANCO,
                     relief="flat", bd=0, padx=20, pady=9, cursor="hand2")


def boton_secundario(padre, contenido, comando):
    """Botón blanco con borde."""
    return tk.Button(padre, text=contenido, command=comando, font=fuente(11), fg=TEXTO, bg=BLANCO,
                     activebackground=AZUL_SUAVE, relief="flat", bd=0, highlightthickness=1,
                     highlightbackground=TEXTO, padx=18, pady=8, cursor="hand2")


def boton_enlace(padre, contenido, comando, fondo=FONDO):
    """Botón que parece un enlace (ej. «← Volver al listado»)."""
    return tk.Button(padre, text=contenido, command=comando, font=fuente(11), fg=TEXTO_SUAVE, bg=fondo,
                     activebackground=fondo, activeforeground=AZUL, relief="flat", bd=0,
                     highlightthickness=0, cursor="hand2")


def desactivar(boton):
    """Desactiva un botón primario y lo pinta gris."""
    boton.configure(state="disabled", bg=GRIS_DESACTIVADO, cursor="arrow")


def logo(padre, fondo, tamano=40, color=MARINO):
    """Lupa dibujada (sin archivos de imagen): círculo + mango."""
    lienzo = tk.Canvas(padre, width=tamano, height=tamano, bg=fondo, highlightthickness=0)
    grosor = max(3, tamano // 10)
    lienzo.create_oval(grosor, grosor, tamano * 0.68, tamano * 0.68, outline=color, width=grosor)
    lienzo.create_line(tamano * 0.6, tamano * 0.6, tamano - grosor, tamano - grosor,
                       fill=color, width=grosor + 2, capstyle="round")
    return lienzo


def icono_categoria(padre, categoria, tamano=220, fondo=AZUL_SUAVE):
    """Ícono ilustrativo del objeto: círculo del color de su categoría con la inicial."""
    lienzo = tk.Canvas(padre, width=tamano, height=tamano, bg=fondo, highlightthickness=0)
    color = COLORES_CATEGORIA.get(categoria, MARINO)
    margen = tamano * 0.18
    lienzo.create_oval(margen, margen, tamano - margen, tamano - margen, fill=color, outline="")
    lienzo.create_text(tamano / 2, tamano / 2, text=categoria[0], fill=BLANCO,
                       font=fuente(int(tamano * 0.25), "bold"))
    return lienzo
