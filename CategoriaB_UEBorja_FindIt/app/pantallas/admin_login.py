"""Vista Login del administrador: usuario y contraseña (oculta con puntos y botón para mostrarla).
Las credenciales son FICTICIAS de demostración y están en data/credenciales_demo.json."""
import tkinter as tk
from tkinter import ttk

from app import estilos
from app.logica import acceso

PUNTO = "•"  # Carácter que oculta la contraseña


class PantallaLogin(tk.Frame):
    def __init__(self, padre, app):
        super().__init__(padre, bg=estilos.FONDO)
        self.app = app

        centro = tk.Frame(self, bg=estilos.FONDO)
        centro.place(relx=0.5, rely=0.47, anchor="center")
        estilos.texto(centro, "¡Bienvenido/a, Administrador/a!", 26, "bold", fondo=estilos.FONDO,
                      anchor="center").pack(pady=(0, 18))

        tarjeta = estilos.tarjeta(centro, relleno=32)
        tarjeta.pack()
        self._avatar(tarjeta).pack(pady=(0, 14))

        estilos.texto(tarjeta, "Nombre de usuario", 12, "bold").pack(fill="x", pady=(0, 4))
        self.usuario = tk.StringVar()
        campo_usuario = ttk.Entry(tarjeta, textvariable=self.usuario, width=38)
        campo_usuario.pack(fill="x")

        estilos.texto(tarjeta, "Contraseña", 12, "bold").pack(fill="x", pady=(14, 4))
        fila = tk.Frame(tarjeta, bg=estilos.BLANCO)
        fila.pack(fill="x")
        self.clave = tk.StringVar()
        self.campo_clave = ttk.Entry(fila, textvariable=self.clave, show=PUNTO)
        self.campo_clave.pack(side="left", fill="x", expand=True)
        self.boton_ver = estilos.boton_secundario(fila, "Mostrar", self.alternar_clave)
        self.boton_ver.configure(width=8, pady=5)
        self.boton_ver.pack(side="left", padx=(8, 0))

        self.error = estilos.texto(tarjeta, "", 10, color=estilos.ERROR)
        self.error.pack(fill="x", pady=(8, 0))

        boton = estilos.boton_primario(tarjeta, "Iniciar sesión", self.ingresar)
        boton.configure(bg=estilos.MARINO, activebackground=estilos.TEXTO)
        boton.pack(fill="x", pady=(14, 0))
        estilos.boton_enlace(centro, "←  Volver al inicio", lambda: app.mostrar("inicio")).pack(pady=(14, 0))

        # Enter también inicia sesión
        for campo in (campo_usuario, self.campo_clave):
            campo.bind("<Return>", lambda _: self.ingresar())
        campo_usuario.focus()

    def _avatar(self, padre):
        """Ícono de usuario dibujado: círculo con cabeza y cuerpo."""
        lienzo = tk.Canvas(padre, width=96, height=96, bg=estilos.BLANCO, highlightthickness=0)
        lienzo.create_oval(3, 3, 93, 93, fill=estilos.AZUL_SUAVE, outline=estilos.MARINO, width=3)
        lienzo.create_oval(34, 20, 62, 48, fill=estilos.AZUL, outline="")
        lienzo.create_arc(20, 52, 76, 108, start=0, extent=180, fill=estilos.AZUL, outline="")
        return lienzo

    def alternar_clave(self):
        """Muestra u oculta la contraseña."""
        oculta = self.campo_clave.cget("show") == PUNTO
        self.campo_clave.configure(show="" if oculta else PUNTO)
        self.boton_ver.configure(text="Ocultar" if oculta else "Mostrar")

    def ingresar(self):
        error = acceso.verificar(self.usuario.get(), self.clave.get())
        if error:
            self.error.configure(text=error)
            self.clave.set("")
            return
        self.app.modo = "admin"
        self.app.mostrar("panel_admin")
