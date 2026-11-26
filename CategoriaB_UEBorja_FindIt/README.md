# FIND IT — Objetos perdidos y encontrados del colegio

Reto «Encuéntralo» · Mentes que Programan 2026 · Categoría B (Software + IA).

Aplicación de **escritorio** para que la comunidad educativa consulte los objetos encontrados en Inspección y registre un reclamo.

## Cómo ejecutar

Requisitos: **Python 3.10 o superior** con Tkinter (viene incluido con Python). No necesita internet ni instalar librerías.

```bash
python main.py        # en Linux puede ser: python3 main.py
```

> En Linux, si falta Tkinter: `sudo apt install python3-tk`.

## Versión web (Flask)

Usa la misma lógica (`app/logica/`) y los mismos datos (`data/`) que la versión de escritorio; solo cambia la interfaz (`web.py`, `templates/`, `static/`).

```bash
pip install -r requirements.txt     # instala Flask (una sola vez)
python web.py                       # abre el servidor
```

- En este equipo: **http://localhost:5000**
- Otro equipo en la **misma red wifi**: **http://IP-de-este-equipo:5000** (la IP se ve con `hostname -I` en Linux o `ipconfig` en Windows).
- Si no conecta, el cortafuegos puede estar bloqueando: en Ubuntu `sudo ufw allow 5000/tcp`.
- Para detener el servidor: `Ctrl + C` en la terminal.

## Ejecutables (Windows, Linux y macOS)

GitHub Actions (`.github/workflows/ejecutables.yml`) construye un ejecutable de la versión web con PyInstaller en cada `push` a `main`.
Se descargan en GitHub → pestaña **Actions** → la última ejecución → **Artifacts** (`FindIt-Windows`, `FindIt-Linux`, `FindIt-macOS`).

- Al abrir el ejecutable se inicia el servidor y se abre el navegador en `http://localhost:5000`. No cierres la ventana de la terminal.
- Los datos se guardan en una carpeta `data/` junto al ejecutable.
- Linux/macOS: dar permiso con `chmod +x FindIt`. En macOS, la primera vez: clic derecho → Abrir.
- Otro puerto: `PUERTO=5050 ./FindIt`.

## Cómo usar

- **Estudiante o profesor:** crea su cuenta con su correo institucional (debe contener `.edu`) e inicia sesión. Ve el listado, busca o filtra, reclama un objeto Disponible o reporta uno que encontró (con foto PNG/GIF opcional). Los avisos llegan al buzón ✉.
- **Flujo de entrega:** reporte → el administrador lo publica → alguien lo reclama → el administrador coordina la hora → mensajes al dueño y a quien lo encontró → «Marcar como entregado».
- **Administrador:** usuario `prueba1`, contraseña `prueba-administrador`.
  Son **credenciales ficticias de demostración** (en `data/credenciales_demo.json`), no seguridad real.
  Puede marcar objetos Reclamados como Entregados y restablecer los datos de prueba.

## Datos

- `data/datos_iniciales.json`: los 10 objetos de prueba del reto (no se modifica).
- `data/datos.json`: se crea al abrir la app por primera vez; guarda los cambios. Para volver al inicio: Administrador → Opciones, o borrar este archivo.

## Estructura

```
main.py              Punto de entrada
app/ventana.py       Ventana principal y navegación entre vistas
app/estilos.py       Colores, fuentes y piezas visuales reutilizables
app/datos.py         Lectura y guardado de los JSON
app/logica/          Reglas del sistema y validaciones (sin interfaz)
app/pantallas/       Una vista por archivo
docs/                Plan, bocetos y reto
```

## Recursos de terceros

- Sonido de clic (`recursos/clic.wav`): recortado de «Mouse Button Click» de sarthakraj_308 (Pixabay, licencia de contenido de Pixabay, uso gratuito).

## Equipo

- **Emilio Navas** ([@Emilio-Habitas-dev](https://github.com/Emilio-Habitas-dev))
- **JoseOrdo0502** ([@josepotato0522-gif](https://github.com/josepotato0522-gif))

Unidad Educativa Borja · Mentes que Programan 2026.
