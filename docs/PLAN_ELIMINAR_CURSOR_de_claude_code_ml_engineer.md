# Plan — quitar el contenido Cursor de `claude_code_ml_engineer`

> Objetivo: dejar `github.com/olonok69/claude_code_ml_engineer` como el curso **solo de Claude Code**
> (Parte 1 Claude Code + Parte 2 metodología agnóstica + Parte 3 grafo de tickets), sin el material
> específico de Cursor que se ha ido añadiendo en paralelo. Ese material vive ya (o vivirá, tras el
> segundo plan) en `github.com/olonok69/cursor_code_ml_engineer`.
>
> Inventario hecho sobre el clon local del repo real (commit `bb0249e` + los 3 ficheros `_CURSOR.md`
> añadidos localmente, aún sin push — ver nota al final). **No tengo credenciales de escritura sobre
> este repo** (confirmado al intentar el `git push` anterior), así que este documento es el
> **plan a ejecutar vosotros** (o un futuro agente con acceso), no algo que yo vaya a aplicar ya.

## Resumen: qué es de quién

| Categoría | Qué incluye |
|---|---|
| **Solo Cursor → eliminar** | `ejemplos_cursor/`, `docs/ai-agents-code-methodology/cursor/`, `CURSOR_ADAPTATION.md`, `CURSOR_WORKING_AGREEMENT_TEMPLATE.md`, `bootstrap-cursor-repo.ps1.txt`, `README_CURSOR.md`, `GUIA_PRESENTACION_CURSOR.md`, `GUIA_TECNICA_CURSOR.md` |
| **Solo Claude Code → se queda** | `ejemplos/`, `presentacion/Claude_Code_Presentacion*.pptx`, `presentacion/build_pptx.py`, `README.md`, `GUIA_PRESENTACION.md`, `GUIA_TECNICA.md`, `*_EN.md`, `docs/DISENO.md`, `docs/SETUP_CODEGRAPH_GSD.md` |
| **Compartido/agnóstico → se queda, pero 3 ficheros necesitan editarse** | `docs/knowledge-graph/`, `docs/synchro/`, `docs/ai-agents-code-methodology/{README,START_HERE,TRANSFER_AND_BOOTSTRAP,PACKAGE_MANIFEST,NEW_REPO_CONFIGURATION_PLAN}.md`, `COPILOT_ADAPTATION.md` + su template, `presentacion/capture_kg_graph.py`, `presentacion/kg_graph.png` |

---

## A. Eliminar sin más (ficheros/carpetas 100% Cursor)

```bash
cd claude_code_ml_engineer

git rm -r ejemplos_cursor/
git rm -r docs/ai-agents-code-methodology/cursor/
git rm docs/ai-agents-code-methodology/CURSOR_ADAPTATION.md
git rm docs/ai-agents-code-methodology/templates/CURSOR_WORKING_AGREEMENT_TEMPLATE.md
git rm docs/ai-agents-code-methodology/scripts/bootstrap-cursor-repo.ps1.txt
git rm README_CURSOR.md GUIA_PRESENTACION_CURSOR.md GUIA_TECNICA_CURSOR.md
```

Estos tres últimos (`README_CURSOR.md`, `GUIA_PRESENTACION_CURSOR.md`, `GUIA_TECNICA_CURSOR.md`) son
los que generé en la sesión anterior — están commiteados en local (commit `3bc11be` sobre `master`) pero
**nunca llegaron a `origin`** porque el push falló por falta de credenciales. Si aún no han llegado al
repo real, este `git rm` no hace nada (no existen ahí) — confírmalo con `git status` / `git log` antes de
ejecutar el resto del plan.

## B. Editar (no eliminar) — ficheros que referencian lo que acabas de borrar

Estos ficheros mezclan Cursor y Claude Code/Copilot. Si borras `cursor/` y `CURSOR_ADAPTATION.md` sin
tocarlos, quedan enlaces rotos y instrucciones para una carpeta que ya no existe.

| Fichero | Líneas con referencias a limpiar | Qué hacer |
|---|---|---|
| `README.md` | 29, 46 | Quitar "adaptación a Cursor/Copilot" → dejar solo Copilot; quitar el inciso `(CURSOR_ADAPTATION.md, cursor/)`. Opcional: añadir una línea apuntando al curso hermano — ver plantilla abajo. |
| `GUIA_PRESENTACION.md` | 386 (mención suelta de "Cursor" como ejemplo de tool de handoff — inocua, opcional dejarla), 471, 494, 497–498 | La sección 10 ("Transferir la metodología") menciona Cursor y Copilot como los dos destinos. Quitar el bloque de Cursor (`CURSOR_ADAPTATION.md`, `cursor/`, `bootstrap-cursor-repo.ps1`), dejar solo Copilot. Sustituir por la plantilla de abajo. |
| `GUIA_TECNICA.md` | 27 (índice: "Cursor / Copilot" → solo "Copilot"), 477–479, 498–500 | Igual que arriba: quitar el bloque `## Cursor:` de la sección 14, dejar solo Copilot + lo compartido. |
| `docs/ai-agents-code-methodology/README.md` | 39, 41, 46, 48 | Quitar el punto que describe `CURSOR_ADAPTATION.md` + la superficie `cursor/`; dejar solo el punto de Copilot. |
| `docs/ai-agents-code-methodology/START_HERE.md` | 7, 18, 23–31, 39–45, 57, 60 | Tiene una sección entera "Fast path — Cursor" (líneas ~23-45) y una fila de tabla comparativa Cursor/Copilot (línea 18). Eliminar la sección Cursor completa; dejar solo el fast-path de Copilot. |
| `docs/ai-agents-code-methodology/TRANSFER_AND_BOOTSTRAP.md` | 34, 50, 54–73, 79, 81, 93 | El bloque "C2) Cursor surface" (líneas ~54-73) entero + las menciones sueltas de Cursor en C1/verificación. Dejar solo lo aplicable a Copilot + lo genérico (ledgers compartidos). |
| `docs/ai-agents-code-methodology/PACKAGE_MANIFEST.md` | 9, 31, 33–46, 51, 58, 60 | Sección entera `## Cursor surface pack (cursor/)` (líneas ~33-46) + la entrada `CURSOR_ADAPTATION.md` (línea 9) + `CURSOR_WORKING_AGREEMENT_TEMPLATE.md` (línea 31) + el paso 4 de Cursor en el bootstrap (línea 58). |
| `docs/ai-agents-code-methodology/NEW_REPO_CONFIGURATION_PLAN.md` | 12, 18, 25, 26 | Cuatro líneas sueltas "(Cursor) …" o "**If using Cursor:**" dentro de listas — borrarlas o quedarte solo con la rama Copilot de cada una. |
| `docs/KNOWLEDGE_GRAPH.md` | — (no tiene referencias directas a Cursor, usa sintaxis `/kg` de Claude Code) | Sin cambios obligatorios — es la versión "canónica" en sintaxis Claude Code, coherente con que este repo es el volumen Claude Code. |

**Plantilla sugerida** para sustituir cada bloque "Cursor" que quites (mantiene la idea de que el método
viaja, sin listar Cursor como destino soportado en este repo):

> *La metodología también se ha transferido a Cursor — ver el curso hermano
> [`cursor_code_ml_engineer`](https://github.com/olonok69/cursor_code_ml_engineer), que reutiliza el
> mismo flujo de 11 etapas y el mismo grafo de tickets sobre la superficie de Cursor.*

## C. Casos límite — decide tú antes de borrar

- **`COPILOT_ADAPTATION.md` + `templates/COPILOT_WORKING_AGREEMENT_TEMPLATE.md`**: no es contenido
  Cursor, así que por defecto se quedan (es la prueba de portabilidad a un tercer agente que usan las
  guías). Bórralos solo si quieres que este repo hable *exclusivamente* de Claude Code sin mencionar
  ninguna transferencia.
- **`docs/DISENO.md`**: es el documento de diseño original de "presentación y guía sobre Claude Code" —
  100% específico de este repo, no toca a Cursor. Se queda tal cual.
- **`docs/SETUP_CODEGRAPH_GSD.md`**: instala CodeGraph **y** GSD (GSD solo existe en Claude Code) y da
  por hecho `~/.claude`, `/gsd-*`, "reinicia Claude Code" — es legítimamente específico de este repo.
  Se queda tal cual.
- **Menciones sueltas de "Cursor" como ejemplo de tool de handoff** (`GUIA_PRESENTACION.md:386`,
  `ejemplos/metodologia/WORKFLOW.md:72`, `ejemplos/metodologia/EJEMPLO_REAL.md:103,125`,
  `docs/synchro/machine-sync/LAPTOP_START_HERE.md`, `RUNBOOK.md`): aquí "Cursor" se usa solo como
  *ejemplo* de "un tool que el humano usa para hacer el push" (no como material didáctico de Cursor) —
  no hace falta tocarlas, son inocuas y hasta ilustran bien que el handoff es agnóstico de herramienta.

## D. Checklist de verificación tras la limpieza

```bash
# 1. Que no quede ninguna referencia rota a lo que borraste
grep -rniL "" . --include="*.md" >/dev/null 2>&1
grep -rni "cursor_adaptation\|cursor/README\|\bejemplos_cursor\b\|bootstrap-cursor-repo" . \
  --include="*.md" --include="*.yml" --include="*.json"

# 2. Que el índice de docs/ai-agents-code-methodology/ siga siendo coherente (solo Copilot + genérico)
cat docs/ai-agents-code-methodology/README.md

# 3. Que el deck y el generador de Claude Code sigan intactos
python presentacion/build_pptx.py   # debe seguir generando Claude_Code_Presentacion.pptx sin errores

# 4. Commit + push
git add -A
git commit -m "Quitar contenido Cursor: ahora vive en cursor_code_ml_engineer"
git push origin master
```

Si prefieres no tocar la prosa de las 5 guías meta (`README`, `START_HERE`, `TRANSFER_AND_BOOTSTRAP`,
`PACKAGE_MANIFEST`, `NEW_REPO_CONFIGURATION_PLAN`) ahora mismo, el mínimo indispensable es **A**
(borrar) — el repo queda funcional, solo con algunos enlaces muertos a `cursor/…` dentro de esos 5
ficheros hasta que hagas **B**.
