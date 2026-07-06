# Prevalencia de herramientas — qué usa Claude y cuándo

El `CLAUDE.md` del proyecto no solo dice *qué* hacer; dice **con qué herramienta** y en qué orden. Esta es
la parte que convierte "tengo MCP instalado" en "el agente tira de la tool correcta automáticamente".

## La regla de oro: navegación semántica antes que leer ficheros

> **"Usa las tools simbólicas de Serena (`get_symbols_overview`, `find_symbol`, `find_referencing_symbols`)
> antes de abrir ficheros de extractor de 4k–6k líneas. Siempre `find_referencing_symbols` antes de
> renombrar o eliminar un helper."** — regla real del `CLAUDE.md`.

Por qué es una *regla* y no una sugerencia: los ficheros clave tienen 4.000–6.000 líneas. Leerlos enteros
es caro (tokens) e impreciso. Serena devuelve el símbolo, sus callers y sus tests sin cargar el fichero.

## Tabla de prevalencia

| Necesito… | Herramienta preferida | Por qué / regla |
|---|---|---|
| Entender un fichero grande, encontrar un símbolo | **Serena** `get_symbols_overview` → `find_symbol body=true` | Antes de abrir ficheros de 5k líneas. |
| Saber quién llama a algo / impacto de un rename | **Serena** `find_referencing_symbols` | **Obligatorio** antes de refactorizar/borrar. |
| "¿Quién llama a esto y qué se rompe si lo cambio?" a escala | **CodeGraph** `codegraph_explore` | Fuente + rutas de llamada + blast radius en 1 consulta (incluye dispatch dinámico que grep no sigue). |
| Verificar el **contrato de salida** (lo que ve el consumidor) | **Playwright** / F12 en el navegador | Subir un doc → "Review & Import" → inspeccionar el JSON del `status endpoint`. El bug se reproduce ahí. |
| Diagnosticar causa raíz **barato** | **Oráculo determinista** (parser, validador, `_diag_*.py`) | Misma respuesta siempre, coste 0. Antes de gastar en el LLM. |
| Diagnosticar entorno (logs, config de Lambda, colas) | **AWS CLI** (CloudWatch, `aws lambda get-function`, SQS/DLQ) | Herramienta de debugging de primera clase, no último recurso. |
| Docs de una librería externa | **Context7** | En vez de fiarse del corte de entrenamiento del modelo. |
| Estado de git / PRs para orientarse | **`gh` CLI**, `git branch -a`, `git log` | "status-first": no ramificar de la base equivocada. |
| Trabajo genuinamente independiente en paralelo | **Subagentes** (`Task`: Explore/Plan/…) | Sin ensuciar el contexto principal. |

## El orden importa (barato → caro, determinista → probabilístico)

1. **Orientación:** markdown local (`STATUS.md`, ledgers) + `git`/`gh` — coste 0.
2. **Navegación:** Serena / CodeGraph — coste bajo, determinista.
3. **Diagnóstico:** oráculo determinista (parser/validador) — coste 0, reproducible.
4. **Verificación de entorno:** AWS CLI — read-only, determinista.
5. **Verificación del contrato:** Playwright/F12 — reproducir el síntoma en la salida real.
6. **Solo al final:** la tirada del LLM (metered, probabilística) para verificar el fix acabado.

> La inversión clásica —"tirar del modelo para diagnosticar"— es justo lo que este orden evita: el modelo
> es caro y no determinista; úsalo para *verificar*, no para *diagnosticar*.

## Permisos: el allowlist refleja esta prevalencia

El `settings.local.json` del proyecto es un allowlist **hand-curated** (cientos de reglas específicas, no
comodines): invocaciones exactas de pytest, operaciones git acotadas, `aws lambda/sts/configure`, y las
tools MCP concretas de Serena (`find_symbol`, `search_for_pattern`, `activate_project`, `find_file`) y
Playwright (`browser_navigate`, `browser_console_messages`, `browser_take_screenshot`, `browser_evaluate`).
`deny` y `ask` van vacíos porque el allowlist ya es la barrera — y el humano es dueño de las acciones
externas (push/PR/deploy no están en la lista).
