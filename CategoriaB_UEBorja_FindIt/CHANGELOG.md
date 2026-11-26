# Registro de cambios — FIND IT

| Hora | Fase del plan | Cambio |
|---|---|---|
| 10:45 | Plan | Creada la carpeta del proyecto, copiados bocetos y reto a `docs/`, y creado `docs/plan.md`. |
| 11:07 | Base | `main.py`, `app/ventana.py` (barra superior + cambio de vistas), `app/estilos.py` (identidad visual), `app/datos.py` (JSON con datos iniciales + copia de trabajo). |
| 11:07 | Base | `data/datos_iniciales.json` con los 10 objetos de prueba y `data/credenciales_demo.json` (prueba1 / prueba-administrador, ficticias). |
| 11:07 | Lógica | `logica/validaciones.py`, `objetos.py` (filtros, conteo, Entregado), `reclamos.py` (regla Disponible → Reclamado), `acceso.py` (login demo). |
| 11:07 | Interfaz | Vistas del flujo: Inicio (amarillo/negro), Listado (tabla profesional, conteo, búsqueda, filtros, mensaje sin resultados), Detalle, Formulario de reclamo (errores por campo y contador de seña), Confirmación. |
| 11:07 | Interfaz | Vistas de administrador: Login (contraseña oculta con puntos + botón Mostrar/Ocultar), Panel (4 tarjetas), Solicitudes de reclamo (marcar como Entregado). |
| 11:07 | Pruebas | Reglas del reto y recorrido por todas las vistas probados automáticamente; README creado. |
| 11:22 | Lógica | Estados centralizados en `objetos.cambiar_estado` (Disponible → Reclamado → Entregado; Reclamado → Disponible al rechazar). Reclamos con estado Pendiente/Entregado/Rechazado. |
| 11:22 | Lógica | Validaciones: nombre y apellido separados, grado + paralelo (curso), reportes de objetos perdidos (`logica/reportes.py`). |
| 11:22 | Interfaz | Listado: botón «Reportar objeto perdido», columna Acción «Reclamar ›» y botón Reclamar (solo Disponible), tarjetas de conteo que filtran por estado, mensaje sin resultados con los filtros activos. |
| 11:22 | Interfaz | Formularios con componente común (`pantallas/componentes.py`): reclamo con nombre/apellido/grado/paralelo y nueva vista `reportar.py`. |
| 11:22 | Interfaz | Administrador: Solicitudes solo con reclamos reales (Entregar / Rechazar), nueva vista Reportes; base común `tabla_admin.py`. |
| 11:22 | Plan | Plan actualizado con los formularios, estados y pruebas nuevas. |
| 11:30 | Datos | Los 10 objetos iniciales empiezan Disponibles (sin reclamos ni entregas iniciales); conteos siempre calculados de los datos reales. |
| 11:30 | Lógica | Grados: todos los niveles (Inicial 1–2, 1ro–10mo EGB, 1ro–3ro BGU, Docente). Correo obligatorio con formato válido en el reclamo. |
| 11:30 | Interfaz | Campo Correo (de preferencia institucional) en el reclamo; columna Correo en Solicitudes del administrador; campos alineados arriba. |
| 11:40 | Lógica | Reportes ahora son de objetos **encontrados** (con correo institucional). `reportes.agregar_al_listado` crea el objeto Disponible con los datos del reporte; `descartar` lo cierra. |
| 11:40 | Interfaz | Vista «Reportar objeto encontrado» (correo, dónde lo encontraste). Administrador: «Recibido: agregar al listado» y «Descartar», con columna Correo. Ventana un poco más alta (780 px). |
| 11:46 | Lógica | `objetos.crear_objeto` (usado por el administrador y por los reportes), `registrar_objeto` con validación (fecha AAAA-MM-DD no futura) y `borrar_objeto` (bloqueado si hay reclamo pendiente). |
| 11:46 | Interfaz | Administrador no puede reclamar: en listado y detalle el botón es «Borrar objeto» (rojo, con confirmación) y la columna Acción dice «Borrar ✕». Nuevo botón «+ Registrar objeto perdido» y vista `registrar_objeto.py` (solo datos del objeto). |
| 11:52 | Interfaz | Tablas del administrador (Solicitudes y Reportes): panel inferior con la fila seleccionada completa, en dos columnas y con los textos largos en varias líneas. |
| 12:38 | Lógica | Cuentas de estudiantes y profesores (`logica/usuarios.py`): registro con correo institucional (.edu), rol, grado (profesor: grado en que da clases), contraseña cifrada con PBKDF2 + sal; inicio de sesión. |
| 12:38 | Lógica | Buzón (`logica/mensajes.py`). Reportes guardan usuario y foto; al publicarlos se avisa a quien encontró el objeto. Reclamos: nuevo estado Coordinado con hora de entrega en el edificio administrativo; mensajes al dueño y a quien encontró. Rechazo avisa al dueño. |
| 12:38 | Interfaz | Vista Acceso (iniciar sesión / crear cuenta, mostrar contraseñas) y Buzón (✉ con contador de no leídos en la barra). Formularios se llenan con los datos de la cuenta. Foto PNG/GIF en el reporte y en el detalle. Administrador: «Coordinar entrega» (hora) y «Aprobar y publicar en el listado». |
| 12:45 | Interfaz | Crear cuenta: campos separados «Grado (estudiantes)» y «Grado en que das clases (profesores)»; el rol desactiva los que no aplican. Contraseñas verificadas en vivo; los errores se borran al corregir el campo. |
| 12:49 | Datos | La app vuelve a leer `datos.json` al cambiar de vista y antes de iniciar sesión o crear cuenta: con varias ventanas abiertas ya no se pierden cuentas ni cambios. |
| 12:57 | Interfaz | Nuevo selector de foto (`pantallas/selector_foto.py`): carpetas rápidas (Descargas, Imágenes, Escritorio, Documentos, personal), buscador por nombre, fotos más recientes primero y vista previa. Reemplaza al selector de Tkinter. |
| 12:58 | Interfaz | Sonido de clic en todos los botones (`app/sonido.py`, `recursos/clic.wav` recortado del audio descargado; fuente citada en el README). |
| 13:25 | Web | Versión web con Flask (`web.py`, `templates/`, `static/estilos.css`, `requirements.txt`): todas las vistas (inicio, cuentas, listado con filtros, detalle con foto, reclamo, reporte con foto JPG/PNG, buzón, administrador). Misma lógica y mismos datos que la versión de escritorio. Servidor en 0.0.0.0:5000. |
| 13:36 | Interfaz/Web | Mensaje al dueño corregido (se le pedirá describir la seña del objeto). Notificaciones en vivo cada 4 s: ✉ en escritorio y web, contadores del panel web (`/api/notificaciones`). Web más grande (letra 18 px, botones, tablas y panel) e inicio web en azul marino con FIND IT en amarillo. |
| 13:42 | Lógica/Web | Coordinar entrega con fecha (no pasada), hora y lugar (por defecto el edificio administrativo), en escritorio y web; mensajes con la fecha exacta. Web: Opciones del administrador (cambiar nombre, usuario y contraseña pidiendo la actual y repitiendo la nueva; se guarda cifrada) y Administrar usuarios (fecha de registro, editar datos/contraseña, borrar cuenta). |
| 13:44 | Interfaz/Web | Quitado el texto «N objetos disponibles para reclamar» del Inicio (escritorio y web). |
