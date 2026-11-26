"""Vista Listado: conteo por estado, búsqueda, filtros y tabla profesional de objetos encontrados."""
import tkinter as tk
from tkinter import messagebox, ttk

from app import estilos
from app.logica import objetos, reclamos

# Columnas de la tabla: clave -> (título, ancho)
COLUMNAS = {
    "id": ("ID", 50), "nombre": ("Objeto", 220), "categoria": ("Categoría", 105),
    "lugar": ("Lugar del hallazgo", 170), "fecha": ("Fecha hallazgo", 115),
    "estado": ("Estado", 115), "entrega": ("Fecha entrega", 110), "accion": ("Acción", 110),
}
TEXTO_RECLAMAR = "Reclamar  ›"
TEXTO_BORRAR = "Borrar  ✕"


class PantallaListado(tk.Frame):
    def __init__(self, padre, app):
        super().__init__(padre, bg=estilos.FONDO, padx=32, pady=16)
        self.app = app
        self.es_admin = app.modo == "admin"  # El administrador no reclama: registra y borra objetos

        if app.modo == "admin":
            estilos.boton_enlace(self, "←  Volver al panel", lambda: app.mostrar("panel_admin")).pack(anchor="w")

        self._crear_encabezado()
        self._crear_filtros()
        self._crear_tabla()
        self.actualizar()

    def _crear_encabezado(self):
        """Título y botón de reporte a la izquierda; tarjetas de conteo (clicables) a la derecha."""
        fila = tk.Frame(self, bg=estilos.FONDO)
        fila.pack(fill="x", pady=(4, 14))
        izquierda = tk.Frame(fila, bg=estilos.FONDO)
        izquierda.pack(side="left", anchor="n")
        estilos.texto(izquierda, "Objetos encontrados", 26, "bold", fondo=estilos.FONDO).pack(anchor="w")
        estilos.texto(izquierda, "Explora y busca entre los objetos encontrados en Inspección.", 12,
                      color=estilos.TEXTO_SUAVE, fondo=estilos.FONDO).pack(anchor="w")
        if self.es_admin:
            texto, destino = "+  Registrar objeto perdido", "registrar_objeto"
        else:
            texto, destino = "+  Reportar objeto encontrado", "reportar"
        boton = estilos.boton_primario(izquierda, texto, lambda: self.app.mostrar(destino))
        boton.configure(bg=estilos.MARINO, activebackground=estilos.TEXTO)
        boton.pack(anchor="w", pady=(10, 0))

        # Tarjetas de conteo: al hacer clic filtran por ese estado
        conteo = objetos.contar_por_estado(self.app.datos)
        colores = {"Total": estilos.TEXTO, **{e: c[0] for e, c in estilos.COLORES_ESTADO.items()}}
        for nombre in ("Entregado", "Reclamado", "Disponible", "Total"):  # orden inverso por side="right"
            tarjeta = estilos.tarjeta(fila, relleno=10)
            tarjeta.pack(side="right", padx=(10, 0), anchor="n")
            titulo = estilos.texto(tarjeta, "Total" if nombre == "Total" else nombre + "s", 10,
                                   color=estilos.TEXTO_SUAVE, width=10, anchor="center")
            titulo.pack()
            numero = estilos.texto(tarjeta, str(conteo[nombre]), 22, "bold", colores[nombre], anchor="center")
            numero.pack()
            estado = objetos.TODOS if nombre == "Total" else nombre
            for widget in (tarjeta, titulo, numero):
                widget.configure(cursor="hand2")
                widget.bind("<Button-1>", lambda _, e=estado: self.filtrar_por_estado(e))

    def _crear_filtros(self):
        """Buscador por texto y filtros por categoría y estado; la tabla se actualiza al instante."""
        fila = tk.Frame(self, bg=estilos.FONDO)
        fila.pack(fill="x", pady=(0, 12))

        estilos.texto(fila, "Buscar:", 11, "bold", fondo=estilos.FONDO).pack(side="left")
        self.busqueda = tk.StringVar()
        ttk.Entry(fila, textvariable=self.busqueda, width=30).pack(side="left", padx=(8, 20))

        estilos.texto(fila, "Categoría:", 11, "bold", fondo=estilos.FONDO).pack(side="left")
        self.categoria = tk.StringVar(value=objetos.TODAS)
        combo_categoria = ttk.Combobox(fila, textvariable=self.categoria, state="readonly", width=12,
                                       values=[objetos.TODAS] + objetos.categorias(self.app.datos))
        combo_categoria.pack(side="left", padx=(8, 20))

        estilos.texto(fila, "Estado:", 11, "bold", fondo=estilos.FONDO).pack(side="left")
        self.estado = tk.StringVar(value=objetos.TODOS)
        combo_estado = ttk.Combobox(fila, textvariable=self.estado, state="readonly", width=12,
                                    values=[objetos.TODOS] + objetos.ESTADOS)
        combo_estado.pack(side="left", padx=8)

        estilos.boton_secundario(fila, "Limpiar filtros", self.limpiar).pack(side="right")

        # trace_add: cualquier cambio en búsqueda, categoría o estado vuelve a filtrar la tabla
        for variable in (self.busqueda, self.categoria, self.estado):
            variable.trace_add("write", lambda *_: self.actualizar())
        for combo in (combo_categoria, combo_estado):
            combo.bind("<<ComboboxSelected>>", lambda _, c=combo: c.selection_clear())

    def _crear_tabla(self):
        """Tabla dentro de una tarjeta blanca, con filas coloreadas por estado y columna «Acción»."""
        abajo = tk.Frame(self, bg=estilos.FONDO)
        abajo.pack(side="bottom", fill="x", pady=(12, 0))
        self.mensaje = estilos.texto(abajo, "", 11, color=estilos.TEXTO_SUAVE, fondo=estilos.FONDO)
        self.mensaje.pack(side="left")
        # Botón de acción: «Reclamar» para estudiantes/profesores, «Borrar objeto» (rojo) para el administrador
        self.color_accion = estilos.ERROR if self.es_admin else estilos.AZUL
        self.boton_accion = estilos.boton_primario(abajo, "Borrar objeto" if self.es_admin else "Reclamar",
                                                   self.borrar if self.es_admin else self.reclamar)
        self.boton_accion.pack(side="right")
        estilos.boton_secundario(abajo, "Ver detalle  →", self.ver_detalle).pack(side="right", padx=10)

        self.marco_tabla = estilos.tarjeta(self, relleno=0)
        self.marco_tabla.pack(fill="both", expand=True)
        self.tabla = ttk.Treeview(self.marco_tabla, columns=list(COLUMNAS), show="headings", selectmode="browse")
        for clave, (titulo, ancho) in COLUMNAS.items():
            self.tabla.heading(clave, text=titulo, anchor="w")
            self.tabla.column(clave, width=ancho, minwidth=50, anchor="w", stretch=clave in ("nombre", "lugar"))
        for estado, (color, fondo_suave) in estilos.COLORES_ESTADO.items():
            self.tabla.tag_configure(estado, background=fondo_suave)
        desplazamiento = ttk.Scrollbar(self.marco_tabla, orient="vertical", command=self.tabla.yview)
        self.tabla.configure(yscrollcommand=desplazamiento.set)
        desplazamiento.pack(side="right", fill="y")
        self.tabla.pack(fill="both", expand=True)

        self.tabla.bind("<Double-1>", lambda _: self.ver_detalle())
        self.tabla.bind("<ButtonRelease-1>", self.clic_en_tabla)
        self.tabla.bind("<<TreeviewSelect>>", lambda _: self.actualizar_boton_accion())

        # Mensaje que reemplaza a la tabla cuando no hay resultados (regla del reto)
        self.sin_resultados = estilos.texto(self.marco_tabla, "", 13, color=estilos.TEXTO_SUAVE,
                                            anchor="center", justify="center")

    def actualizar(self):
        """Vuelve a llenar la tabla según la búsqueda y los filtros."""
        texto, categoria, estado = self.busqueda.get(), self.categoria.get(), self.estado.get()
        self.tabla.delete(*self.tabla.get_children())
        encontrados = objetos.filtrar(self.app.datos, texto, categoria, estado)
        for objeto in encontrados:
            if self.es_admin:
                accion = TEXTO_BORRAR
            else:
                accion = TEXTO_RECLAMAR if reclamos.puede_reclamar(objeto) else "—"
            self.tabla.insert("", "end", iid=str(objeto["id"]), tags=(objeto["estado"],), values=(
                f"{objeto['id']:02d}", objeto["nombre"], objeto["categoria"], objeto["lugar"],
                objeto["fecha_hallazgo"], "●  " + objeto["estado"], objeto["fecha_entrega"] or "—", accion))

        if encontrados:
            self.sin_resultados.place_forget()
            ayuda = "«Borrar» para quitar un objeto" if self.es_admin else "«Reclamar» en un objeto disponible"
            self.mensaje.configure(text=f"{len(encontrados)} objeto(s). Doble clic para ver el detalle o pulsa {ayuda}.",
                                   fg=estilos.TEXTO_SUAVE)
        else:
            filtros = objetos.describir_filtros(texto, categoria, estado)
            self.sin_resultados.configure(text=f"No se encontraron objetos con: {filtros}.\n"
                                               "Prueba con otro filtro o pulsa «Limpiar filtros».")
            self.sin_resultados.place(relx=0.5, rely=0.5, anchor="center")
            self.mensaje.configure(text="0 objetos.", fg=estilos.TEXTO_SUAVE)
        self.actualizar_boton_accion()

    def objeto_seleccionado(self):
        seleccion = self.tabla.selection()
        return objetos.buscar_por_id(self.app.datos, int(seleccion[0])) if seleccion else None

    def actualizar_boton_accion(self):
        """Se activa con un objeto seleccionado; «Reclamar» además exige que esté Disponible."""
        objeto = self.objeto_seleccionado()
        activo = objeto is not None and (self.es_admin or reclamos.puede_reclamar(objeto))
        if activo:
            self.boton_accion.configure(state="normal", bg=self.color_accion, cursor="hand2")
        else:
            estilos.desactivar(self.boton_accion)

    def clic_en_tabla(self, evento):
        """Clic en la columna Acción: «Reclamar ›» abre el formulario; «Borrar ✕» (admin) borra el objeto."""
        fila = self.tabla.identify_row(evento.y)
        columna = self.tabla.identify_column(evento.x)
        if fila and columna == f"#{len(COLUMNAS)}":
            if self.es_admin:
                self.borrar()
            elif reclamos.puede_reclamar(objetos.buscar_por_id(self.app.datos, int(fila))):
                self.app.mostrar("reclamo", objeto_id=int(fila))

    def filtrar_por_estado(self, estado):
        """Clic en una tarjeta de conteo: muestra solo ese estado en todas las categorías."""
        self.busqueda.set("")
        self.categoria.set(objetos.TODAS)
        self.estado.set(estado)

    def limpiar(self):
        self.filtrar_por_estado(objetos.TODOS)

    def ver_detalle(self):
        objeto = self.objeto_seleccionado()
        if not objeto:
            self.mensaje.configure(text="Primero selecciona un objeto de la tabla.", fg=estilos.ERROR)
            return
        self.app.mostrar("detalle", objeto_id=objeto["id"])

    def borrar(self):
        """Solo administrador: quita el objeto del listado (pide confirmación)."""
        objeto = self.objeto_seleccionado()
        if not objeto or not messagebox.askyesno("Borrar objeto", f"¿Borrar «{objeto['nombre']}» del listado?"):
            return
        error = objetos.borrar_objeto(self.app.datos, objeto["id"])
        if error:
            self.mensaje.configure(text=error, fg=estilos.ERROR)
            return
        self.app.guardar()
        self.app.mostrar("listado")  # se recarga para actualizar también los contadores

    def reclamar(self):
        objeto = self.objeto_seleccionado()
        if objeto and reclamos.puede_reclamar(objeto):
            self.app.mostrar("reclamo", objeto_id=objeto["id"])
