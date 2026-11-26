"""Ventana sencilla para elegir la foto del objeto: carpetas rápidas, buscador por nombre y vista previa.
Reemplaza al selector de archivos de Tkinter, que en Linux es difícil de usar."""
import os
import tkinter as tk
from pathlib import Path
from tkinter import filedialog, ttk

from app import estilos
from app.logica.validaciones import FORMATOS_FOTO

# Carpetas rápidas (nombres en español y en inglés según el idioma del sistema)
CARPETAS_RAPIDAS = [("Descargas", ("Descargas", "Downloads")), ("Imágenes", ("Imágenes", "Pictures")),
                    ("Escritorio", ("Escritorio", "Desktop")), ("Documentos", ("Documentos", "Documents"))]
PROFUNDIDAD = 3      # cuántos niveles de subcarpetas se revisan
MAXIMO = 400         # máximo de fotos listadas (para que sea rápido)


def buscar_fotos(carpeta):
    """Fotos PNG/GIF dentro de la carpeta y sus subcarpetas (hasta PROFUNDIDAD niveles)."""
    fotos = []
    base = len(Path(carpeta).parts)
    for raiz, subcarpetas, archivos in os.walk(carpeta):
        if len(Path(raiz).parts) - base >= PROFUNDIDAD:
            subcarpetas.clear()
        subcarpetas[:] = [c for c in subcarpetas if not c.startswith(".")]  # sin carpetas ocultas
        for archivo in archivos:
            if archivo.lower().endswith(FORMATOS_FOTO):
                fotos.append(Path(raiz) / archivo)
                if len(fotos) >= MAXIMO:
                    return fotos
    return sorted(fotos, key=lambda ruta: ruta.stat().st_mtime, reverse=True)  # las más recientes primero


def elegir_foto(padre):
    """Abre la ventana y devuelve la ruta elegida (texto) o None si se cancela."""
    ventana = SelectorFoto(padre)
    padre.wait_window(ventana)
    return ventana.resultado


class SelectorFoto(tk.Toplevel):
    def __init__(self, padre):
        super().__init__(padre, bg=estilos.FONDO, padx=20, pady=16)
        self.title("Elegir foto del objeto")
        self.geometry("860x520")
        self.transient(padre.winfo_toplevel())
        self.resultado = None
        self.fotos = []
        self.vista = None

        estilos.texto(self, "Elige la foto del objeto (PNG o GIF)", 16, "bold", fondo=estilos.FONDO).pack(anchor="w")
        estilos.texto(self, "1) Elige una carpeta  2) Busca por nombre  3) Haz clic en la foto y pulsa «Usar esta foto».",
                      10, color=estilos.TEXTO_SUAVE, fondo=estilos.FONDO).pack(anchor="w", pady=(0, 10))

        cuerpo = tk.Frame(self, bg=estilos.FONDO)
        cuerpo.pack(fill="both", expand=True)
        cuerpo.columnconfigure(1, weight=1)
        cuerpo.rowconfigure(0, weight=1)

        # Izquierda: carpetas rápidas
        carpetas = tk.Frame(cuerpo, bg=estilos.FONDO)
        carpetas.grid(row=0, column=0, sticky="ns", padx=(0, 12))
        estilos.texto(carpetas, "Carpetas", 11, "bold", fondo=estilos.FONDO).pack(anchor="w", pady=(0, 4))
        self.botones = {}
        casa = Path.home()
        opciones = [(nombre, next((casa / n for n in nombres if (casa / n).is_dir()), None))
                    for nombre, nombres in CARPETAS_RAPIDAS] + [("Carpeta personal", casa)]
        for nombre, ruta in opciones:
            if ruta:
                boton = estilos.boton_secundario(carpetas, nombre, lambda r=ruta, n=nombre: self.abrir_carpeta(r, n))
                boton.configure(anchor="w", width=16)
                boton.pack(fill="x", pady=2)
                self.botones[nombre] = boton
        estilos.boton_secundario(carpetas, "Otra carpeta…", self.otra_carpeta).pack(fill="x", pady=(12, 0))

        # Centro: buscador y lista de fotos
        centro = tk.Frame(cuerpo, bg=estilos.FONDO)
        centro.grid(row=0, column=1, sticky="nsew")
        self.busqueda = tk.StringVar()
        fila = tk.Frame(centro, bg=estilos.FONDO)
        fila.pack(fill="x", pady=(0, 6))
        estilos.texto(fila, "Buscar:", 11, "bold", fondo=estilos.FONDO).pack(side="left")
        entrada = ttk.Entry(fila, textvariable=self.busqueda)
        entrada.pack(side="left", fill="x", expand=True, padx=(8, 0))
        self.busqueda.trace_add("write", lambda *_: self.filtrar())
        self.lista = tk.Listbox(centro, font=estilos.fuente(11), activestyle="none", selectbackground=estilos.AZUL,
                                highlightthickness=1, highlightbackground=estilos.BORDE, relief="flat")
        self.lista.pack(fill="both", expand=True)
        self.lista.bind("<<ListboxSelect>>", lambda _: self.previsualizar())
        self.lista.bind("<Double-1>", lambda _: self.usar())
        self.estado = estilos.texto(centro, "", 10, color=estilos.TEXTO_SUAVE, fondo=estilos.FONDO)
        self.estado.pack(anchor="w")

        # Derecha: vista previa
        derecha = estilos.tarjeta(cuerpo, relleno=10)
        derecha.grid(row=0, column=2, sticky="ns", padx=(12, 0))
        self.previa = tk.Label(derecha, text="Vista previa", width=26, height=12, bg=estilos.AZUL_SUAVE,
                               fg=estilos.TEXTO_SUAVE, font=estilos.fuente(10))
        self.previa.pack()

        botones = tk.Frame(self, bg=estilos.FONDO)
        botones.pack(fill="x", pady=(12, 0))
        estilos.boton_primario(botones, "Usar esta foto", self.usar).pack(side="right")
        estilos.boton_secundario(botones, "Cancelar", self.destroy).pack(side="right", padx=10)

        # Empieza en Descargas (o en la primera carpeta que exista)
        primera = next(iter(self.botones))
        self.botones[primera].invoke()
        entrada.focus()
        self.grab_set()  # ventana modal: hay que elegir o cancelar

    def abrir_carpeta(self, ruta, nombre):
        for etiqueta, boton in self.botones.items():
            boton.configure(bg=estilos.AZUL_SUAVE if etiqueta == nombre else estilos.BLANCO)
        self.estado.configure(text="Buscando fotos…")
        self.update_idletasks()
        self.carpeta = Path(ruta)
        self.fotos = buscar_fotos(ruta)
        self.filtrar()

    def otra_carpeta(self):
        ruta = filedialog.askdirectory(parent=self, initialdir=str(Path.home()), title="Elegir carpeta")
        if ruta:
            self.abrir_carpeta(ruta, None)

    def filtrar(self):
        """Muestra solo las fotos cuyo nombre contiene el texto buscado."""
        texto = self.busqueda.get().lower().strip()
        self.visibles = [f for f in self.fotos if texto in f.name.lower()]
        self.lista.delete(0, "end")
        for foto in self.visibles:
            carpeta = foto.parent.relative_to(self.carpeta) if foto.parent != self.carpeta else ""
            self.lista.insert("end", f"  {foto.name}" + (f"   (en {carpeta})" if carpeta else ""))
        if self.visibles:
            self.estado.configure(text=f"{len(self.visibles)} foto(s) PNG o GIF en {self.carpeta}")
        else:
            self.estado.configure(text=f"No hay fotos PNG o GIF que coincidan en {self.carpeta}")

    def seleccionada(self):
        seleccion = self.lista.curselection()
        return self.visibles[seleccion[0]] if seleccion else None

    def previsualizar(self):
        """Muestra la foto elegida en pequeño (máximo ~220 px)."""
        ruta = self.seleccionada()
        if not ruta:
            return
        try:
            foto = tk.PhotoImage(file=str(ruta))
            factor = max(1, -(-max(foto.width(), foto.height()) // 220))
            self.vista = foto.subsample(factor)
            self.previa.configure(image=self.vista, text="", width=self.vista.width(), height=self.vista.height())
        except tk.TclError:
            self.vista = None
            self.previa.configure(image="", text="No se puede mostrar\nesta imagen", width=26, height=12)

    def usar(self):
        ruta = self.seleccionada()
        if not ruta:
            self.estado.configure(text="Primero haz clic en una foto de la lista.", fg=estilos.ERROR)
            return
        self.resultado = str(ruta)
        self.destroy()
