"""Vista Acceso (estudiantes y profesores): iniciar sesión o crear una cuenta con el correo institucional."""
import tkinter as tk

from app import estilos
from app.logica import usuarios
from app.logica.validaciones import GRADOS, PARALELOS, ROLES
from app.pantallas.componentes import Campo, mostrar_errores

GRADOS_CUENTA = [g for g in GRADOS if g != "Docente"]


class PantallaAcceso(tk.Frame):
    def __init__(self, padre, app):
        super().__init__(padre, bg=estilos.FONDO, padx=32, pady=16)
        self.app = app
        estilos.boton_enlace(self, "←  Volver al inicio", lambda: app.mostrar("inicio")).pack(anchor="w")
        estilos.texto(self, "Bienvenido/a a FIND IT", 26, "bold", fondo=estilos.FONDO).pack(anchor="w")
        estilos.texto(self, "Inicia sesión o crea tu cuenta con tu correo institucional.", 12,
                      color=estilos.TEXTO_SUAVE, fondo=estilos.FONDO).pack(anchor="w", pady=(0, 12))

        cuerpo = tk.Frame(self, bg=estilos.FONDO)
        cuerpo.pack(fill="both", expand=True)
        cuerpo.columnconfigure(0, weight=2, uniform="c")
        cuerpo.columnconfigure(1, weight=3, uniform="c")
        self._crear_login(cuerpo)
        self._crear_registro(cuerpo)

    def _crear_login(self, cuerpo):
        tarjeta = estilos.tarjeta(cuerpo, relleno=24)
        tarjeta.grid(row=0, column=0, sticky="new", padx=(0, 12))
        estilos.texto(tarjeta, "Iniciar sesión", 18, "bold").pack(anchor="w", pady=(0, 10))
        self.login = {"correo": Campo(tarjeta, "Correo institucional"),
                      "clave": Campo(tarjeta, "Contraseña", oculto=True)}
        for campo in self.login.values():
            campo.marco.pack(fill="x", pady=4)
            campo.control.bind("<Return>", lambda _: self.ingresar())
        self.error_login = estilos.texto(tarjeta, "", 10, color=estilos.ERROR, wraplength=300)
        self.error_login.pack(fill="x")
        estilos.boton_primario(tarjeta, "Iniciar sesión", self.ingresar).pack(fill="x", pady=(10, 0))

    def _crear_registro(self, cuerpo):
        tarjeta = estilos.tarjeta(cuerpo, relleno=24)
        tarjeta.grid(row=0, column=1, sticky="new", padx=(12, 0))
        tarjeta.columnconfigure((0, 1), weight=1)
        estilos.texto(tarjeta, "Crear cuenta", 18, "bold").grid(row=0, column=0, columnspan=2, sticky="w", pady=(0, 6))
        self.registro = {
            "nombre": Campo(tarjeta, "Nombre"),
            "apellido": Campo(tarjeta, "Apellido"),
            "rol": Campo(tarjeta, "Soy", "lista", ROLES),
            "grado_clase": Campo(tarjeta, "Grado en que das clases (profesores)", "lista", GRADOS_CUENTA),
            "grado": Campo(tarjeta, "Grado (estudiantes)", "lista", GRADOS_CUENTA),
            "paralelo": Campo(tarjeta, "Paralelo (estudiantes)", "lista", PARALELOS),
            "correo": Campo(tarjeta, "Correo institucional"),
            "clave": Campo(tarjeta, "Contraseña (mín. 6)", oculto=True),
            "confirmar": Campo(tarjeta, "Repite la contraseña", oculto=True),
        }
        # (fila, columna); None = ocupa las dos columnas
        posiciones = {"nombre": (1, 0), "apellido": (1, 1), "rol": (2, 0), "grado_clase": (2, 1),
                      "grado": (3, 0), "paralelo": (3, 1), "correo": (4, None), "clave": (5, 0), "confirmar": (5, 1)}
        for clave, (fila, columna) in posiciones.items():
            marco = self.registro[clave].marco
            if columna is None:
                marco.grid(row=fila, column=0, columnspan=2, sticky="new", pady=2)
            else:
                marco.grid(row=fila, column=columna, sticky="new", pady=2, padx=(0, 8) if columna == 0 else (8, 0))
        fila = 5

        # El rol decide qué campos se usan: estudiante -> grado y paralelo; profesor -> grado en que da clases
        self.registro["rol"].control.bind("<<ComboboxSelected>>", lambda _: self.actualizar_rol())
        self.registro["rol"].poner("Estudiante")
        self.actualizar_rol()
        # Verificación en vivo de que las contraseñas coinciden
        for clave in ("clave", "confirmar"):
            # after_idle: se revisa después de que el campo borre su error anterior
            self.registro[clave].variable.trace_add("write", lambda *_: self.after_idle(self.revisar_claves))

        mostrar = tk.BooleanVar()
        tk.Checkbutton(tarjeta, text="Mostrar contraseñas", variable=mostrar, bg=estilos.BLANCO,
                       activebackground=estilos.BLANCO, font=estilos.fuente(10),
                       command=lambda: self.alternar_claves(mostrar.get())).grid(row=fila + 1, column=0, sticky="w")
        estilos.boton_primario(tarjeta, "Crear cuenta", self.crear_cuenta).grid(row=fila + 1, column=1, sticky="e", pady=(8, 0))

    def actualizar_rol(self):
        es_profesor = self.registro["rol"].valor() == "Profesor"
        self.registro["grado_clase"].habilitar(es_profesor)
        self.registro["grado"].habilitar(not es_profesor)
        self.registro["paralelo"].habilitar(not es_profesor)

    def revisar_claves(self):
        """Mientras se escribe «Repite la contraseña», avisa si no es igual a la primera."""
        clave, confirmar = self.registro["clave"].valor(), self.registro["confirmar"].valor()
        if confirmar and clave != confirmar:
            self.registro["confirmar"].marcar("Las contraseñas no coinciden.")
        else:
            self.registro["confirmar"].marcar(None)

    def alternar_claves(self, visibles):
        for campos in (self.login, self.registro):
            for clave in ("clave", "confirmar"):
                if clave in campos:
                    campos[clave].control.configure(show="" if visibles else "•")

    def ingresar(self):
        self.app.recargar()  # por si la cuenta se creó en otra ventana
        error, usuario = usuarios.iniciar_sesion(self.app.datos, self.login["correo"].valor(), self.login["clave"].valor())
        if error:
            self.error_login.configure(text=error)
            return
        self.app.iniciar_sesion_usuario(usuario)

    def crear_cuenta(self):
        valores = {clave: campo.valor() for clave, campo in self.registro.items()}
        grado_clase = valores.pop("grado_clase")
        es_profesor = valores["rol"] == "Profesor"
        if es_profesor:  # Para el profesor, «grado» es el grado en el que da clases
            valores["grado"] = grado_clase
        self.app.recargar()  # para no repetir un correo registrado en otra ventana
        errores, usuario = usuarios.registrar(self.app.datos, **valores)
        if errores:
            if es_profesor and "grado" in errores:  # el error se muestra en el campo que usa el profesor
                errores["grado_clase"] = errores.pop("grado")
            mostrar_errores(self.registro, errores)
            return
        self.app.guardar()
        self.app.iniciar_sesion_usuario(usuario)  # Al crear la cuenta entra directamente
