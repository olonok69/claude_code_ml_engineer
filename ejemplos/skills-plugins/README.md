# Plugins, tools y skills

Los tres mecanismos de extensibilidad de Claude Code, de más simple a más potente.

## 1. Tools (herramientas)

Lo que Claude puede *hacer*: `Read`, `Edit`, `Write`, `Bash`, `Grep`, `Glob`, `WebFetch`, `Task`
(subagentes), más las tools `mcp__*` que añaden los servidores MCP. Controlas el acceso con el
**allowlist de permisos** en `settings.json` (`allow` / `deny` / `ask`).

## 2. Slash commands (comandos custom)

Un fichero Markdown en `.claude/commands/<nombre>.md` = un comando `/<nombre>`. El cuerpo es el prompt
que se ejecuta. Ideal para tareas repetibles cortas. Ver [`audit.md`](./.claude/commands/audit.md) → `/audit`.

## 3. Skills

Una **skill** empaqueta un flujo de trabajo repetible con instrucciones más ricas. Vive en
`.claude/skills/<nombre>/SKILL.md` con frontmatter (`name`, `description`). La `description` es lo que
Claude usa para **decidir cuándo invocarla** automáticamente. Ver
[`deploy-staging/SKILL.md`](./.claude/skills/deploy-staging/SKILL.md).

Diferencia clave frente a un slash command: la skill puede llevar ficheros de apoyo (scripts, plantillas,
referencias) en su carpeta y Claude la **auto-selecciona** por su `description`; el slash command lo
invocas tú explícitamente con `/`.

### Cuándo una skill gana a un documento: `day`

[`day/SKILL.md`](./.claude/skills/day/SKILL.md) es el segundo ejemplo, y está aquí por lo que
demuestra más que por lo que hace. Empaqueta los dos momentos de los que depende un registro
compartido — **preparar la máquina al empezar** (`day start`) y **publicar el trabajo al terminar**
(`day end`) — y es *consciente del rol*: lee la tarjeta de identidad de la máquina antes de tocar
nada, porque un `contributor` y el `publisher` no hacen lo mismo.

⚠️⚠️ **La razón de que sea una skill y no un párrafo en un runbook.** La regla "haz `pull` al empezar
y `push` al terminar" estuvo escrita en el manual de operaciones **durante meses y no se cumplía** en
la máquina que publicaba. Nada registraba una sincronización, así que nada podía enseñar la deriva:
el incumplimiento era invisible incluso para quien lo incumplía. **La documentación no puede forzar
un hábito; una rutina invocable sí** — y de paso deja un rastro (`activity.sh`) que responde "¿cuándo
sincronizó esta máquina por última vez?" para todas las máquinas.

Léela por el patrón, no por los comandos: gatea el trabajo peligroso detrás de comprobaciones
(¿hay trabajo local sin publicar?, ¿hay ficheros que el `pull` va a sobrescribir?, ¿tiene esta máquina
permiso para publicar el artefacto derivado?), y **se detiene y pregunta** en vez de elegir por ti.
Una skill que decide sola en el caso ambiguo es la que acaba destruyendo trabajo ajeno.

### Las otras skills reales de este proyecto

Todas sanitizadas (sin nombres de cliente, IDs de ticket ni identificadores de cuenta):

| Skill | Para qué | Lo que enseña |
|---|---|---|
| [`kg`](./.claude/skills/kg/SKILL.md) | Consulta determinista del grafo de tickets **antes** de grepear el registro | Una skill puede ser *barata y sin LLM*: lee un artefacto ya construido y apunta a qué leer. |
| [`kg-refresh`](./.claude/skills/kg-refresh/SKILL.md) | Reconstruir el grafo cuando el corpus se mueve — **solo publisher** | ⚠️ Lleva la convención de IDs de nodo: sin fijarla, solo **12,6%** de los ids y **6,3%** de las etiquetas sobrevivían a un refresco, y con ellas se perdían todos los nombres de comunidad escritos a mano. |
| [`sanitise-diff`](./.claude/skills/sanitise-diff/SKILL.md) | Puerta mecánica antes de commit/PR: nombres de cliente, IDs de ticket, secretos, auto-atribución del agente | ⚠️ Lee su nota final: **el fichero cuya misión es cazar nombres de cliente es el único que los contiene todos**. La lista va fuera, gitignored. |
| [`methodology-plan`](./.claude/skills/methodology-plan/SKILL.md) | Rellenar la plantilla de planificación tras el triaje y la investigación barata | Una skill como *gate de proceso*: no escribe código, obliga a que exista un plan antes. |

Los scripts que la skill `day` orquesta están en
[`../metodologia/s3-sync/`](../metodologia/s3-sync/) — reales y ejecutables.

⚠️ **Lo que NO está aquí, a propósito:** las decenas de skills `gsd-*`. Son un plugin de terceros
instalado desde un marketplace, no código nuestro; vendorizarlas en un curso las congela en una
versión y las desconecta de sus actualizaciones. Instálalas, no las copies.

## 4. Plugins y marketplaces

Un **plugin** agrupa y distribuye skills + comandos + agentes + servidores MCP + hooks como una unidad
instalable desde un *marketplace*.

```bash
/plugin marketplace add <owner/repo>   # añadir un marketplace
/plugin install <plugin>               # instalar
/plugin                                 # gestionar los instalados
```

Así se distribuyen setups completos: p. ej. GSD (ver `../gsd/`) instala decenas de skills `gsd-*`,
agentes y comandos de una vez.

## 5. Subagents (agent types)

Con la tool `Task` lanzas **subagentes** con su propio contexto y presupuesto: `Explore` (búsqueda
read-only), `Plan` (arquitectura), `general-purpose`, o agentes especializados de un plugin. Sirven para
paralelizar trabajo independiente sin ensuciar tu contexto principal.
