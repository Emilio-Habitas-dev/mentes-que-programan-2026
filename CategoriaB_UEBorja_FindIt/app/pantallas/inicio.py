"""Vista Inicio: identidad de FIND IT (amarillo y negro), explicación breve y elección de rol."""
import tkinter as tk

from app import estilos


class PantallaInicio(tk.Frame):
    def __init__(self, padre, app):
        super().__init__(padre, bg=estilos.AMARILLO)
        self.app = app
        amarillo = estilos.AMARILLO

        # Bloque central: se mantiene centrado aunque se cambie el tamaño de la ventana
        centro = tk.Frame(self, bg=amarillo)
        centro.place(relx=0.5, rely=0.45, anchor="center")

        tk.Label(centro, text="FIND IT", font=estilos.fuente(64, "bold", "italic"),
                 fg=estilos.NEGRO, bg=amarillo).pack()
        tk.Label(centro, text="Reporta y encuentra tus\nobjetos más rápido",
                 font=estilos.fuente(17, "bold", "italic"), fg=estilos.NEGRO, bg=amarillo).pack()
        tk.Label(centro, text="Consulta los objetos que se encontraron en el colegio, búscalos por nombre o "
                              "categoría y registra un reclamo si alguno es tuyo.",
                 font=estilos.fuente(12), fg=estilos.NEGRO, bg=amarillo, wraplength=520).pack(pady=(16, 22))

        tk.Label(centro, text="Acceder como:", font=estilos.fuente(20, "bold", "italic"),
                 fg=estilos.NEGRO, bg=amarillo).pack(pady=(0, 10))
        self._boton_rol(centro, "ADMINISTRADOR", lambda: app.mostrar("login"))
        self._boton_rol(centro, "ESTUDIANTE\nO PROFESOR", self.entrar_estudiante)

    def _boton_rol(self, padre, contenido, comando):
        """Botón negro con borde azul, como en el boceto."""
        borde = tk.Frame(padre, bg=estilos.AZUL_BORDE, padx=4, pady=4)
        borde.pack(pady=6)
        tk.Button(borde, text=contenido, command=comando, font=estilos.fuente(13, "bold", "italic"),
                  fg=estilos.BLANCO, bg=estilos.NEGRO, activebackground="#222222", activeforeground=estilos.BLANCO,
                  relief="flat", bd=0, width=24, height=2, cursor="hand2").pack()

    def entrar_estudiante(self):
        """Estudiantes y profesores inician sesión o crean su cuenta."""
        self.app.mostrar("acceso")
