"""Vista Confirmación: mensaje de éxito o de error y opción para volver al listado."""
import tkinter as tk

from app import estilos


class PantallaConfirmacion(tk.Frame):
    def __init__(self, padre, app, exito, titulo, detalle, objeto_id=None):
        super().__init__(padre, bg=estilos.FONDO, padx=32, pady=20)

        tarjeta = estilos.tarjeta(self, relleno=36)
        tarjeta.place(relx=0.5, rely=0.42, anchor="center")

        # Círculo verde con ✓ o rojo con ✕
        color = estilos.VERDE if exito else estilos.ERROR
        circulo = tk.Canvas(tarjeta, width=84, height=84, bg=estilos.BLANCO, highlightthickness=0)
        circulo.create_oval(2, 2, 82, 82, fill=color, outline="")
        circulo.create_text(42, 43, text="✓" if exito else "✕", fill=estilos.BLANCO, font=estilos.fuente(34, "bold"))
        circulo.pack()

        estilos.texto(tarjeta, titulo, 22, "bold", anchor="center").pack(pady=(14, 6))
        estilos.texto(tarjeta, detalle, 12, color=estilos.TEXTO_SUAVE, justify="center",
                      anchor="center", wraplength=460).pack()

        botones = tk.Frame(tarjeta, bg=estilos.BLANCO)
        botones.pack(pady=(22, 0))
        if not exito and objeto_id is not None:
            estilos.boton_secundario(botones, "Volver al detalle",
                                     lambda: app.mostrar("detalle", objeto_id=objeto_id)).pack(side="left", padx=6)
        estilos.boton_primario(botones, "Volver al listado", lambda: app.mostrar("listado")).pack(side="left", padx=6)
