# FIND IT — Objetos perdidos y encontrados del colegio

Reto «Encuéntralo» · Mentes que Programan 2026 · Categoría B (Software + IA).

Aplicación de **escritorio** para que la comunidad educativa consulte los objetos encontrados en Inspección y registre un reclamo.

## Cómo ejecutar

Requisitos: **Python 3.10 o superior** con Tkinter (viene incluido con Python). No necesita internet ni instalar librerías.

```bash
python main.py        # en Linux puede ser: python3 main.py
```

> En Linux, si falta Tkinter: `sudo apt install python3-tk`.

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
