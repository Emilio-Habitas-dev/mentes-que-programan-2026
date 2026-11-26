"""Vista Reportar objeto encontrado (estudiante o profesor): avisa a Inspección que encontró un objeto."""
import tkinter as tk

from app import datos, estilos
from app.logica import reportes
from app.logica.validaciones import CATEGORIAS, GRADOS, PARALELOS, validar_foto
from app.pantallas.componentes import Campo, llenar_con_usuario, mostrar_errores
from app.pantallas.selector_foto import elegir_foto


class PantallaReportar(tk.Frame):
    def __init__(self, padre, app):
        super().__init__(padre, bg=estilos.FONDO, padx=32, pady=12)
        self.app = app
        estilos.boton_enlace(self, "←  Volver al listado", lambda: app.mostrar("listado")).pack(anchor="w")

        tarjeta = estilos.tarjeta(self, relleno=22)
        tarjeta.pack(pady=(4, 0))
        estilos.texto(tarjeta, "Reportar objeto encontrado", 22, "bold").grid(row=0, column=0, columnspan=2, sticky="w")
        estilos.texto(tarjeta, "¿Encontraste algo? Repórtalo y guárdalo: cuando aparezca el dueño te avisaremos "
                               "en ✉ la hora de entrega en el edificio administrativo.", 11, color=estilos.TEXTO_SUAVE, wraplength=520).grid(
            row=1, column=0, columnspan=2, sticky="w", pady=(2, 8))

        self.campos = {
            "nombre": Campo(tarjeta, "Nombre"),
            "apellido": Campo(tarjeta, "Apellido"),
            "correo": Campo(tarjeta, "Correo institucional"),
            "grado": Campo(tarjeta, "Grado", "lista", GRADOS),
            "paralelo": Campo(tarjeta, "Paralelo", "lista", PARALELOS),
            "objeto": Campo(tarjeta, "Objeto encontrado"),
            "categoria": Campo(tarjeta, "Categoría", "lista", CATEGORIAS),
            "lugar": Campo(tarjeta, "Dónde lo encontraste"),
            "descripcion": Campo(tarjeta, "Descripción del objeto", "texto", ancho=52, contador=True),
        }
        # (fila, columna); columna None = ocupa las dos columnas
        posiciones = {"nombre": (2, 0), "apellido": (2, 1), "correo": (3, None), "grado": (4, 0),
                      "paralelo": (4, 1), "objeto": (5, 0), "categoria": (5, 1), "lugar": (6, 0),
                      "descripcion": (7, None)}
        for clave, (fila, columna) in posiciones.items():
            if columna is None:
                self.campos[clave].marco.grid(row=fila, column=0, columnspan=2, sticky="new", pady=2)
            else:
                self.campos[clave].marco.grid(row=fila, column=columna, sticky="new", pady=2,
                                              padx=(0, 10) if columna == 0 else (10, 0))
        self.campos["descripcion"].control.configure(height=2)

        # Foto opcional del objeto (PNG o GIF)
        self.ruta_foto = None
        marco_foto = tk.Frame(tarjeta, bg=estilos.BLANCO)
        marco_foto.grid(row=6, column=1, sticky="new", pady=2, padx=(10, 0))
        estilos.texto(marco_foto, "Foto del objeto (opcional)", 11, "bold").pack(anchor="w", pady=(0, 4))
        estilos.boton_secundario(marco_foto, "Elegir foto…", self.elegir_foto).pack(anchor="w")
        self.texto_foto = estilos.texto(marco_foto, "PNG o GIF", 9, color=estilos.TEXTO_SUAVE)
        self.texto_foto.pack(anchor="w")

        botones = tk.Frame(tarjeta, bg=estilos.BLANCO)
        botones.grid(row=8, column=0, columnspan=2, sticky="ew", pady=(8, 0))
        estilos.boton_primario(botones, "Enviar reporte", self.enviar).pack(side="right")
        estilos.boton_secundario(botones, "Cancelar", lambda: app.mostrar("listado")).pack(side="right", padx=10)
        if app.usuario:
            llenar_con_usuario(self.campos, app.usuario)
            self.campos["objeto"].control.focus()
        else:
            self.campos["nombre"].control.focus()

    def elegir_foto(self):
        ruta = elegir_foto(self)
        if ruta:
            self.ruta_foto = ruta
            nombre = ruta.split("/")[-1]
            self.texto_foto.configure(text="✓ " + (nombre if len(nombre) <= 28 else nombre[:25] + "…"), fg=estilos.VERDE)

    def enviar(self):
        valores = {clave: campo.valor() for clave, campo in self.campos.items()}
        error_foto = validar_foto(self.ruta_foto)
        if error_foto:
            self.texto_foto.configure(text=error_foto, fg=estilos.ERROR)
            return
        usuario_id = self.app.usuario["id"] if self.app.usuario else None
        errores, reporte = reportes.registrar_reporte(self.app.datos, **valores, usuario_id=usuario_id)
        if errores:
            mostrar_errores(self.campos, errores)
            return
        if self.ruta_foto:  # La foto se copia a data/fotos con el número del reporte
            reporte["foto"] = datos.guardar_foto(self.ruta_foto, f"reporte_{reporte['id']}")
        self.app.guardar()
        self.app.mostrar("confirmacion", exito=True, titulo="¡Gracias por reportarlo!",
                         detalle=f"El administrador revisará tu reporte de «{reporte['objeto']}».\n"
                                 "Guárdalo: te avisaremos en ✉ cuando aparezca el dueño y la hora de entrega.")
