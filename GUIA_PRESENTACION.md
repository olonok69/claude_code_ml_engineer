# Claude Code — Guía de presentación

> Guía narrativa para la charla + vídeo. Está pensada para el/la **ponente**: cada sección mapea a un
> bloque de slides del deck ([`presentacion/`](./presentacion/)) e incluye el hilo a contar, los puntos
> clave y una frase de cierre 🗣️ lista para la diapositiva. Audiencia: **técnica / desarrolladores**.
>
> El detalle de implementación (configs, código copy-paste) está en [`GUIA_TECNICA.md`](./GUIA_TECNICA.md)
> y en [`ejemplos/`](./ejemplos/).

---

## Índice

0. [Qué es Claude Code (encuadre)](#0-qué-es-claude-code)
1. [Instalación y uso básico](#1-instalación-y-uso-básico)
2. [Memoria, instrucciones y sesiones](#2-memoria-instrucciones-y-sesiones)
3. [MCP — conectar tus herramientas](#3-mcp)
4. [Plugins, tools y skills](#4-plugins-tools-y-skills)
5. [Automatización](#5-automatización)
6. [Metodología real: GSD + CodeGraph + agente disciplinado](#6-metodología-real)
7. [Cierre](#7-cierre)

---

## 0. Qué es Claude Code

**Hilo:** Claude Code es un agente de coding que **lee tu codebase, edita ficheros, ejecuta comandos** y
se integra con tus herramientas. No es un autocompletado: entiende el proyecto entero y trabaja a través
de varios ficheros y tools. Y **el mismo motor** corre en terminal, IDE (VS Code/JetBrains), app de
escritorio y navegador — tus `CLAUDE.md`, settings y servers MCP funcionan en todas las superficies.

**Qué puedes hacer con él (los titulares):**
- Automatizar lo tedioso: escribir tests, arreglar lint, resolver conflictos de merge, actualizar deps.
- Construir features y arreglar bugs describiendo en lenguaje natural.
- Crear commits y PRs; revisar código en CI.
- Conectar tus herramientas con MCP; correr en pipelines Unix; programar tareas recurrentes.

🗣️ *"No es un copiloto que sugiere líneas: es un colaborador que planifica, edita en varios ficheros y verifica."*

---

## 1. Instalación y uso básico

**Hilo:** Instalar es una línea. Lo importante es entender los **dos modos** de uso.

**Instalación (elige uno):**
```bash
curl -fsSL https://claude.ai/install.sh | bash     # macOS / Linux / WSL (recomendado, auto-update)
brew install --cask claude-code                     # Homebrew
winget install Anthropic.ClaudeCode                 # Windows
# también: apt / dnf / apk en Linux
```
Luego, en cualquier proyecto:
```bash
cd tu-proyecto
claude            # primera vez te pide login
```

**Los dos modos (la idea que hay que dejar clara):**
- **Interactivo** — abres `claude` y conversas. Aquí vive el **plan mode**: Claude propone un plan antes
  de tocar nada y tú lo apruebas.
- **Headless (`-p`)** — un solo prompt, entra por stdin, sale por stdout. Es lo que lo hace **componible**
  al estilo Unix y automatizable en CI:
  ```bash
  tail -200 app.log | claude -p "avísame si ves anomalías"
  git diff main --name-only | claude -p "revisa estos ficheros por seguridad"
  ```

**Superficies:** terminal, VS Code/Cursor, JetBrains, Desktop (diffs visuales, sesiones en paralelo),
Web (claude.ai/code, tareas largas sin setup local).

🗣️ *"Interactivo para pensar contigo; `-p` para meterlo en una tubería. El mismo Claude, dos formas de invocarlo."*

---

## 2. Memoria, instrucciones y sesiones

**Hilo:** El agente es tan bueno como el contexto que le das — y como lo **gestionas**. Tres piezas:
`CLAUDE.md`, settings, y sesiones que viajan entre dispositivos.

### `CLAUDE.md` — la memoria del proyecto
Un Markdown que Claude lee al inicio de **cada** sesión. Ahí pones estándares de código, decisiones de
arquitectura, comandos y checklists. Se combina por **jerarquía**: global del usuario
(`~/.claude/CLAUDE.md`) → raíz del repo → subcarpetas → `CLAUDE.local.md` personal.

**El error clásico y cómo lo resuelvo — patrón de dos niveles:**
- **Nivel 1 (siempre cargado):** pequeño. Solo orientación + **punteros de una línea**.
- **Nivel 2 (bajo demanda):** el detalle en ficheros que el agente lee solo cuando hace falta.
- Regla *write-once*: cada dato se escribe en un único sitio; el `CLAUDE.md` lleva el puntero, no la copia.
- Resultado real: recortamos el nuestro **~73% sin perder información**. (Ejemplo sanitizado en
  [`ejemplos/claude-md/`](./ejemplos/claude-md/).)

**Auto-memory:** además, Claude guarda solo aprendizajes (comandos de build, pistas de debug) entre
sesiones sin que escribas nada.

### Settings — permisos
`settings.json` controla qué puede hacer el agente con un **allowlist** (`allow`/`deny`/`ask`). Un setup
profesional no usa comodines: usa reglas específicas (p. ej. la invocación exacta de pytest, operaciones
git acotadas, tools `mcp__*` concretas). Es la postura "el humano es dueño de las acciones externas".

### Sesiones que viajan
Las sesiones no están atadas a una superficie: empieza en la web/móvil y tráela al terminal con
`claude --teleport`; sigue desde el móvil con **Remote Control**; pasa una sesión del terminal al
**Desktop** con `/desktop` para revisar diffs.

🗣️ *"El `CLAUDE.md` que se carga siempre debe ser una onboarding de 30 segundos, no un vertedero. Punteros, no copias."*

---

## 3. MCP

**Hilo:** **MCP (Model Context Protocol)** es el estándar abierto para enchufar Claude a datos y
herramientas externas: Drive, Jira, Slack, tu base de datos, un navegador, tu tooling propio. Cada server
expone *tools* que aparecen como `mcp__<server>__<tool>`.

**Los tres scopes (dónde vive la config):**
- **local** → `.claude/settings.local.json` (solo tú, esta máquina).
- **project** → `.mcp.json` en la raíz, **versionado**, compartido con el equipo.
- **user** → `~/.claude.json` (todos tus proyectos).

**Añadir uno:**
```bash
claude mcp add --transport http context7 https://mcp.context7.com/mcp
claude mcp list        # estado
/mcp                   # dentro de la sesión: auth OAuth, tools
```

**Los que uso a diario:** `serena` (navegación semántica de código), `context7` (docs de librerías al
día), `playwright` (verificar la UI en un navegador real), `codegraph` (grafo del código), `supabase`.

**Buenas prácticas:** secretos por variable de entorno (nunca en el JSON versionado); el server disponible
≠ tool permitida (sigues controlando con el allowlist). Config de ejemplo en [`ejemplos/mcp/`](./ejemplos/mcp/).

🗣️ *"MCP convierte a Claude de 'sabe de código' a 'sabe de TU sistema': tus docs, tus tickets, tu navegador."*

---

## 4. Plugins, tools y skills

**Hilo:** Cuatro capas de extensibilidad, de simple a potente.

1. **Tools** — lo que Claude puede *hacer*: `Read/Edit/Write/Bash/Grep/Glob/WebFetch/Task` + las `mcp__*`.
   El acceso se gobierna con el allowlist de permisos.
2. **Slash commands** — un `.md` en `.claude/commands/` = un `/comando`. El cuerpo es el prompt.
   Ejemplo: [`/audit`](./ejemplos/skills-plugins/.claude/commands/audit.md) (npm audit → fix → tests).
3. **Skills** — empaquetan un flujo repetible en `.claude/skills/<n>/SKILL.md` con `description`; Claude
   la **auto-selecciona** por esa descripción. Ejemplo: `deploy-staging`. Frente al slash command (lo
   invocas tú), la skill puede llevar scripts/plantillas y se dispara sola.
4. **Plugins + marketplaces** — agrupan skills + comandos + agentes + MCP + hooks como una unidad
   instalable: `/plugin marketplace add <owner/repo>` → `/plugin install <x>`. Así se distribuye un setup
   entero (GSD instala decenas de skills de golpe).

**Subagentes:** con `Task` lanzas agentes con su propio contexto (`Explore`, `Plan`, `general-purpose`,
o especializados) para paralelizar sin ensuciar tu sesión.

🗣️ *"Slash command = atajo que invocas tú. Skill = capacidad que Claude decide usar. Plugin = las dos, distribuibles."*

---

## 5. Automatización

**Hilo:** Cuatro niveles, del control determinista a la autonomía total. (Aquí es donde el curso de hooks
brilla — todo en [`ejemplos/hooks/`](./ejemplos/hooks/) y [`ejemplos/automation/`](./ejemplos/automation/).)

### a) Hooks — el control determinista
Un hook es un comando de shell que se dispara **antes/después** de una acción del agente. No le *pides*
que formatee: lo **fuerzas**. Contrato:
- Payload por **stdin**; eventos `PreToolUse`/`PostToolUse`/`SessionStart`/`Stop`/…
- **Matcher = regex sobre el nombre de la tool** (`Write|Edit|MultiEdit`, `Read|Grep`, `*`).
- **`exit 0` permite · `exit 2` BLOQUEA** y devuelve stderr a Claude como feedback.
- Pre te da la *intención* (`tool_input`, puedes vetar); Post te da el *resultado* (`tool_response`).

Cinco hooks de ejemplo, todos reales:
- **Seguridad:** bloquear lectura de `.env` (exit 2).
- **Observabilidad:** volcar cada payload a un JSON.
- **Calidad (no bloqueante):** `prettier --write` tras cada edición.
- **Calidad (bloqueante):** type-check; si no compila, corta y Claude lo arregla en el turno.
- **Meta ("IA revisando IA"):** un hook que llama al Agent SDK para detectar código duplicado y vetarlo.

### b) Headless / piping — `claude -p` en cualquier tubería (ver sección 1).

### c) CI/CD — GitHub Actions / GitLab / GitHub Code Review. Revisión de PRs e issues automáticas.
   Ejemplo de workflow en [`ejemplos/automation/github-action-claude.yml`](./ejemplos/automation/github-action-claude.yml).

### d) Tareas programadas:
- **Routines** (`/schedule`) — corren en infra de Anthropic aunque apagues el equipo; disparables por
  API o eventos de GitHub.
- **Desktop scheduled tasks** — en tu máquina, con acceso local.
- **`/loop`** — polling rápido dentro de una sesión.

### e) Agent SDK — para workflows a medida: `query({ prompt, options: { allowedTools } })`.

🗣️ *"Con instrucciones le pides que se porte bien; con un hook lo garantizas. `exit 2` es el 'no' que Claude no puede ignorar."*

---

## 6. Metodología real

**Hilo:** Herramientas sin método = caos rápido. Así es como lo uso en el día a día.

### El principio
> **El agente es un colaborador disciplinado, no un autopilot. La autonomía se gana por-decisión, no se
> concede en bloque.** El agente posee investigación, planes, implementación, tests y documentación;
> el humano posee las decisiones go/no-go, el scope y **toda acción externa** (push, PR, deploy).

### Los gates que no se saltan
- **"Sin prueba local no está hecho."** Nunca digas "arreglado/pasa" sin enseñar el output del comando.
- **Oráculo determinista gratis antes de la tirada de pago:** diagnostica con un validador/parser
  (determinista) y gástate la llamada al modelo solo para verificar el fix acabado.
- **Solución genérica con "prueba no-op":** arregla la *clase* del problema y demuestra salida
  byte-idéntica sobre el set de referencia conocido.
- **Gate de sanitización** (mecánico, siempre): revisa las líneas *añadidas* por nombres de cliente,
  IDs de ticket y secretos. Sin auto-atribución del agente en lo entregado.
- **"'Variación del LLM' es la conclusión de último recurso"**, tras descartar configuración y lógica.

### El tooling que lo encarna
- **GSD** ([`ejemplos/gsd/`](./ejemplos/gsd/)) — ciclo por fases *discutir → planificar → ejecutar →
  verificar* con estado en `.planning/` y subagentes especializados. Es el método hecho tooling.
- **CodeGraph** ([`ejemplos/codegraph/`](./ejemplos/codegraph/)) — grafo del código: en vez de
  grep→abrir→seguir-import, una consulta devuelve fuente + rutas de llamada + blast radius.
- **Serena + Playwright + AWS CLI** — navegación semántica, verificación de UI, diagnóstico determinista.

🗣️ *"El modelo no gana confianza gratis: la gana decisión a decisión, con evidencia. Ese es el trabajo."*

---

## 7. Cierre

- Instalar es trivial; el valor está en **cómo** lo usas: contexto lean, permisos guardados, método.
- Las 5 capas: **instalar → memoria/sesiones → MCP → skills/plugins → automatización.**
- El salto de nivel: de "chatear con un asistente" a **un sistema** con hooks que garantizan calidad,
  MCP que conecta tu mundo, y una metodología que trata al agente como colaborador con gates de evidencia.

**Referencias:** documentación oficial <https://code.claude.com/docs> · GSD
<https://github.com/tomascortereal/claude-code-setup> · CodeGraph <https://colbymchenry.github.io/codegraph/>.
