# Plan de desarrollo — FIND IT (Reto "Encuéntralo")

> Objetos perdidos y encontrados del colegio. App de escritorio **Python + Tkinter**, datos en **JSON local**, sin internet. Se ejecuta con `python main.py`.
> **Hora límite: 14:00 se deja de programar.** 14:00–15:00 defensa (5 min exposición + 3 demo + 3 preguntas).

## 1. Requisitos del reto (marcar al final)

**Vistas mínimas**
- [ ] Inicio: nombre e identidad visual, explicación breve, menú y acceso a funciones.
- [ ] Listado: nombre, fecha del hallazgo, categoría y estado + búsqueda/filtro.
- [ ] Detalle: info completa, ícono ilustrativo y botón «Reclamar».
- [ ] Formulario de reclamo: validación de obligatorios con mensajes comprensibles.
- [ ] Confirmación: mensaje de éxito o error y botón para volver al listado.

**Reglas del sistema (el jurado las prueba)**
- [ ] Estados: Disponible, Reclamado, Entregado.
- [ ] «Reclamar» solo activo si el objeto está Disponible.
- [ ] Reclamo válido → objeto pasa a Reclamado y se ve en el listado.
- [ ] Formulario: nombre, curso y seña particular, todos obligatorios; seña ≥ 10 caracteres.
- [ ] Datos faltantes/incorrectos → no se registra y se explica qué corregir.
- [ ] Búsqueda/filtro sin resultados → mensaje.

**Técnicos**
- [ ] Ventana ordenada al redimensionar.
- [ ] Navegación entre las 5 vistas.
- [ ] Interacción real y almacenamiento local (JSON).
- [ ] Código organizado + README con instrucciones.
- [ ] Los 10 objetos de prueba cargados.

## 2. MVP y extras

**MVP (lo exigido, primero):** las 5 vistas del flujo Estudiante/Profesor, reglas del sistema, 10 objetos de prueba, guardado en JSON.

**Extras hechos:**
1. Conteo por estado (tarjetas clicables que filtran por ese estado).
2. Botón «Reclamar» en la tabla (columna Acción) y abajo, solo activo si el objeto está Disponible.
3. **Reportar objeto encontrado** (estudiante/profesor, con correo institucional) → el administrador, al recibirlo en Inspección, pulsa «Recibido: agregar al listado» y se crea como objeto Disponible con esos datos.
4. Login de administrador de demostración: `prueba1` / `prueba-administrador`, contraseña oculta con puntos y botón Mostrar/Ocultar.
5. Panel de administrador: solicitudes de reclamo (Entregar o Rechazar), reportes (marcar atendido), objetos, restablecer datos.



## 3. Pantallas y mapa de navegación

Basado en los bocetos de `docs/bocetos/`.

```
                  ┌──────────── INICIO (FIND IT) ────────────┐
                  │ logo · eslogan · explicación · conteos   │
                  │ [Estudiante o profesor]   [Administrador]│
                  └───────┬──────────────────────────┬───────┘
                          ▼                          ▼ (extra)
                   LISTADO DE OBJETOS          LOGIN ADMIN (demo)
              búsqueda + filtro categoría            ▼
                          ▼ (doble clic / Ver)   PANEL ADMIN
                       DETALLE                  ├─ Solicitudes de reclamo → marcar Entregado
                          ▼ [Reclamar]          ├─ Registrar objeto encontrado
                  FORMULARIO DE RECLAMO         └─ Opciones (restablecer datos)
                          ▼ [Enviar]
                     CONFIRMACIÓN ──► [Volver al listado]
```

| Vista | Boceto | Contenido | Acciones |
|---|---|---|---|
| Inicio | `01_inicio_boceto.png` | Logo FIND IT, eslogan, explicación breve, conteo por estado | Estudiante o profesor / Administrador |
| Listado | `04_listado_remaster.jpg` | Tabla: ID, objeto, categoría, fecha hallazgo, estado (con color), lugar | Buscar, filtrar por categoría, Ver detalle, Volver a inicio |
| Detalle | — | Ícono por categoría, todos los datos, estado | Reclamar (desactivado si no está Disponible), Volver |
| Formulario de reclamo | `07_formulario_reclamo_remaster.jpg` | Nombre, apellido, grado, paralelo, seña particular (contador en vivo) | Enviar / Cancelar |
| Reportar objeto encontrado | — | Nombre, apellido, correo institucional, grado, paralelo, objeto, categoría, dónde se encontró, descripción | Enviar / Cancelar |
| Confirmación | — | Éxito (objeto ahora Reclamado) o error | Volver al listado |
| Login admin | `02_login_admin_remaster.jpg` | Usuario y clave de demo | Ingresar / Volver |
| Panel admin | `03_panel_admin_remaster.jpg` | Tarjetas: solicitudes (con contador), registrar objeto, opciones | Abrir cada sección, Salir |

## 4. Identidad visual

- **Inicio:** fondo amarillo + texto/botones negros con borde azul (boceto 01). Es la marca de FIND IT.
- **Resto de vistas:** estilo de los remasters: fondo gris azulado claro, tarjetas blancas, azul marino como color principal.
- **Estado con color:** Disponible = verde, Reclamado = ámbar, Entregado = gris.
- **Ícono de detalle:** círculo de color por categoría dibujado en `tk.Canvas` con la inicial (no depende de imágenes externas ni de emojis).
- Colores y fuentes en un solo archivo: `app/estilos.py`.
- Bocetos `02`–`04` fueron remasterizados con IA (Gemini): incluirlo en la declaración de IA.

## 5. Datos y validaciones

- `data/datos_iniciales.json`: los 10 objetos de prueba del reto, **todos Disponibles** (decisión del equipo: los estados cambian solo por acciones reales en la app).
- `data/datos.json`: se crea copiando el inicial la primera vez; ahí se guardan los cambios (persisten al cerrar). "Restablecer" lo vuelve a copiar.

```json
{
  "objetos":  [{"id": 1, "nombre": "Chompa azul con capucha", "categoria": "Ropa", "lugar": "Cancha de básquet",
                "fecha_hallazgo": "2026-11-18", "estado": "Disponible", "descripcion": "Talla M con cierre plateado",
                "fecha_entrega": null}],
  "reclamos": [{"id": 1, "objeto_id": 1, "nombre": "", "apellido": "", "curso": "2do BGU A", "sena": "", "fecha": "", "estado": "Pendiente"}],
  "reportes": [{"id": 1, "nombre": "", "apellido": "", "curso": "", "objeto": "", "categoria": "", "lugar": "", "descripcion": "", "fecha": "", "estado": "Pendiente"}]
}
```

**Formularios y validaciones (`app/logica/validaciones.py`):**

| Campo | Reclamo | Reporte | Regla |
|---|---|---|---|
| Nombre / Apellido (separados) | ✔ | ✔ | Obligatorios, solo letras y espacios |
| Correo | ✔ | ✔ | Obligatorio, formato válido; se recomienda el institucional |
| Grado | ✔ | ✔ | Lista: Inicial 1–2, 1ro–10mo EGB, 1ro–3ro BGU, Docente |
| Paralelo | ✔ | ✔ | Lista A–D; no se pide a Docente. Grado + paralelo = curso (ej. «2do BGU A») |
| Seña particular | ✔ | — | Obligatoria, mínimo 10 caracteres |
| Objeto, categoría, dónde se encontró | — | ✔ | Obligatorios |
| Descripción | — | ✔ | Obligatoria, mínimo 10 caracteres |

- Los errores se muestran bajo cada campo, en rojo, y no se guarda nada.
- El objeto debe seguir Disponible al enviar el reclamo (si no, Confirmación muestra el error).

**Estados (`app/logica/objetos.py`, un solo lugar):** Disponible → Reclamado (reclamo) → Entregado (inspector). Reclamado → Disponible si el inspector rechaza el reclamo. Cualquier otro cambio se bloquea.
**Solicitudes:** solo las de reclamos hechos en la app (no hay solicitudes de datos iniciales).

## 6. Estructura de archivos

```
CategoriaB_UEBorja_FindIt/        ← nombre exigido: CategoriaB_Colegio_NombreDelProyecto
├── README.md · CHANGELOG.md · main.py
├── docs/   plan.md, ficha_tecnica.md, navegacion.md, bocetos/, reto_original.docx
├── data/   datos_iniciales.json, datos.json
└── app/
    ├── estilos.py        # Colores, fuentes, estilos ttk, chips de estado
    ├── datos.py          # Cargar, guardar y restablecer el JSON
    ├── ventana.py        # Ventana principal y cambio entre vistas
    ├── logica/
    │   ├── validaciones.py
    │   ├── objetos.py    # Buscar/filtrar, conteo por estado, cambiar estado
    │   └── reclamos.py   # Registrar reclamo (regla Disponible → Reclamado)
    └── pantallas/
        ├── inicio.py · listado.py · detalle.py · reclamo.py · confirmacion.py
        └── admin_login.py · admin_panel.py · registrar_objeto.py   (extras)
```

**Nota login demo:** la clave de demostración va en `data/` como dato ficticio y se documenta en el README; no es seguridad real (el reto prohíbe claves reales en el código). Si apura el tiempo, el botón Administrador entra directo al panel.

## 7. Reparto del equipo

| Integrante | Responsable de | Explica en la defensa |
|---|---|---|
| 1 | Interfaz: `estilos.py`, `ventana.py`, `pantallas/` | Navegación, diseño e identidad visual |
| 2 | Lógica: `logica/` (validaciones, reglas de estado, reclamos) | Reglas del sistema y validación |
| 3 | Datos y entregables: `datos.py`, JSON, ficha, mapa, README, declaración de IA; coordina pruebas | Datos y decisión técnica |

## 8. Orden de trabajo e hitos

| Hito | Contenido | Meta |
|---|---|---|
| 1. Base | `main.py`, `estilos.py`, `ventana.py`, `datos.py` + JSON con los 10 objetos | App abre en Inicio |
| 2. Flujo | Listado → Detalle → Reclamo → Confirmación con reglas y validaciones | **MVP completo antes de las 12:30** |
| 3. Integración | Revisión de código, comentarios, mensajes, redimensionado | 13:00 |
| 4. Extras | En el orden de la sección 2 | Hasta 13:40 |
| 5. Pruebas y cierre | Sección 9, README, ficha, `.zip` probado | **Código congelado a las 14:00** |

## 9. Pruebas (lo que revisará el jurado)

- [ ] Reclamar un objeto Disponible con datos válidos → Confirmación de éxito → en el listado aparece Reclamado.
- [ ] Objeto Reclamado o Entregado → botón «Reclamar» desactivado.
- [ ] Formulario vacío → no registra y marca cada campo que falta.
- [ ] Filtro por estado (combo o tarjeta de conteo) muestra solo ese estado; combinado sin resultados explica qué filtros están activos.
- [ ] Reclamo válido → aparece en Solicitudes del administrador → Entregar (pasa a Entregado) o Rechazar (vuelve a Disponible).
- [ ] Reporte de objeto encontrado → aparece en Reportes del administrador → «Agregar al listado» → aparece como Disponible y se puede reclamar.
- [ ] Seña con menos de 10 caracteres → error específico.
- [ ] Búsqueda sin coincidencias (ej. "xyz") → mensaje "No se encontraron objetos".
- [ ] Filtro por categoría muestra solo esa categoría.
- [ ] Cerrar y abrir la app → los cambios siguen.
- [ ] Redimensionar la ventana → todo sigue ordenado.

## 10. Decisión técnica para la defensa

Separar **pantallas** (lo que se ve), **lógica** (reglas de estado y validaciones) y **datos** (JSON). La regla "solo se reclama si está Disponible" vive en un solo lugar (`logica/reclamos.py`), así el botón y el registro usan la misma regla. Tkinter y JSON porque vienen con Python y la app funciona sin internet.
