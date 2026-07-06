# Prevalencia de herramientas — qué usa Claude y cuándo

El `CLAUDE.md` del proyecto no solo dice *qué* hacer; dice **con qué herramienta** y en qué orden. Esta es
la parte que convierte "tengo MCP instalado" en "el agente tira de la tool correcta automáticamente".

## La regla de oro: navegación por grafo antes que leer ficheros

> **"Para 'qué es esto / quién depende / qué toco', un `codegraph_explore` **primero** — fuente + rutas de
> llamada + blast radius + flags de cobertura de tests en una llamada (trata la fuente que devuelve como YA
> leída, no la re-abras). Serena `find_referencing_symbols` para el chequeo **preciso** antes de renombrar o
> eliminar un helper (desambigua por clase). grep/Read solo para literales."** — regla real del `CLAUDE.md`.

Por qué es una *regla* y no una sugerencia: los ficheros clave tienen 4.000–6.000 líneas. Leerlos enteros
es caro (tokens) e impreciso. CodeGraph devuelve el símbolo, sus callers, sus tests y **qué se rompe al
cambiarlo** en un solo round-trip; Serena desambigua un símbolo homónimo por clase antes de un rename —
donde el `impact` plano de CodeGraph los mezclaría.

## Tabla de prevalencia

| Necesito… | Herramienta preferida | Por qué / regla |
|---|---|---|
| Survey: "qué es / quién depende / qué se rompe / ¿está testeado?" | **CodeGraph** `codegraph_explore` | Fuente + rutas de llamada + blast radius + cobertura en 1 consulta (incluye dispatch dinámico que grep no sigue). Trátala como YA leída. |
| Chequeo preciso antes de un rename/borrado | **Serena** `find_referencing_symbols` | **Obligatorio**; desambigua homónimos por clase (el `impact` de CodeGraph los mezcla). |
| Cuerpo de un símbolo / overview de un fichero de 5k líneas | **Serena** `find_symbol body=true` / `get_symbols_overview` | O la fuente que ya imprimió `codegraph_explore`. |
| Verificar el **contrato de salida** (lo que ve el consumidor) | **Playwright** / F12 en el navegador | Subir un doc → "Review & Import" → inspeccionar el JSON del `status endpoint`. El bug se reproduce ahí. |
| Diagnosticar causa raíz **barato** | **Oráculo determinista** (parser, validador, `_diag_*.py`) | Misma respuesta siempre, coste 0. Antes de gastar en el LLM. |
| Diagnosticar entorno (logs, config de Lambda, colas) | **AWS CLI** (CloudWatch, `aws lambda get-function`, SQS/DLQ) | Herramienta de debugging de primera clase, no último recurso. |
| Docs de una librería externa | **Context7** | En vez de fiarse del corte de entrenamiento del modelo. |
| Estado de git / PRs para orientarse | **`gh` CLI**, `git branch -a`, `git log` | "status-first": no ramificar de la base equivocada. |
| Trabajo genuinamente independiente en paralelo | **Subagentes** (`Task`: Explore/Plan/…) | Sin ensuciar el contexto principal. |

## El orden importa (barato → caro, determinista → probabilístico)

1. **Orientación:** markdown local (`STATUS.md`, ledgers) + `git`/`gh` — coste 0.
2. **Navegación:** CodeGraph `codegraph_explore` (survey, 1 llamada) → Serena `find_referencing_symbols` (chequeo preciso antes de renombrar) — coste bajo, determinista.
3. **Diagnóstico:** oráculo determinista (parser/validador) — coste 0, reproducible.
4. **Verificación de entorno:** AWS CLI — read-only, determinista.
5. **Verificación del contrato:** Playwright/F12 — reproducir el síntoma en la salida real.
6. **Solo al final:** la tirada del LLM (metered, probabilística) para verificar el fix acabado.

> La inversión clásica —"tirar del modelo para diagnosticar"— es justo lo que este orden evita: el modelo
> es caro y no determinista; úsalo para *verificar*, no para *diagnosticar*.

## Permisos: el allowlist refleja esta prevalencia

El `settings.local.json` del proyecto es un allowlist **hand-curated** (cientos de reglas específicas, no
comodines): invocaciones exactas de pytest, operaciones git acotadas, `aws lambda/sts/configure`, y las
tools MCP concretas de Serena (`find_symbol`, `search_for_pattern`, `activate_project`, `find_file`),
CodeGraph (`codegraph_explore`) y Playwright (`browser_navigate`, `browser_console_messages`,
`browser_take_screenshot`, `browser_evaluate`).
`deny` y `ask` van vacíos porque el allowlist ya es la barrera — y el humano es dueño de las acciones
externas (push/PR/deploy no están en la lista).
