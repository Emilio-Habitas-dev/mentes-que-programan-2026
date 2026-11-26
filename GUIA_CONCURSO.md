# Guía — Mentes que Programan 2026 (Categoría B: Software con IA)

> Fuente: `~/Descargas/Reglamento_Mentes_Software.pdf` · Concurso: **jueves 26 nov 2026**, UCACUE, Cuenca.

---

## 1. Contexto y cómo trabajar

- Es un concurso de programación para **estudiantes de bachillerato**. El día del concurso se entrega un **reto** (enunciado) y hay que construir una aplicación que lo resuelva.
- **Tiempo de desarrollo (Categoría B, según Anexo C.2 del reglamento): 09:00–15:00 (6 h)**, incluida la entrega. Descontando la presentación del reto (15 min) y la pausa de comida (30 min) quedan **~5 h de trabajo**, y los últimos ~35 min son para documentación, declaración de IA y entrega. Es decir, **~4 h 30 min para construir la app**.
- Aun así el alcance debe ser **pequeño y realista**: pocas pantallas, pocas funciones, todo funcionando. Recortar alcance antes que dejar algo a medias.
- Ojo: el Anexo C es un **ejemplo**, no el horario oficial; el reto definitivo y su horario se confirman al inicio. Verificar con la organización si cambia.
- Las **defensas son sin IA**: los estudiantes explican y modifican el código en vivo. El código debe ser **simple y entendible** por quien lo defiende.
- **Stack acordado: Python** (el equipo lo domina; no conoce HTML/web). App de **escritorio con Tkinter** (viene con Python, no requiere instalar nada).
- **Todo debe funcionar sin internet** ni servicios externos: sin APIs web, sin bases de datos en la nube, sin CDN, sin descargas en tiempo de ejecución. Datos guardados en archivos locales (JSON).
- La **declaración de uso de IA (Anexo B) la redacta el equipo a mano**. No se llena automáticamente.

### Reglas para escribir el código

- Solo librería estándar de Python (`tkinter`, `json`, `datetime`, `os`…). Evitar dependencias externas.
- Funciones cortas y nombres claros en español o inglés (consistentes).
- **Incluir comentarios en el código** para guiar al jurado/público y al propio equipo: un comentario al inicio de cada archivo (qué hace) y uno breve por función o bloque importante (qué hace y por qué). Sin exagerar: explicar la intención, no repetir lo obvio.
- Sin trucos ni "magia" que los estudiantes no puedan explicar.
- Solo datos ficticios. **Nunca** claves, contraseñas ni credenciales en el código ni en prompts.
- Citar cualquier recurso de terceros (íconos, imágenes) y respetar licencias.

## 2. Rúbrica (100 pts) y cómo ganarla

| Criterio | Pts | Qué hacer para puntuar |
|---|---|---|
| Creatividad, innovación y valor | 20 | Ir más allá del mínimo del enunciado con 1–2 funciones diferenciadoras útiles y pequeñas (filtro, búsqueda, resumen, confirmación). |
| Análisis y diseño | 15 | Ficha técnica clara: usuarios, alcance, funciones. Mapa de navegación + bocetos coherentes con lo construido. |
| Estructura, calidad y comprensión del código | 20 | Archivos por responsabilidad, nombres claros, funciones cortas, comentarios breves. Todo explicable. |
| Funcionalidad e integración | 20 | **Que todo funcione de verdad**: navegación completa, **validación de formularios**, datos guardados, mensajes de error/éxito. |
| Uso responsable de IA | 10 | Declaración (Anexo B) honesta: herramientas, tareas, 2 prompts, qué se corrigió/descartó, pruebas hechas. |
| Defensa técnica y demostración | 15 | Guion ensayado; cada integrante explica una parte; saber justificar **una decisión técnica**. |

**Desempate** (en orden): Funcionalidad e integración → Estructura/código → Defensa. ⇒ **Prioridad #1: que funcione sin fallos.**

## 3. Entregables obligatorios

1. Aplicación funcional + **código fuente** accesible + **instrucciones de ejecución** (README).
2. **Ficha técnica**: problema, usuarios, objetivo, plataforma, tecnologías, funciones (también Anexo A).
3. **Mapa de navegación** + bocetos/esquemas de las pantallas principales.
4. **Declaración de uso de IA** (Anexo B), escrita por el equipo.
5. Demostración + explicación de **una decisión técnica**.

**Cómo se entrega:** el reglamento solo pide un "archivo, repositorio o medio de entrega" y **no fija cuál**. Confirmarlo con la organización al inicio. Mientras tanto, estructurar el proyecto para que sea **autocontenido en una sola carpeta** (código, datos, README y `docs/`), fácil de comprimir en un `.zip` o subir a un repositorio, y que corra en otro equipo con solo `python main.py`. Registrar la hora de entrega.

## 4. Estructura de proyecto recomendada (Python + Tkinter)

```
proyecto/
├── README.md              # Cómo ejecutar (python main.py) + resumen
├── main.py                # Punto de entrada: crea la ventana y arranca la app
├── docs/
│   ├── plan.md            # Plan de desarrollo (se crea y se ajusta con el reto)
│   ├── ficha_tecnica.md   # Anexo A
│   ├── navegacion.md      # Mapa de navegación (diagrama simple)
│   └── bocetos/           # Fotos o imágenes de bocetos
├── data/
│   └── datos_demo.json    # Datos ficticios; también guarda registros nuevos
└── app/
    ├── pantallas/         # Una ventana/frame por pantalla (listado, detalle, formulario…)
    ├── logica/            # Reglas de negocio y validaciones (sin código de interfaz)
    └── datos.py           # Leer/escribir el JSON
```

Patrón habitual en este tipo de reto (ejemplo oficial "Servicios estudiantiles"): **Listado → Detalle → Formulario de registro → Confirmación**, con validación de formularios y datos de demostración.

## 5. Plan general de desarrollo

| Fase | Tarea | Salida |
|---|---|---|
| 1. Reto | Leer el reto y las condiciones de IA | — |
| 2. Plan | Crear el plan de desarrollo con el reto (`docs/plan.md`) y ajustarlo si cambia el alcance o el tiempo | Plan de desarrollo |
| 3. Análisis | Usuarios, problema, funciones (MVP + extras pequeños) | Ficha técnica borrador |
| 4. Diseño | Mapa de navegación + bocetos | `docs/` |
| 5. Interfaz | Pantallas y componentes | Pantallas navegables |
| 6. Lógica | Formularios, validaciones, datos | MVP funcional |
| 7. Integración | Unir piezas, revisar y limpiar código | App coherente |
| 8. Pruebas | Pruebas + usabilidad + extras si sobra tiempo | Lista de pruebas |
| 9. Cierre | README, ficha, entrega (la declaración de IA la redacta el equipo) | Todo entregado |

Reglas: **primero el MVP funcionando**; los extras solo después. Con el tiempo limitado, recortar alcance antes que dejar algo a medias.

## 6. Defensa (máx. 11 min)

- **Peso y alcance de la app:** debe estar optimizada y ser lo bastante ligera para presentarse bien dentro de los tiempos indicados (abrir rápido, flujo principal corto de mostrar, sin pantallas de más).
- **En la defensa el jurado pregunta y puede pedir explicar o modificar** una parte del programa; los estudiantes responden y lo hacen **sin IA**.
- **5 min presentación**: problema → usuarios → solución → diseño (mapa/bocetos) → tecnologías → uso de IA.
- **3 min demo**: recorrido completo del flujo principal, incluida una **validación que falla** y luego un registro exitoso.
- **3 min preguntas**: estar listos para modificar en vivo (cambiar un texto, agregar un campo, cambiar una validación).
- Preparar la respuesta a "¿por qué eligieron X?" (decisión técnica, p. ej. por qué Python + Tkinter + JSON).

## 7. Checklist final antes de entregar

- [ ] Se creó el plan de desarrollo (`docs/plan.md`) y se siguió.
- [ ] La app arranca sin internet, solo con `python main.py`, y todo está en una sola carpeta lista para entregar (medio confirmado).
- [ ] Todas las pantallas del mapa existen y se navega entre ellas.
- [ ] Formularios validan (campos vacíos, formato, mensajes claros).
- [ ] Se comprimió el proyecto, se descomprimió en otra carpeta y funcionó con `python main.py` (sin rutas propias del equipo).
- [ ] Solo datos ficticios; sin claves ni credenciales.
- [ ] Ficha técnica, mapa y bocetos completos; declaración de IA redactada por el equipo.
- [ ] Recursos de terceros citados.
- [ ] Cada integrante puede explicar cualquier archivo de `app/`.
