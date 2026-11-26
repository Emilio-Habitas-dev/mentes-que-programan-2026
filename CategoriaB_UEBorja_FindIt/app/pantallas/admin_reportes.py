"""Vista Reportes de objetos encontrados (administrador): al recibir el objeto se agrega al listado."""
from tkinter import messagebox

from app.logica import reportes
from app.pantallas.tabla_admin import PantallaTablaAdmin


class PantallaReportes(PantallaTablaAdmin):
    TITULO = "Reportes de objetos encontrados"
    SUBTITULO = "Revisa el reporte y publícalo en el listado; quien lo encontró recibe un mensaje."
    VACIO = "No hay reportes pendientes."
    COLUMNAS = {
        "objeto": ("Objeto", 150), "categoria": ("Categoría", 95), "lugar": ("Dónde se encontró", 140),
        "descripcion": ("Descripción", 200), "persona": ("Reportado por", 140), "correo": ("Correo", 200),
        "curso": ("Curso", 85), "fecha": ("Fecha", 95), "foto": ("Foto", 60),
    }

    def __init__(self, padre, app):
        super().__init__(padre, app, [("Descartar", self.descartar, False),
                                      ("Aprobar y publicar en el listado", self.agregar, True)])

    def filas(self):
        return [(r["id"], (r["objeto"], r["categoria"], r["lugar"], r["descripcion"],
                           f"{r['nombre']} {r['apellido']}", r.get("correo", "—"), r["curso"], r["fecha"],
                           "Sí" if r.get("foto") else "No"))
                for r in reportes.pendientes(self.app.datos)]

    def agregar(self):
        reporte_id = self.seleccionado()
        if reporte_id is None or not messagebox.askyesno(
                "Publicar en el listado", "¿Publicar este objeto en el listado como Disponible?"):
            return
        nuevo = reportes.agregar_al_listado(self.app.datos, reporte_id)
        self.app.guardar()
        self.actualizar()
        self.avisar(f"«{nuevo['nombre']}» agregado al listado con el ID {nuevo['id']:02d}.")

    def descartar(self):
        reporte_id = self.seleccionado()
        if reporte_id is None or not messagebox.askyesno("Descartar", "¿Descartar este reporte?"):
            return
        reportes.descartar(self.app.datos, reporte_id)
        self.app.guardar()
        self.actualizar()
        self.avisar("Reporte descartado.")
