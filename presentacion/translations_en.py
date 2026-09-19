"""ES -> EN deck strings, keyed by the full Spanish line.

Harvested from the Spanish and English decks as they stood on 2026-07-21. Both were
generated from the same layout code and align 1:1 (39 slides, 697 paragraphs, zero
run-count mismatches, zero collisions), which is what makes a positional harvest safe.

KEY   = the Spanish line, i.e. "".join(run texts) as build_pptx.py emits it.
VALUE = the English runs, in order. When the count matches the emitted runs the
        formatting (bold, colour) is preserved run for run; when it does not,
        build_pptx.py falls back to putting the whole line in the first run and
        reports it, because the decks were re-saved by PowerPoint, which merges
        adjacent runs that share formatting.

Entries where ES == EN are kept deliberately: dropping them made 117 already-English
terms ("Hooks", "Skills", "CI/CD") show up as missing translations and buried the
handful that genuinely were.

Lines absent here pass through in Spanish; `--lang en` prints them at the end.
"""

TRANSLATIONS = {
    '                        # -> scratch FUERA del repo':
        ('                        # -> scratch OUTSIDE the repo',),
    '                        # nodos+aristas+clustering':
        ('                        # nodes+edges+clustering',),
    '                     commits atómicos':
        ('                     atomic commits',),
    '                     gsd-plan-checker)':
        ('                     gsd-plan-checker)',),
    '     ?.file_path?.includes(".env")) {':
        ('     ?.file_path?.includes(".env")) {',),
    '    {"type": "ephemeral"} }]   # breakpoint':
        ('    {"type": "ephemeral"} }]   # breakpoint',),
    '  "cache_control":':
        ('  "cache_control":',),
    '  "content": query }]  # variable: FUERA':
        ('  "content": query }]  # variable: OUTSIDE',),
    '  "teammateMode": "in-process" }  // tmux|iterm2':
        ('  "teammateMode": "in-process" }  // tmux|iterm2',),
    '  "text": STABLE_INSTRUCTIONS,   # estable':
        ('  "text": STABLE_INSTRUCTIONS,   # stable',),
    '  --from git+https://github.com/oraios/serena \\':
        ('  --from git+https://github.com/oraios/serena \\',),
    '  console.error("Bloqueado: no leas .env");':
        ('  console.error("Blocked: don\'t read .env");',),
    '  if (m.type === "result") console.log(m.result);':
        ('  if (', 'm.type', ' === "result") console.log(', 'm.result', ');'),
    '  process.exit(2);   // <-- veto':
        ('  process.exit(2);   // <-- veto',),
    '  serena start-mcp-server':
        ('  serena start-mcp-server',),
    '  tras cambios en auth o deps.':
        ('  after changes to auth or deps.',),
    '# .claude/agents/security-reviewer.md':
        ('# .claude/agents/security-reviewer.md',),
    '# breakpoint -> 0 hits y nadie sabe por qué':
        ('# breakpoint -> 0 hits and nobody knows why',),
    '# error clásico: timestamp ANTES del':
        ('# classic mistake: timestamp BEFORE the',),
    '(según sus benchmarks: casi elimina las lecturas de fichero)':
        ('(per its benchmarks: nearly eliminates file reads)',),
    '---':
        ('---',),
    '.claude/commands/x.md = /x. El cuerpo es el prompt. Lo invocas tú.':
        ('.claude/commands/x.md = /x. The body is the prompt. You invoke it.',),
    '.claude/settings.local.json — solo tú, esta máquina.':
        ('.claude/settings.local.json — only you, this machine.',),
    '.claude/skills/x/SKILL.md con description. Claude la auto-selecciona; lleva scripts/plantillas.':
        ('.claude/skills/x/SKILL.md with description. Claude auto-selects it; carries scripts/templates.',),
    '.mcp.json en la raíz, versionado, compartido con el equipo.':
        ('.mcp.json at the root, versioned, shared with the team.',),
    '// ~/.claude/settings.json':
        ('// ~/.claude/settings.json',),
    '/clear     # reset entre tareas':
        ('/clear     # reset between tasks',),
    '/compact céntrate en la API':
        ('/compact focus on the API',),
    '/compact o auto-compact':
        ('/compact or auto-compact',),
    '/context   # desglose de uso':
        ('/context   # usage breakdown',),
    '/desktop pasa la sesión al Desktop para revisar diffs.':
        ('/desktop hands the session to Desktop to review diffs.',),
    '/graphify <scratch>     # ÚNICO paso con LLM:':
        ('/graphify <scratch>     # ONLY step with LLM:',),
    '/gsd-execute-phase-> olas paralelas,':
        ('/gsd-execute-phase-> parallel waves,',),
    '/gsd-new-project  -> PROJECT.md + ROADMAP.md':
        ('/gsd-new-project  -> PROJECT.md + ROADMAP.md',),
    '/gsd-plan-phase   -> PLAN.md  (+ gate':
        ('/gsd-plan-phase   -> PLAN.md  (+ gate',),
    '/gsd-progress     # qué toca ahora':
        ("/gsd-progress     # what's next",),
    '/gsd-verify-work  -> VERIFICATION.md':
        ('/gsd-verify-work  -> VERIFICATION.md',),
    '/kg':
        ('/kg',),
    '/kg (grafo de tickets → zona de peligro) · STATUS.md · git · gh':
        ('/kg (ticket graph → danger zone) · STATUS.md · git · gh',),
    '/kg <A> <B>        # camino    (path)':
        ('/kg <A> <B>        # path      (path)',),
    '/kg <ticket|tema>  # vecinos   (explain)':
        ('/kg <ticket|topic> # neighbors (explain)',),
    '/kg find <substr>  # nombre exacto de nodo':
        ('/kg find <substr>  # exact node name',),
    '/kg saca la zona de peligro (un SHARP_EDGE que restringe el fix); git/gh dan la base.':
        ('/kg surfaces the danger zone (a SHARP_EDGE constraining the fix); git/gh give the baseline.',),
    '/kg-refresh        # reconstruir (barato)':
        ('/kg-refresh        # rebuild (cheap)',),
    '/rewind    # checkpoints (Esc+Esc)':
        ('/rewind    # checkpoints (Esc+Esc)',),
    '01  Instalación y uso básico':
        ('01  Install and basic use',),
    '01 · Instalación y uso básico':
        ('01 · Install and basic use',),
    '02  Memoria, instrucciones y sesiones':
        ('02  Memory, instructions and sessions',),
    '02 · Memoria y sesiones':
        ('02 · Memory and sessions',),
    '03  Contexto: context window y prompt caching':
        ('03  Context: context window and prompt caching',),
    '03 · Contexto y prompt caching':
        ('03 · Context and prompt caching',),
    '04  MCP — conectar tus herramientas':
        ('04  MCP — connect your tools',),
    '04 · MCP':
        ('04 · MCP',),
    '05  Plugins, tools y skills':
        ('05  Plugins, tools and skills',),
    '05 · Plugins, tools y skills':
        ('05 · Plugins, tools and skills',),
    '06  Subagents y Agent Teams':
        ('06  Subagents and Agent Teams',),
    '06 · Subagents y Agent Teams':
        ('06 · Subagents and Agent Teams',),
    '07  Automatización':
        ('07  Automation',),
    '07 · Automatización':
        ('07 · Automation',),
    '08  El flujo de 11 etapas + ejemplo real':
        ('08  The 11-stage workflow + real example',),
    '08 · El flujo de 11 etapas + ejemplo real':
        ('08 · The 11-stage workflow + real example',),
    '09  Las herramientas del método':
        ("09  The method's tools",),
    '09 · Las herramientas del método':
        ("09 · The method's tools",),
    '1':
        ('1',),
    '1 llamada':
        ('1 call',),
    '10':
        ('10',),
    '10  Transferir la metodología (Copilot)':
        ('10  Transfer the methodology (Copilot)',),
    '10 · Transferir a otro agente (Copilot)':
        ('10 · Transfer to another agent (Copilot)',),
    '11':
        ('11',),
    '11  Sincronización de máquinas':
        ('11  Machine sync',),
    '11 · Sincronización de máquinas':
        ('11 · Machine sync',),
    '12':
        ('12',),
    '12  Diseño · pipeline · comandos /kg · el grafo real':
        ('12  Design · pipeline · /kg commands · the real graph',),
    '12a · El problema y el diseño (spike)':
        ('12a · The problem and the design (spike)',),
    '12b · Pipeline y comandos (/kg, /kg-refresh)':
        ('12b · Pipeline and commands (/kg, /kg-refresh)',),
    '12c · El grafo real, visualizado':
        ('12c · The real graph, visualized',),
    '12d · Uso y enganche en la metodología':
        ('12d · Usage and hook into the methodology',),
    '13':
        ('13',),
    '13  Cierre':
        ('13  Closing',),
    '14':
        ('14',),
    '15':
        ('15',),
    '16':
        ('16',),
    '17':
        ('17',),
    '18':
        ('18',),
    '19':
        ('19',),
    '2':
        ('2',),
    '20':
        ('20',),
    '21':
        ('21',),
    '22':
        ('22',),
    '23':
        ('23',),
    '24':
        ('24',),
    '25':
        ('25',),
    '26':
        ('26',),
    '27':
        ('27',),
    '28':
        ('28',),
    '29':
        ('29',),
    '3':
        ('3',),
    '30':
        ('30',),
    '31':
        ('31',),
    '32':
        ('32',),
    '33':
        ('33',),
    '34':
        ('34',),
    '35':
        ('35',),
    '36':
        ('36',),
    '4':
        ('4',),
    '5':
        ('5',),
    '507 nodos · 35 comunidades: history-first sin LLM.':
        ('507 nodes · 35 communities: history-first, no LLM.',),
    '58% menos tool calls · 22% más rápido':
        ('58% fewer tool calls · 22% faster',),
    '6':
        ('6',),
    '7':
        ('7',),
    '8':
        ('8',),
    '9':
        ('9',),
    '<repo>/CLAUDE.local.md   # personal, no versionado':
        ('<repo>/CLAUDE.local.md   # personal, not versioned',),
    '<repo>/CLAUDE.md         # compartido (versionado)':
        ('<repo>/CLAUDE.md         # shared (versioned)',),
    '<repo>/sub/CLAUDE.md     # al entrar en la subcarpeta':
        ('<repo>/sub/CLAUDE.md     # on entering the subfolder',),
    '@imports y CLAUDE.md de subcarpeta solo cargan cuando tocan. El detalle vive fuera.':
        ('@imports and subfolder CLAUDE.md load only when needed. Detail lives outside.',),
    'AGENDA':
        ('AGENDA',),
    'AGENT TEAM':
        ('AGENT TEAM',),
    'AWS CLI — CloudWatch · lambda get-function · SQS/DLQ':
        ('AWS CLI — CloudWatch · lambda get-function · SQS/DLQ',),
    'Activar (off por defecto)':
        ('Enable (off by default)',),
    'Agent SDK — workflows a medida (menor privilegio)':
        ('Agent SDK — custom ', 'workflows', ' (', 'least', ' privilege)'),
    'Agent Teams: varios Claudes que se coordinan':
        ('Agent Teams: several Claudes coordinating',),
    'Agentic AiClaude Code: from assistant to agentic developing system':
        ('Agentic Ai', 'Claude Code: from assistant to agentic developing system'),
    'Agnóstica de la herramienta: se demuestra con Claude Code, pero la disciplina viaja.':
        ('Tool-agnostic: demonstrated with Claude Code, but the discipline travels.',),
    'Agnóstica:  no es un flujo de Claude Code — es una forma de trabajar con CUALQUIER agente. La sección 10 lo demuestra transfiriéndola a GitHub Copilot.':
        ('Agnostic:  ', 'not a Claude Code workflow — a way of working with ANY agent. Section 10 proves it by transferring it to GitHub Copilot.'),
    'Agrupan skills+comandos+agentes+MCP+hooks. /plugin install. GSD es uno.':
        ('Bundle skills+commands+agents+MCP+hooks. /plugin install. GSD is one.',),
    'Aislado; devuelve un resumen':
        ('Isolated; returns a summary',),
    'Alto (N sesiones en paralelo)':
        ('High (N sessions in parallel)',),
    'Arrancar en cualquier proyecto':
        ('Start', ' ', 'in', ' ', 'any', ' ', 'project'),
    'Auto-memory':
        ('Auto-memory',),
    'Auto-memory + entorno':
        ('Auto-memory + environment',),
    'Añadir un server (secretos por env var; cada server suma contexto — sección 03)':
        ('Add a server (secrets via env var; each server adds context — section 03)',),
    'Bajo (lo caro muere fuera)':
        ('Low (costly work dies outside)',),
    'Basado en la documentación oficial (code.claude.com), el curso de hooks de Anthropic, GSD, CodeGraph y una instalación real en producción.':
        ("Based on the official docs (code.claude.com), Anthropic's hooks course, GSD, CodeGraph and a real production install.",),
    'Bloque de tools grande y cambiante → escrituras caras':
        ('Large, changing tools block → expensive writes',),
    'Bug QA: “un campo sale vacío en la UI, pero está escrito en el PDF.”':
        ('QA bug: ', "“a field shows empty in the UI, but it's written in the PDF.”"),
    'Build (skill /kg-refresh)':
        ('Build (skill /kg-refresh)',),
    'Built-ins (tool Task)':
        ('Built-ins (Task tool)',),
    'CG':
        ('CG',),
    'CI/CD':
        ('CI/CD',),
    'CIERRE':
        ('CLOSING',),
    'CLAUDE.md mínimo':
        ('Minimal CLAUDE.md',),
    'CLAUDE.md pequeño y estable':
        ('Small, stable CLAUDE.md',),
    'CLAUDE.md: el patrón de dos niveles':
        ('CLAUDE.md: the two-tier pattern',),
    'CLI  (install --location=global escribe el MCP)':
        ('CLI  (install --location=global writes the MCP)',),
    'CURSO / WORKSHOP · DEVELOPER TOOLING':
        ('COURSE / WORKSHOP · DEVELOPER TOOLING',),
    'Caching en Claude Code: tú decides el hit-rate':
        ('Caching in Claude Code: you decide the hit-rate',),
    'Cada herramienta, en una frase — y su fase':
        ('Each tool in one sentence — and its phase',),
    'Cada server suma su bloque de tools. Desactiva los que el proyecto no use.':
        ("Each server adds its tools block. Disable the ones the project doesn't use.",),
    'Cada teammate = sesión completa':
        ('Each teammate = full session',),
    'Cada turno reenvía TODO el contexto. La API cachea el prefijo estable — orden estricto Tools → System → Messages: un cambio invalida su nivel y los siguientes.':
        ('Every turn resends ALL context. The API caches the stable prefix — strict order ', 'Tools → System → Messages', ': a change invalidates its level and all after.'),
    'Cambia el prefijo → invalida el cache desde ahí':
        ('Change the prefix → invalidates cache from there',),
    'Carga bajo demanda':
        ('Loads on demand',),
    'Channels / Slack':
        ('Channels / Slack',),
    'Ciclo por fases, estado versionado en .planning/':
        ('Phase-based cycle, state versioned in .planning/',),
    'Claude Code':
        ('Claude Code',),
    'Claude Code lo aplica solo (system + tools + historial = prefijo). TTL por defecto: 1 h con suscripción · 5 min con API key. Cambiar/apagar por env var: ENABLE_PROMPT_CACHING_1H · FORCE_PROMPT_CACHING_5M · DISABLE_PROMPT_CACHING. Cada lectura renueva la ventana: con suscripción, una pausa de hasta 1 h sigue en cache.':
        ('Claude Code ', 'applies it', ' alone (system + tools + ', 'history', ' = ', 'prefix', '). ', 'TTL ', 'by', ' ', 'default', ': 1 h with ', 'subscription', ' · 5 min with API key. ', 'Change/', 'disable', ' ', 'by', ' env var: ', 'ENABLE_PROMPT_CACHING_1H · FORCE_PROMPT_CACHING_5M · DISABLE_PROMPT_CACHING', '. Each ', 'each read', ' ', 'renews', ' the ', 'window', ': with ', 'subscription', ', ', 'one', ' pause of up to 1 h ', 'continues', ' ', 'in', ' cache', '.'),
    'Claude Code · Curso / Workshop':
        ('Claude Code · Course / Workshop',),
    'CodeGraph codegraph_explore — fuente + rutas + blast radius + cobertura':
        ('CodeGraph codegraph_explore — source + paths + blast radius + coverage',),
    'CodeGraph · Serena · oráculos: barato→caro; GSD = el método productizado.':
        ('CodeGraph · Serena · oracles: cheap→expensive; GSD = the method productized.',),
    'CodeGraph → investigar':
        ('CodeGraph → investigate',),
    'CodeGraph: inteligencia de código local':
        ('CodeGraph: local code intelligence',),
    'Codigo determinista: parser / validador / _diag_*.py':
        ('Code', ' ', 'deterministic', ': parser / ', 'validator', ' / _diag_*.py'),
    'Comunicación':
        ('Communication',),
    'Conecta tu mundo; empaqueta y distribuye flujos.':
        ('Connect your world; package and distribute workflows.',),
    'Config':
        ('Config',),
    'Consulta: CERO LLM (kg_query.sh lee graph.json)':
        ('Query: ZERO LLM (kg_query.sh reads graph.json)',),
    'Context window: el recurso que gobierna todo':
        ('Context window: the resource that governs everything',),
    'Contexto':
        ('Context',),
    'Contexto & caching':
        ('Context & caching',),
    'Contrato':
        ('Contract',),
    'Contrato de salida':
        ('Output contract',),
    'Conversación + tool results':
        ('Conversation + tool results',),
    'Coste':
        ('Cost',),
    'Cuatro capas de extensibilidad':
        ('Four layers of extensibility',),
    'Custom: un .md con frontmatter (/agents los lista)':
        ('Custom: a .md with frontmatter (/agents lists them)',),
    'Cómo se usa — y dónde se engancha':
        ("How it's used — and where it hooks in",),
    'De asistente a sistema':
        ('From assistant to system',),
    'De hooks a agentes programados':
        ('From hooks to scheduled agents',),
    'Desktop handoff':
        ('Desktop handoff',),
    'Diagnosticar':
        ('Diagnose',),
    'Documentar — cada cosa una vez':
        ('Document — each thing once',),
    'Dos modos: interactivo y headless':
        ('Two modes: interactive and headless',),
    'Dónde se engancha':
        ('Where it hooks in',),
    'Editar CLAUDE.md/settings a mitad de sesión':
        ('Editing CLAUDE.md/settings mid-session',),
    'Ejemplo real: /kg get_letter_end → la zona de peligro completa al instante: los 5-6 tickets que comparten ese código.':
        ('Real example: /kg get_letter_end ', '→ the full danger zone instantly: the 5-6 tickets sharing that code.'),
    'El agente es un colaborador disciplinado':
        ('The agent is a disciplined collaborator',),
    'El agente posee':
        ('The agent owns',),
    'El campo está vacío en el JSON del endpoint (Playwright/F12) → el Lambda es responsable.':
        ('The field is empty in the endpoint JSON (Playwright/F12) → the Lambda is responsible.',),
    'El contrato de un hook':
        ("A hook's contract",),
    'El corpus: manifest, no glob':
        ('The corpus: manifest, not glob',),
    'El flujo de 11 etapas':
        ('The 11-stage workflow',),
    'El flujo real de 11 etapas':
        ('The real 11-stage workflow',),
    'El gotcha que lo sostiene:  graphify respeta .gitignore y todo data/ lo está → correr el detector in situ encuentra 0 ficheros. Por eso el corpus se monta en un scratch fuera del repo y los artefactos se copian de vuelta.':
        ('The gotcha behind it:  ', 'graphify honors .gitignore and all of data/ is ignored → running the detector in place finds 0 files. Hence the corpus is staged in a scratch outside the repo and artifacts are copied back.'),
    'El grafo de tickets':
        ('The ticket graph',),
    'El grafo de tickets (graphify)':
        ('The ticket graph (graphify)',),
    'El grafo real: 507 nodos, 35 comunidades':
        ('The real graph: 507 nodes, 35 communities',),
    'El historial se relee a 0.1× — el caso ideal':
        ('History is re-read at 0.1× — the ideal case',),
    'El humano posee':
        ('The human owns',),
    'El landing lo conduce un agente — con guardrails':
        ('An agent drives the landing — with guardrails',),
    'El mismo Claude, dos formas de invocarlo':
        ('The same Claude, two ways to invoke it',),
    'El mismo motor en todas partes':
        ('The ', 'same', ' engine ', 'in', ' ', 'all', ' parts'),
    'El método productizado (subagentes gsd-* + .planning/). Para greenfield multi-fase; este proyecto usa data/changes/, no GSD.':
        ('The method productized (gsd-* subagents + .planning/). For multi-phase greenfield; this project uses data/changes/, not GSD.',),
    'El presupuesto y el descuento: lean y estable gana en ambos.':
        ('The budget and the discount: lean and stable wins both.',),
    'El problema':
        ('The problem',),
    'El problema, y por qué graphify':
        ('The problem, and why graphify',),
    'El starter-kit (docs/ai-agents-code-methodology/)':
        ('The starter-kit (docs/ai-agents-code-methodology/)',),
    'El subagente refactor-scout (ejemplos/subagents/) empaqueta el orden CodeGraph → Serena → grep como procedimiento.':
        ('The refactor-scout subagent ', '(ejemplos/subagents/) packages the CodeGraph → Serena → grep order as a procedure.'),
    'Empuja eventos externos o convierte un bug de Slack en un PR.':
        ('Push external events or turn a Slack bug into a PR.',),
    'Entorno (logs, config)':
        ('Environment (logs, config)',),
    'Env var experimental + settings':
        ('Experimental env var + settings',),
    'Eres un ingeniero de seguridad senior…':
        ('You are a senior security engineer…',),
    'Escala el trabajo; hooks que garantizan calidad.':
        ('Scale the work; hooks that guarantee quality.',),
    'Estándar abierto para enchufar Claude a datos y tools externas. Las tools aparecen como mcp__<server>__<tool>.':
        ('Open standard to plug Claude into external data and tools. Tools appear as ', 'mcp__<server>__<tool>', '.'),
    'Explore → Plan → Code':
        ('Explore → Plan → Code',),
    'Fix + verificar':
        ('Fix + verify',),
    'G':
        ('G',),
    'GSD → plan/ejecutar/verificar':
        ('GSD → plan/execute/verify',),
    'GSD: la metodología hecha tooling':
        ('GSD: the methodology productized',),
    'Gates deterministas; el humano posee las decisiones.':
        ('Deterministic gates; the human owns the decisions.',),
    'GitHub Actions · GitLab · GitHub Code Review sobre cada PR.':
        ('GitHub Actions · GitLab · GitHub Code Review on every PR.',),
    'Grafo de la MEMORIA del proyecto (con graphify): tickets + sharp edges. History-first sin LLM (Parte 3).':
        ("Graph of the project's MEMORY (with graphify): tickets + sharp edges. History-first, no LLM (Part 3).",),
    'Grafo de tickets → orientar':
        ('Ticket graph → orient',),
    'Grafo del CÓDIGO (tree-sitter→SQLite, local). Survey en 1 llamada: fuente + callers + blast radius + cobertura.':
        ('Graph of the CODE (tree-sitter→SQLite, local). Survey in 1 call: source + callers + blast radius + coverage.',),
    'Handoff':
        ('Handoff',),
    'Handoff: el humano hace push / PR':
        ('Handoff: the human does push / PR',),
    'Headless (-p) — componible':
        ('Headless (-p) — composable',),
    'Headless / piping':
        ('Headless / piping',),
    'Higiene de contexto: máxima señal por token':
        ('Context hygiene: maximum signal per token',),
    'Homebrew':
        ('Homebrew',),
    'Honestidad y ciclo de vida':
        ('Honesty and lifecycle',),
    'Hooks':
        ('Hooks',),
    'Hooks: el control determinista':
        ('Hooks: deterministic control',),
    'Implementar: TDD RED → GREEN, mínimo':
        ('Implement: TDD RED → GREEN, minimal',),
    'Inbound — solo delta':
        ('Inbound — delta only',),
    'Instalar (stdio)':
        ('Install (stdio)',),
    'Instalar + memoria':
        ('Install + memory',),
    'Instalar es una línea':
        ('Install is one line',),
    'Interactivo — pensar contigo':
        ('Interactive — thinking with you',),
    'Investigar':
        ('Investigate',),
    'Investigar: oráculo determinista barato':
        ('Investigate: cheap deterministic oracle',),
    'Jerarquía de CLAUDE.md (se combinan; @fichero importa)':
        ('CLAUDE.md hierarchy (they combine; @file imports)',),
    'Jerarquía, permisos y memoria automática':
        ('Hierarchy, permissions and automatic memory',),
    'L':
        ('L',),
    'La 5ª capa — subagentes y equipos de agentes — merece sección propia: es la siguiente.':
        ("The 5th layer — subagents and agent teams — deserves its own section: it's next.",),
    'La arquitectura (experimental)':
        ('The architecture (experimental)',),
    'La exploración sucia va a un subagente (sección 06); vuelve solo el resumen.':
        ('Dirty exploration goes to a subagent (section 06); only the summary returns.',),
    'La herramienta: del binario en tu terminal a equipos de agentes.':
        ('The tool: from the binary in your terminal to agent teams.',),
    'La metodología':
        ('The methodology',),
    'La prueba de que es agnóstica: llevarla a Copilot':
        ("Proof it's agnostic: taking it to Copilot",),
    'La salida real':
        ('The real output',),
    'La tecnología es graphify — CodeGraph es solo la analogía.  Mismo rol (grafo consultable antes de tocar nada), otro dominio (tickets, no código), otra herramienta. La Fase 1 fue un SPIKE con decisión keep/extend/replace: validar graphify off-the-shelf antes de invertir en extracción custom. Bastó — y se quedó.':
        ('The technology is graphify — CodeGraph is just the analogy.  ', 'Same role (queryable graph before touching anything), different domain (tickets, not code), different tool. Phase 1 was a SPIKE with a keep/extend/replace decision: validate off-the-shelf graphify before investing in custom extraction. It sufficed — and it stayed.'),
    'La tirada del LLM — para VERIFICAR el fix, no para diagnosticar':
        ('The LLM call — to VERIFY the fix, not to diagnose',),
    'Las piezas':
        ('The pieces',),
    'Las tools del método':
        ("The method's tools",),
    'Lecturas con puntería':
        ('Targeted reads',),
    'Linux pkg':
        ('Linux pkg',),
    'Lo estable primero; el breakpoint al final de lo estable':
        ('Stable first; the breakpoint at the end of the stable part',),
    'Lo que Claude puede hacer: Read/Edit/Bash/Grep/Task + mcp__*. Gobernadas por permisos.':
        ('What Claude can do: Read/Edit/Bash/Grep/Task + mcp__*. Governed by permissions.',),
    'Lo que hay que saber':
        ('What you need to know',),
    'Los mandos':
        ('The controls',),
    'Límites hoy':
        ('Limits today',),
    'MCP + skills + plugins':
        ('MCP + skills + plugins',),
    'MCP con moderación':
        ('MCP in moderation',),
    'Model Context Protocol: conecta tu mundo':
        ('Model Context Protocol: connect your world',),
    'Muchos servers MCP activos':
        ('Many active MCP servers',),
    'Mínimo cacheable ~1k tokens · máx. 4 breakpoints · diagnóstico en usage.cache_read_input_tokens.':
        ('Cacheable minimum ~1k tokens · max 4 breakpoints · diagnosis in usage.cache_read_input_tokens.',),
    'Nada, o .claude/agents/*.md':
        ('Nothing, or .claude/agents/*.md',),
    'Native (recomendado)':
        ('Native (recommended)',),
    'Navegación semántica vía LSP (MCP)':
        ('Semantic navigation via LSP (MCP)',),
    'Navegación semántica vía LSP. find_referencing_symbols desambigua por clase: el chequeo preciso antes de renombrar.':
        ('Semantic navigation via LSP. find_referencing_symbols disambiguates by class: the precise check before renaming.',),
    'Navegar (survey)':
        ('Navigate (survey)',),
    'Nivel 1 — siempre cargado (pequeño)':
        ('Tier 1 — always loaded (small)',),
    'Nivel 2 — bajo demanda (el detalle)':
        ('Tier 2 — on demand (the detail)',),
    'Or':
        ('Or',),
    'Orientar':
        ('Orient',),
    'Orientar: /kg + history-first + status-first':
        ('Orient: /kg + history-first + status-first',),
    'Oráculos → diagnosticar':
        ('Oracles → diagnose',),
    'Outbound — copia completa':
        ('Outbound — full copy',),
    'P':
        ('P',),
    'PARTE 1':
        ('PART 1',),
    'PARTE 1 · 01 · INSTALACIÓN Y USO BÁSICO':
        ('PART 1 · 01 · INSTALL AND BASIC USE',),
    'PARTE 1 · 02 · INSTRUCCIONES, PERMISOS Y AUTO-MEMORY':
        ('PART 1 · 02 · INSTRUCTIONS, PERMISSIONS AND AUTO-MEMORY',),
    'PARTE 1 · 02 · MEMORIA E INSTRUCCIONES':
        ('PART 1 · 02 · MEMORY AND INSTRUCTIONS',),
    'PARTE 1 · 02 · SESIONES':
        ('PART 1 · 02 · SESSIONS',),
    'PARTE 1 · 03 · CONTEXTO':
        ('PART 1 · 03 · CONTEXT',),
    'PARTE 1 · 04 · MCP':
        ('PART 1 · 04 · MCP',),
    'PARTE 1 · 05 · PLUGINS, TOOLS Y SKILLS':
        ('PART 1 · 05 · PLUGINS, TOOLS AND SKILLS',),
    'PARTE 1 · 06 · SUBAGENTS Y AGENT TEAMS':
        ('PART 1 · 06 · SUBAGENTS AND AGENT TEAMS',),
    'PARTE 1 · 07 · AUTOMATIZACIÓN':
        ('PART 1 · 07 · AUTOMATION',),
    'PARTE 1 · Claude Code':
        ('PART 1 · Claude Code',),
    'PARTE 1 · la herramienta':
        ('PART 1 · the tool',),
    'PARTE 1 — Claude Code: instalación · memoria · contexto & caching · MCP · skills · subagents & teams · automatización':
        ('PART 1 — ', 'Claude Code: ', 'install', ' · memory · ', 'context', ' & caching · MCP · skills · subagents & teams · ', 'automation'),
    'PARTE 2':
        ('PART 2',),
    'PARTE 2 + 3 · el método y el grafo':
        ('PART 2 + 3 · the method and the graph',),
    'PARTE 2 · 08 · LA METODOLOGÍA':
        ('PART 2 · 08 · THE METHODOLOGY',),
    'PARTE 2 · 09 · HERRAMIENTAS DEL MÉTODO':
        ('PART 2 · 09 · METHOD TOOLS',),
    'PARTE 2 · 10 · TRANSFERENCIA':
        ('PART 2 · 10 · TRANSFER',),
    'PARTE 2 · 11 · OPS':
        ('PART 2 · 11 · OPS',),
    'PARTE 2 · La metodología (agnóstica)':
        ('PART 2 · The methodology (agnostic)',),
    'PARTE 2 — La metodología (agnóstica): flujo con gates · CodeGraph / Serena / Graphify / GSD · transferencia · ops':
        ('PART 2 — ', 'The ', 'methodology', ' (', 'agnostic', '): ', 'workflow', ' with gates · ', 'CodeGraph', ' / Serena /', ' ', 'Graphify', ' /', ' GSD · ', 'transfer', ' · ops'),
    'PARTE 3':
        ('PART 3',),
    'PARTE 3 · 12A · GRAFO DE TICKETS':
        ('PART 3 · 12A · TICKET GRAPH',),
    'PARTE 3 · 12B · GRAFO DE TICKETS':
        ('PART 3 · 12B · TICKET GRAPH',),
    'PARTE 3 · 12C · GRAFO DE TICKETS':
        ('PART 3 · 12C · TICKET GRAPH',),
    'PARTE 3 · 12D · GRAFO DE TICKETS':
        ('PART 3 · 12D · TICKET GRAPH',),
    'PARTE 3 · El grafo de tickets (graphify)':
        ('PART 3 · The ticket graph (graphify)',),
    'PARTE 3 — El grafo de conocimiento de tickets, construido con graphify: pipeline, comandos /kg y el grafo real':
        ('PART 3 — ', 'The ticket knowledge graph, built with graphify: pipeline, /kg commands and the real graph', '', '', '', '', '', '', '', '', '', '', '', ''),
    'Paralelismo real: revisión multi-capa':
        ('Real parallelism: multi-layer review',),
    'Parsers/validadores/_diag_*.py propios: respuesta barata y reproducible antes de gastar la tirada del LLM.':
        ('Your own parsers/validators/_diag_*.py: a cheap, reproducible answer before spending the LLM call.',),
    'Patrón de bloqueo (JS)':
        ('Blocking pattern (JS)',),
    'Permisos = allowlist específico':
        ('Permissions = specific allowlist',),
    'Pipeline y comandos creados en Claude Code':
        ('Pipeline and commands built in Claude Code',),
    'Plan → acuerdo humano explícito':
        ('Plan → explicit human agreement',),
    'Playwright / F12 sobre el endpoint que ve el consumidor':
        ('Playwright / F12 on the endpoint the consumer sees',),
    'Playwright → triaje y outbound':
        ('Playwright → triage and outbound',),
    'Plugins + marketplace':
        ('Plugins + marketplace',),
    'Por eso /kg-refresh es un skill, no un script:  el paso semántico (/graphify, subagentes en paralelo) es un paso de Claude; los bookends son deterministas.':
        ("That's why /kg-refresh is a skill, not a script:  ", 'the semantic step (/graphify, subagents in parallel) is a Claude step; the bookends are deterministic.'),
    'Por qué es OBLIGATORIO pre-rename:  el impact plano de CodeGraph mezcla métodos homónimos (Invoice.process vs Refund.process); Serena los desambigua por clase. Complementarios, no rivales.':
        ("Why it's MANDATORY pre-rename:  ", "CodeGraph's flat impact mixes same-name methods (Invoice.process vs Refund.process); Serena disambiguates them by class. Complementary, not rivals."),
    'Prefijo corto que nunca cambia → hits en cada turno':
        ('Short prefix that never changes → hits every turn',),
    'Primero para navegar:  fuente + callers + blast radius + cobertura en 1 consulta (trátala como YA leída). Serena find_referencing_symbols = chequeo preciso (desambigua por clase). --path fija el repo por defecto.':
        ('First for navigation:  ', 'source + callers + blast radius + coverage in 1 query (treat it as ALREADY read). Serena find_referencing_symbols = precise check (disambiguates by class). --path sets the default repo.'),
    'Prompt caching: no pagar lo mismo dos veces':
        ("Prompt caching: don't pay for the same thing twice",),
    'Provenance':
        ('Provenance',),
    'Puente a la Parte 2: GSD empaqueta exactamente esto — gsd-planner, gsd-executor, gsd-verifier son subagentes custom como plugin (este proyecto usa el flujo data/changes/, no GSD — ver Parte 2).':
        ('Bridge to Part 2: ', 'GSD packages exactly this — gsd-planner, gsd-executor, gsd-verifier are custom subagents as a plugin (this project uses the data/changes/ flow, not GSD — see Part 2).'),
    'Pw':
        ('Pw',),
    'Qué herramienta usa el agente, y cuándo':
        ('Which tool the agent uses, and when',),
    'Re-extraer en la base previa: ya salía vacío → pre-existente, no regresión.':
        ('Re-extract on the previous base: already empty → pre-existing, not a regression.',),
    'Reescribe el historial → rompe el cache de mensajes una vez, y sigue':
        ('Rewrites history → breaks the message cache once, then continues',),
    'Refactor-check':
        ('Refactor-check',),
    'Referencias:  code.claude.com/docs  ·  github.com/tomascortereal/claude-code-setup  ·  colbymchenry.github.io/codegraph  ·  github.com/oraios/serena':
        ('References:  code.claude.com/docs  ·  github.com/tomascortereal/claude-code-setup  ·  colbymchenry.github.io/codegraph  ·  github.com/oraios/serena',),
    'Regla del CLAUDE.md: codegraph_explore PRIMERO (survey en 1 llamada) · Serena find_referencing_symbols para el chequeo preciso antes de renombrar. Orden: barato → caro, determinista → probabilístico.':
        ('CLAUDE.md rule: ', 'codegraph_explore FIRST (survey in 1 call) · Serena find_referencing_symbols for the precise check before renaming. ', 'Order: cheap → expensive, deterministic → probabilistic.'),
    'Regla oficial: si puedes borrarlo sin que Claude se equivoque, bórralo. Dos niveles + punteros.':
        ('Official rule: if you can delete it without Claude going wrong, delete it. Two tiers + pointers.',),
    'Regresión vs. pre-existente (probarlo)':
        ('Regression vs. pre-existing (prove it)',),
    'Remote Control':
        ('Remote Control',),
    'Reproduce el síntoma donde lo ve el consumidor: el endpoint real, no una función interna.':
        ('Reproduce the symptom where the consumer sees it: the real endpoint, not an internal function.',),
    'Revisión bot + persistir lecciones':
        ('Bot review + persist lessons',),
    'Routines (/schedule, infra Anthropic) · Desktop tasks · /loop.':
        ('Routines (/schedule, Anthropic infra) · Desktop tasks · /loop.',),
    'SUBAGENTE':
        ('SUBAGENT',),
    'Sanitizar — líneas añadidas':
        ('Sanitize — added lines',),
    'Sanitizar → el humano hace push/PR. Un bot detecta un caso más → test + PLAYBOOK.':
        ('Sanitize → the human does push/PR. A bot catches one more case → test + PLAYBOOK.',),
    'Scheduling':
        ('Scheduling',),
    'Scope local':
        ('Local scope',),
    'Scope project':
        ('Project scope',),
    'Scope user':
        ('User scope',),
    'Se':
        ('Se',),
    'Se pide en lenguaje natural: “monta un equipo con un architect y dos implementers; exige aprobación de plan antes de tocar código”':
        ('You ask in natural language: ', '“set up a team with one architect and two implementers; require plan approval before touching code”'),
    'Se re-mapea por repo':
        ('Re-mapped per repo',),
    "Seguridad (.env), formato (prettier), type-check bloqueante, 'IA revisando IA' vía SDK.":
        ("Security (.env), formatting (prettier), blocking type-check, 'AI reviewing AI' via SDK.",),
    'Separa exploración (plan mode) de implementación; el ruido no se queda a vivir.':
        ("Separates exploration (plan mode) from implementation; the noise doesn't move in.",),
    'Serena + CodeGraph localizan el detector; un _diag_pdf.py determinista da la causa: SIN LLM.':
        ('Serena + CodeGraph locate the detector; a deterministic _diag_pdf.py gives the cause: NO LLM.',),
    'Serena find_referencing_symbols — desambigua por clase (antes de renombrar)':
        ('Serena find_referencing_symbols — disambiguates by class (before renaming)',),
    'Serena → pre-refactor':
        ('Serena → pre-refactor',),
    'Serena: navegación semántica, chequeo preciso':
        ('Serena: semantic navigation, precise check',),
    'Servers que uso':
        ('Servers I use',),
    'Sesiones que viajan entre superficies':
        ('Sessions that travel across surfaces',),
    'Sesión larga, turnos frecuentes':
        ('Long session, frequent turns',),
    'Side-quests: investigar, verificar':
        ('Side-quests: investigate, verify',),
    'Sigue una sesión local desde el móvil o cualquier navegador.':
        ('Follow a local session from your phone or any browser.',),
    'Skills':
        ('Skills',),
    'Slash commands':
        ('Slash commands',),
    'Solo al final':
        ('Only at the end',),
    'Solo resultado → principal':
        ('Result only → main',),
    'Starter-kit probado en Copilot; machine-sync con guardrails.':
        ('Starter-kit proven on Copilot; machine-sync with guardrails.',),
    'Subagentes especializados':
        ('Specialized subagents',),
    'Subagentes para investigar':
        ('Subagents for investigation',),
    'Subagentes: el ruido muere fuera de tu sesión':
        ('Subagents: noise dies outside your session',),
    'Subagents & teams + automatización':
        ('Subagents & teams + automation',),
    'System prompt':
        ('System prompt',),
    'TTL 1 hora':
        ('TTL 1 hour',),
    'TTL 5 min (defecto)':
        ('TTL 5 min (default)',),
    'Task list + mensajes entre teammates':
        ('Task list + messages between teammates',),
    'Teleport':
        ('Teleport',),
    'Test RED → fix estructural (no cliente) → regresión no-op + contrato local (wrapper) + dentro de la imagen desplegada.':
        ('RED test → structural fix (not client) → no-op regression + local contract (wrapper) + inside the deployed image.',),
    'Tools':
        ('Tools',),
    'Tools MCP':
        ('MCP tools',),
    'Transferible y hasta en ops':
        ('Transferable, even to ops',),
    'Triaje inbound: ¿síntoma en el contrato?':
        ('Inbound triage: symptom in the contract?',),
    'Tu CLAUDE.md':
        ('Your CLAUDE.md',),
    'U':
        ('U',),
    'Un caso completo construido con graphify — no con CodeGraph: la memoria del proyecto, navegable.':
        ("A complete case built with graphify — not CodeGraph: the project's memory, navigable.",),
    'Un curso, tres partes':
        ('One course, three parts',),
    'Un ejemplo real: arquitectura de la aplicación':
        ('A real example: application architecture',),
    'Un ejemplo real, de principio a fin':
        ('A real example, end to end',),
    'Un runbook real: sincronizar máquinas':
        ('A real runbook: syncing machines',),
    'Una línea; CLAUDE.md de dos niveles; sesiones que viajan.':
        ('One line; two-tier CLAUDE.md; sessions that travel.',),
    'Una sesión de 50 turnos relee el prefijo 50 veces a 0.1× — ese es el descuento que hace viables las sesiones largas.':
        ('A 50-turn session re-reads the prefix 50 times at 0.1× — ', "that's the discount that makes long sessions viable."),
    'Ventana: 200K tokens (1M en beta vía API). El rendimiento degrada ANTES de llenarla: contexto con ruido = peores decisiones. Auto-compact salta cerca del límite y es lossy — mejor /compact manual con foco.':
        ('Window: 200K tokens (1M in beta via API). ', 'Performance degrades BEFORE it fills: noisy context = worse decisions. Auto-compact fires near the limit and is lossy — better a focused manual /compact.'),
    'Verificar: contrato (wrapper) + imagen desplegada':
        ('Verify: contract (wrapper) + deployed image',),
    'Viaja SIN cambios (las 5 reglas)':
        ('Travels UNCHANGED (the 5 rules)',),
    'Windows':
        ('Windows',),
    '_AGENT_TEAMS": "1" },':
        ('_AGENT_TEAMS": "1" },',),
    'a':
        ('a',),
    'apt / dnf / apk en Debian, Fedora, RHEL, Alpine.':
        ('apt / dnf / apk on Debian, Fedora, RHEL, Alpine.',),
    'b':
        ('b',),
    'brew install --cask claude-code (brew upgrade para actualizar).':
        ('brew install --cask claude-code (brew upgrade to update).',),
    'búsqueda de nodos, panel de info, filtro por comunidad (vis-network).':
        ('node search, info panel, community filter (vis-network).',),
    'c':
        ('c',),
    'cd tu-proyecto':
        ('cd ', 'your-project'),
    'claude            # login la 1ª vez':
        ('claude', '            # login the 1st ', 'time'),
    'claude --teleport trae una sesión web/móvil al terminal.':
        ('claude --teleport brings a web/mobile session to the terminal.',),
    'claude -p en cualquier tubería Unix o script.':
        ('claude -p in any Unix pipe or script.',),
    'claude mcp add --transport http context7 https://mcp.context7.com/mcp':
        ('claude mcp add --transport http context7 https://mcp.context7.com/mcp',),
    'claude mcp add serena -- uvx \\':
        ('claude mcp add serena -- uvx \\',),
    'claude mcp list      # estado      /mcp   # auth OAuth y tools dentro de la sesión':
        ('claude mcp list      # status      /mcp   # OAuth auth and tools in-session',),
    'codegraph explore "<símbolo|pregunta>"':
        ('codegraph explore "<symbol|question>"',),
    'codegraph init      # crea .codegraph/':
        ('codegraph init      # creates .codegraph/',),
    'codegraph serve --path <repo> --mcp':
        ('codegraph serve --path <repo> --mcp',),
    'codegraph sync      # incremental tras editar':
        ('codegraph sync      # incremental after edits',),
    'crece':
        ('grows',),
    'curl -fsSL https://claude.ai/install.sh | bash — macOS/Linux/WSL, con auto-update.':
        ('curl -fsSL https://claude.ai/install.sh | bash — macOS/Linux/WSL, with auto-update.',),
    'd':
        ('d',),
    'de asistente a sistema de desarrollo agéntico':
        ('from assistant to ', 'agentic development system'),
    'description: Revisa vulnerabilidades':
        ('description: Reviews vulnerabilities',),
    'escribir 1.25×':
        ('write 1.25×',),
    'escribir 2×':
        ('write 2×',),
    'ficheros leídos, output de comandos… crece cada turno':
        ('files read, command output… grows every turn',),
    'fijo':
        ('fixed',),
    'for await (const m of query({ prompt, options: { allowedTools: ["Edit"] } }))':
        ('for await (const m of query({ prompt, options: { ', 'allowedTools', ': ["Edit"] } }))'),
    'git diff main --name-only | claude -p "revisa estos ficheros por seguridad"':
        ('git diff main --name-only | claude -p "review these files for security"',),
    'graph.html interactivo:':
        ('interactive graph.html:',),
    'if (payload.tool_input':
        ('if (payload.tool_input',),
    'import { query } from "@anthropic-ai/claude-agent-sdk";':
        ('import { query } from "@anthropic-ai/', 'claude', '-agent-', 'sdk', '";'),
    'kg_refresh.sh finalize  # output/ + leak-check':
        ('kg_refresh.sh finalize  # output/ + leak-check',),
    'kg_refresh.sh prepare   # manifest -> stage':
        ('kg_refresh.sh prepare   # manifest -> stage',),
    'leer 0.1×':
        ('read 0.1×',),
    'lo que tú decidas — por eso el patrón de dos niveles':
        ('whatever you decide — hence the two-tier pattern',),
    'messages=[{"role": "user",':
        ('messages=[{"role": "user",',),
    'metered':
        ('metered',),
    'model: opus':
        ('model: opus',),
    'name: security-reviewer':
        ('name: security-reviewer',),
    'por server':
        ('per server',),
    'preciso':
        ('precise',),
    'process.exit(0);':
        ('process.exit(0);',),
    'read-only':
        ('read-only',),
    'reproducir':
        ('reproduce',),
    'serena · context7 · playwright · codegraph · supabase.':
        ('serena · context7 · playwright · codegraph · supabase.',),
    'sin inferencia':
        ('no inference',),
    'system=[{ "type": "text",':
        ('system=[{ "type": "text",',),
    'tail -200 app.log | claude -p "avísame si ves anomalías"':
        ('tail -200 app.log | claude -p "flag any anomalies you see"',),
    'tools: Read, Grep, Glob, Bash':
        ('tools: Read, Grep, Glob, Bash',),
    'tú decides':
        ('you decide',),
    'winget install Anthropic.ClaudeCode · o el instalador PowerShell.':
        ('winget install Anthropic.ClaudeCode · or the PowerShell installer.',),
    '{ "env": { "CLAUDE_CODE_EXPERIMENTAL':
        ('{ "env": { "CLAUDE_CODE_EXPERIMENTAL',),
    '}':
        ('}',),
    '~/.claude.json — todos tus proyectos.':
        ('~/.claude.json — all your projects.',),
    '~/.claude/CLAUDE.md      # global usuario':
        ('~/.claude/CLAUDE.md      # user global',),
    '~4.200 tokens — oculto, siempre primero':
        ('~4,200 tokens — hidden, always first',),
    '~680 + ~280 tokens al arrancar':
        ('~680 + ~280 tokens at startup',),
    '¿Lo usamos aquí? No: este proyecto corre el flujo de 11 etapas + data/changes/, más depurado para fixes por ticket. GSD encaja en un greenfield multi-componente (roadmap → fases). Aquí ilustra la Parte 1: subagentes custom + skills como plugin.':
        ('Do we use it here? No: ', 'this project runs the 11-stage workflow + data/changes/, more refined for per-ticket fixes. GSD fits a multi-component greenfield (roadmap → phases). Here it illustrates Part 1: custom subagents + skills as a plugin.'),
    '¿Subagente o team? La decisión':
        ('Subagent or team? The decision',),
    'Índice tree-sitter → SQLite (.codegraph/)':
        ('Tree-sitter index → SQLite (.codegraph/)',),
    'Úsalo para':
        ('Use it for',),
    'índice ~120 tokens; el schema, al usar la tool':
        ('index ~120 tokens; the schema, on tool use',),
    "“ CodeGraph responde '¿qué se rompe?'; Serena responde '¿exactamente quién llama a ESTE process()?' ”":
        ('“ ', "CodeGraph answers 'what breaks?'; Serena answers 'exactly who calls THIS process()?'", ' ”'),
    '“ Con instrucciones le pides que se porte bien; con un hook lo garantizas. ”':
        ('“ ', 'With instructions you ask for good behavior; with a hook you guarantee it.', ' ”'),
    '“ Contexto hay que leer y esto lo hace mas estable rinde mejor y cuesta menos: dos niveles optimiza ambos ejes a la vez. ”':
        ('“ ', 'Lean, stable context performs better AND costs less: two tiers optimize both axes at once.', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', ' ”'),
    '“ Demo ejecutable: ejemplos/prompt-caching/cache_demo.py — mira los contadores de cache. ”':
        ('“ ', 'Runnable demo: ejemplos/prompt-caching/cache_demo.py — watch the cache counters.', ' ”'),
    '“ Ejemplos reales en ejemplos/subagents/: security-reviewer y refactor-scout (regla CodeGraph→Serena). ”':
        ('“ ', 'Real examples in ejemplos/subagents/: security-reviewer and refactor-scout (CodeGraph→Serena rule).', ' ”'),
    '“ El agente orquesta y es donde vive la inferencia; lo caro se concentra en plan/código/verify, no en buscar. ”':
        ('“ ', 'The agent orchestrates and hosts the inference; cost concentrates in plan/code/verify, not in searching.', ' ”'),
    '“ El mismo motor y los mismos CLAUDE.md/settings/MCP en todas las superficies. ”':
        ('“ ', 'The same engine and the same CLAUDE.md/settings/MCP across all surfaces.', ' ”'),
    '“ El modelo no gana confianza gratis: la gana decisión a decisión, con evidencia. ”':
        ('“ ', "The model doesn't earn trust for free: it earns it decision by decision, with evidence.", ' ”'),
    '“ Instalar es trivial; el valor está en cómo lo usas. ”':
        ('“ ', 'Installing is trivial; the value is in how you use it.', ' ”'),
    '“ La inversión clásica — el modelo diagnostica — es lo que este orden evita: el modelo verifica; los oráculos diagnostican. ”':
        ('“ ', 'The classic inversion — the model diagnoses — is what this order avoids: the model verifies; the oracles diagnose.', ' ”'),
    "“ La metodología no es solo para código: memoria durable, guardrails y 'el humano hace lo externo' también en ops. ”":
        ('“ ', "The methodology isn't just for code: durable memory, guardrails and 'the human does the external' in ops too.", ' ”'),
    '“ La prevalencia de tools de la Parte 2 es, en el fondo, política de contexto. ”':
        ('“ ', "Part 2's tool precedence is, at bottom, context policy.", ' ”'),
    '“ Las comunidades mapean a zonas de peligro reales; los god-nodes son la lista de onboarding gratis. ”':
        ('“ ', 'Communities map to real danger zones; the god-nodes are a free onboarding list.', ' ”'),
    '“ Material completo (diseño, scripts, tests, salida real): docs/knowledge-graph/. ”':
        ('“ ', 'Full material (design, scripts, tests, real output): docs/knowledge-graph/.', ' ”'),
    '“ Mide con /context antes de optimizar: te dice exactamente qué bloque engorda. ”':
        ('“ ', 'Measure with /context before optimizing: it tells you exactly which block bloats.', ' ”'),
    '“ Mismo método, productizado: GSD para greenfield multi-fase; aquí, data/changes/ afinado a fixes por ticket. ”':
        ('“ ', 'Same method, productized: GSD for multi-phase greenfield; here, data/changes/ tuned to per-ticket fixes.', ' ”'),
    '“ Particiona los ficheros: cada teammate es dueño de los suyos. ”':
        ('“ ', 'Partition the files: each teammate owns theirs.', ' ”'),
    '“ Recortamos el CLAUDE.md ~73% sin perder información: punteros, no copias. ”':
        ('“ ', 'We cut CLAUDE.md ~73% with no information loss: pointers, not copies.', ' ”'),
    '“ Si solo conservas cinco reglas, conserva esas cinco. Las tools se sustituyen; la disciplina viaja. ”':
        ('“ ', 'If you keep only five rules, keep these five. Tools get swapped; the discipline travels.', ' ”'),
    '“ Slash command = atajo que invocas tú. Skill = capacidad que Claude decide usar. Plugin = el reparto. ”':
        ('“ ', 'Slash command = shortcut you invoke. Skill = capability Claude decides to use. Plugin = the distribution.', ' ”'),
    '“ Staging con provenance: sst-5468__sst-5468.md, hub__STATUS.md, memory__x.md — cada nodo traza a su fuente. ”':
        ('“ ', 'Staging with provenance: sst-5468__sst-5468.md, hub__STATUS.md, memory__x.md — each node traces to its source.', ' ”'),
    '“ Subagente para que el ruido muera fuera; team para que varios Claudes debatan. El coste no es el mismo. ”':
        ('“ ', 'Subagent so noise dies outside; team so several Claudes can debate. The cost is not the same.', ' ”'),
    '“ Un paso semántico en el build, cero LLM en la consulta. El grafo es el mapa; el agente, el guía. ”':
        ('“ ', 'One semantic step in the build, zero LLM in the query. The graph is the map; the agent, the guide.', ' ”'),
    '“ Una consulta en vez de grep→abrir→seguir-import→repetir. Menos contexto, más señal. ”':
        ('“ ', 'One query instead of grep→open→follow-import→repeat. Less context, more signal.', ' ”'),
    '“La autonomía se gana por-decisión, no se concede en bloque.”':
        ('“Autonomy is earned per-decision, not granted wholesale.”',),
    '“lee config/auth.js” > “entiende el auth”. Adelanto: CodeGraph-primero (Parte 2).':
        ('“read config/auth.js” > “understand the auth”. Preview: CodeGraph-first (Part 2).',),
    '→':
        ('→',),
    '↺':
        ('↺',),
    '⌁':
        ('⌁',),
    '■ Los recuadros coral son GATES (puntos de decisión). Un gate rojo = STOP: no escribir código.':
        ('■ ', 'Coral boxes are GATES (decision points). A red gate = STOP: no writing code.'),
    '▣':
        ('▣',),
    '▸  -h dereferencia el symlink de .aws (crítico)':
        ('▸  ', '-h dereferences the .aws symlink (critical)'),
    '▸  /kg <ticket|tema> ANTES de grep':
        ('▸  ', '/kg <ticket|topic> BEFORE grep'),
    '▸  /kg y /kg-refresh — skills de Claude Code':
        ('▸  ', '/kg and /kg-refresh — Claude Code skills'),
    '▸  116 ficheros, ~196k palabras':
        ('▸  ', '116 files, ~196k words'),
    '▸  35 comunidades':
        ('▸  ', '35 communities'),
    '▸  507 nodos · 672 aristas':
        ('▸  ', '507 nodes · 672 edges'),
    '▸  7% INFERRED (conf. 0.7)':
        ('▸  ', '7% INFERRED (conf. 0.7)'),
    '▸  92% EXTRACTED (fiable)':
        ('▸  ', '92% EXTRACTED (reliable)'),
    '▸  <TICKET>/<TICKET>.md — ~55 ledgers autocontenidos':
        ('▸  ', '<TICKET>/<TICKET>.md — ~55 self-contained ledgers'),
    '▸  Abres `claude` y conversas':
        ('▸  ', 'You open `claude` and talk'),
    '▸  Apunta a QUÉ leer; no lo sustituye':
        ('▸  ', "Points at WHAT to read; doesn't replace it"),
    '▸  Aristas: llamadas, imports, herencia, referencias':
        ('▸  ', 'Edges: calls, imports, inheritance, references'),
    '▸  Claude guarda aprendizajes (comandos de build, pistas de debug) entre sesiones sin que escribas nada.':
        ('▸  ', 'Claude stores learnings (build commands, debug hints) across sessions without you writing anything.'),
    '▸  Contexto AISLADO: solo el resumen vuelve a tu sesión':
        ('▸  ', 'ISOLATED context: only the summary returns to your session'),
    '▸  Coste: cada teammate es una sesión completa':
        ('▸  ', 'Cost: each teammate is a full session'),
    '▸  Decisiones go/no-go y el scope':
        ('▸  ', 'Go/no-go decisions and scope'),
    '▸  Densidad sin conocimiento nuevo = ruido':
        ('▸  ', 'Density without new knowledge = noise'),
    '▸  Desktop (diffs, sesiones en paralelo)':
        ('▸  ', 'Desktop (diffs, ', 'sessions', ' ', 'in', ' ', 'parallel', ')'),
    '▸  Determinista (del AST), sin API keys':
        ('▸  ', 'Deterministic (from the AST), no API keys'),
    '▸  Devuelve: fuente + rutas + blast radius + cobertura':
        ('▸  ', 'Returns: source + paths + blast radius + coverage'),
    '▸  Docs gitignored de data/ + memoria (snapshot-memory) viajan':
        ('▸  ', 'Gitignored docs in data/ + memory (snapshot-memory) travel'),
    '▸  El contrato: HTTP / DB / evento / artefacto':
        ('▸  ', 'The contract: HTTP / DB / event / artifact'),
    '▸  El código ya está en GitHub → git fetch':
        ('▸  ', 'The code is already on GitHub → git fetch'),
    '▸  El grafo lo hace EXPLÍCITO y consultable en 1 llamada':
        ('▸  ', 'The graph makes it EXPLICIT and queryable in 1 call'),
    '▸  El humano es dueño de push/PR/deploy':
        ('▸  ', 'The human owns push/PR/deploy'),
    '▸  El humano hace push / merge; el agente prepara y reporta con evidencia (conteos, PRs)':
        ('▸  ', 'The human does push / merge; the agent prepares and reports with evidence (counts, PRs)'),
    '▸  El humano posee lo externo (merge, deploy)':
        ('▸  ', 'The human owns the external (merge, deploy)'),
    '▸  El tracker: Jira · Azure Boards · Issues':
        ('▸  ', 'The tracker: Jira · Azure Boards · Issues'),
    '▸  En destino: bootstrap (/kg) + target-setup.sh rehacen el tooling':
        ('▸  ', 'On target: bootstrap (/kg) + target-setup.sh rebuild the tooling'),
    '▸  En la principal: restore-memory → /kg-refresh reconstruye':
        ('▸  ', 'On the main one: restore-memory → /kg-refresh rebuilds'),
    '▸  En paralelo para trabajo independiente':
        ('▸  ', 'In parallel for independent work'),
    '▸  Encaja en tuberías Unix y en CI':
        ('▸  ', 'Fits Unix pipes and CI'),
    '▸  Encontrarlo a mano = recordar que existe + grep':
        ('▸  ', 'Finding it by hand = remembering it exists + grep'),
    '▸  Es la onboarding de 30s del agente':
        ('▸  ', "It's the agent's 30s onboarding"),
    '▸  Etapa 1 (Orientar) del flujo de 11 etapas':
        ('▸  ', 'Stage 1 (Orient) of the 11-stage workflow'),
    '▸  Eventos: PreToolUse, PostToolUse, SessionStart, Stop…':
        ('▸  ', 'Events: PreToolUse, PostToolUse, SessionStart, Stop…'),
    '▸  Exclusiones duras: binarios, handovers repetidos, copias stale (payload/)':
        ('▸  ', 'Hard exclusions: binaries, repeated handovers, stale copies (payload/)'),
    '▸  Excluye venvs / node_modules / caches / .codegraph':
        ('▸  ', 'Excludes venvs / node_modules / caches / .codegraph'),
    '▸  Explore — búsqueda read-only por el codebase':
        ('▸  ', 'Explore — read-only search across the codebase'),
    '▸  Ideal para explorar, diseñar, depurar':
        ('▸  ', 'Ideal for exploring, designing, debugging'),
    '▸  Investigación y diagnóstico':
        ('▸  ', 'Investigation and diagnosis'),
    '▸  La aprobación del plan':
        ('▸  ', 'Plan approval'),
    '▸  La base de toda la automatización':
        ('▸  ', 'The foundation of all automation'),
    '▸  La pirámide de tests y el runtime desplegado':
        ('▸  ', 'The test pyramid and the deployed runtime'),
    '▸  Las reglas de sanitización locales':
        ('▸  ', 'The local sanitization rules'),
    '▸  Las tools: Serena/CodeGraph//kg son fungibles':
        ('▸  ', 'The tools: Serena/CodeGraph//kg are fungible'),
    '▸  Lead + teammates: cada uno una SESIÓN completa':
        ('▸  ', 'Lead + teammates: each one a full SESSION'),
    '▸  Matcher = regex sobre el nombre de la tool':
        ('▸  ', 'Matcher = regex on the tool name'),
    '▸  Mensajería directa entre teammates (inboxes)':
        ('▸  ', 'Direct messaging between teammates (inboxes)'),
    '▸  NO hereda tu conversación: contexto en el prompt':
        ('▸  ', 'Does NOT inherit your conversation: context in the prompt'),
    '▸  Opera sobre SÍMBOLOS, no texto: precisión de IDE':
        ('▸  ', 'Operates on SYMBOLS, not text: IDE precision'),
    '▸  Orientación mínima: qué es el proyecto, mapa de repos, comandos':
        ('▸  ', 'Minimal orientation: what the project is, repo map, commands'),
    '▸  PLAYBOOK.md — lecciones de debugging':
        ('▸  ', 'PLAYBOOK.md — debugging lessons'),
    '▸  Payload del evento por STDIN':
        ('▸  ', 'Event payload via STDIN'),
    '▸  Plan mode: propone un plan y tú lo apruebas antes de tocar nada':
        ('▸  ', 'Plan mode: it proposes a plan and you approve before touching anything'),
    '▸  Plan — diseñar la estrategia':
        ('▸  ', 'Plan — design the strategy'),
    '▸  Plan → acuerdo → implementar':
        ('▸  ', 'Plan → agreement → implement'),
    '▸  Planes e implementación':
        ('▸  ', 'Plans and implementation'),
    '▸  Plantillas STATUS · SHARP_EDGES · handover · QA + bootstrap-new-repo.ps1 → estructura en el repo destino':
        ('▸  ', 'STATUS · SHARP_EDGES · handover · QA templates + bootstrap-new-repo.ps1 → structure in the target repo'),
    '▸  Pre = intención (tool_input) · Post = resultado (tool_response)':
        ('▸  ', 'Pre = intent (tool_input) · Post = result (tool_response)'),
    '▸  Pueden debatir hallazgos, no solo reportar':
        ('▸  ', 'They can debate findings, not just report'),
    '▸  Rastro durable: porqué, qué, cómo se verificó':
        ('▸  ', 'Durable trail: why, what, how it was verified'),
    '▸  Recall en zonas densas · EXTRACTED = fiable, INFERRED = pista · interno (data/) · derivado se reconstruye, pero lo escrito a mano viaja':
        ('▸  ', 'Recall in dense zones · EXTRACTED = reliable, INFERRED = hint · internal (data/) · derived gets rebuilt, but hand-authored files travel'),
    '▸  Regla history-first del CLAUDE.md:':
        ('▸  ', 'CLAUDE.md history-first rule:'),
    '▸  Regla write-once: el core apunta, no copia':
        ('▸  ', "Write-once rule: the core points, doesn't copy"),
    '▸  Reglas concretas, no Bash(*)':
        ('▸  ', 'Concrete rules, not Bash(*)'),
    '▸  Resolver la clase general, no un input':
        ('▸  ', 'Solve the general class, not one input'),
    '▸  Roles = tus subagentes custom reutilizados':
        ('▸  ', 'Roles = your custom subagents reused'),
    "▸  SHARP_EDGES.md — invariantes 'no tocar'":
        ('▸  ', "SHARP_EDGES.md — 'do not touch' invariants"),
    '▸  Sin /resume in-process · un team por sesión · sin anidar':
        ('▸  ', 'No in-process /resume · one team per session · no nesting'),
    '▸  Sin grafo de tickets: fallback determinista (STATUS newest-first + búsqueda léxica + historia de commits) = 80% del valor':
        ('▸  ', 'Without the ticket graph: deterministic fallback (STATUS newest-first + lexical search + commit history) = 80% of the value'),
    '▸  Solo PUNTEROS de una línea a todo lo demás':
        ('▸  ', 'Only one-line POINTERS to everything else'),
    '▸  Solo no-destructivo (renombrar, no borrar) · git fetch = única op de red':
        ('▸  ', "Non-destructive only (rename, don't delete) · git fetch = only network op"),
    '▸  Split-panes requiere tmux o iTerm2':
        ('▸  ', 'Split-panes require tmux or iTerm2'),
    '▸  Símbolos: funciones, clases, rutas, componentes':
        ('▸  ', 'Symbols: functions, classes, routes, components'),
    '▸  Task list compartida: ~/.claude/tasks/<team>/':
        ('▸  ', 'Shared task list: ~/.claude/tasks/<team>/'),
    '▸  Terminal · VS Code / Cursor · JetBrains':
        ('▸  ', 'Terminal · VS Code / Cursor · JetBrains'),
    '▸  Tests y documentación':
        ('▸  ', 'Tests and documentation'),
    '▸  Toda acción externa: push, PR, deploy':
        ('▸  ', 'Every external action: push, PR, deploy'),
    '▸  USB: mount manual en WSL + verificar byte a byte':
        ('▸  ', 'USB: manual mount in WSL + byte-for-byte verify'),
    "▸  Un bug 'nuevo' casi siempre tiene contexto previo que restringe el fix":
        ('▸  ', "A 'new' bug almost always has prior context constraining the fix"),
    '▸  Un prompt: entra por stdin, sale por stdout':
        ('▸  ', 'One prompt: in via stdin, out via stdout'),
    '▸  Un tarball: workspace + ~/.claude · .aws · .ssh':
        ('▸  ', 'One tarball: workspace + ~/.claude · .aws · .ssh'),
    '▸  Verificar en el contrato del CONSUMIDOR':
        ('▸  ', "Verify against the CONSUMER's contract"),
    '▸  Web (claude.ai/code, tareas largas)':
        ('▸  ', 'Web (claude.ai/code, ', 'tasks', ' ', 'long', ')'),
    '▸  Writeups sst-* (+ fallback determinista) · hubs · runbooks · memoria':
        ('▸  ', 'sst-* writeups (+ deterministic fallback) · hubs · runbooks · memory'),
    '▸  backup + diff de STATUS.md; STOP si hubo ediciones propias':
        ('▸  ', 'backup + diff of STATUS.md; STOP if it had manual edits'),
    '▸  build_manifest.py + stage_corpus.py — el corpus':
        ('▸  ', 'build_manifest.py + stage_corpus.py — the corpus'),
    '▸  data/changes/STATUS.md — estado vivo por ticket':
        ('▸  ', 'data/changes/STATUS.md — live state per ticket'),
    '▸  description = auto-selección · tools = allowlist propio':
        ('▸  ', 'description = auto-selection · tools = own allowlist'),
    '▸  exit 0 permite · exit 2 BLOQUEA (stderr → Claude)':
        ('▸  ', 'exit 0 allows · exit 2 BLOCKS (stderr → Claude)'),
    '▸  find_referencing_symbols — quién referencia, POR CLASE':
        ('▸  ', 'find_referencing_symbols — who references, BY CLASS'),
    '▸  find_symbol (body=true) — un método de un fichero de 5k líneas':
        ('▸  ', 'find_symbol (body=true) — one method from a 5k-line file'),
    '▸  general-purpose — multi-paso, todos los tools':
        ('▸  ', 'general-purpose — multi-step, all tools'),
    '▸  get_symbols_overview — esqueleto de un fichero':
        ('▸  ', "get_symbols_overview — a file's skeleton"),
    '▸  gsd-code-reviewer — REVIEW.md por severidad':
        ('▸  ', 'gsd-code-reviewer — REVIEW.md by severity'),
    '▸  gsd-executor — commits atómicos, checkpoints':
        ('▸  ', 'gsd-executor — atomic commits, checkpoints'),
    '▸  gsd-plan-checker — ¿logrará el objetivo? (goal-backward)':
        ('▸  ', 'gsd-plan-checker — will it meet the goal? (goal-backward)'),
    '▸  gsd-planner — desglose + dependencias':
        ('▸  ', 'gsd-planner — breakdown + dependencies'),
    '▸  gsd-verifier — verifica el OBJETIVO, no solo tareas':
        ('▸  ', 'gsd-verifier — verifies the GOAL, not just tasks'),
    '▸  kg_query.sh — envuelve graphify explain/path + find':
        ('▸  ', 'kg_query.sh — wraps graphify explain/path + find'),
    '▸  kg_refresh.sh — prepare · finalize · bootstrap · snapshot/restore-memory':
        ('▸  ', 'kg_refresh.sh — prepare · finalize · bootstrap · snapshot/restore-memory'),
    '▸  manifest.txt DIFFEABLE: ~116 ficheros, ~196k palabras':
        ('▸  ', 'manifest.txt DIFFABLE: ~116 files, ~196k words'),
    '▸  mcp__serena__find_symbol, pytest exacto…':
        ('▸  ', 'mcp__serena__find_symbol, exact pytest…'),
    '▸  search_for_pattern · activate_project (multi-repo)':
        ('▸  ', 'search_for_pattern · activate_project (multi-repo)'),
    '▸  settings.json: allow / deny / ask':
        ('▸  ', 'settings.json: allow / deny / ask'),
    '▸  test_kg_*.py — los bookends, TESTEADOS':
        ('▸  ', 'test_kg_*.py — the bookends, TESTED'),
    '▸  ~540 ficheros de writeups, sharp edges, runbooks, memoria':
        ('▸  ', '~540 files of writeups, sharp edges, runbooks, memory'),
    '★':
        ('★',),
}

# ---------------------------------------------------------------------------
# MANUAL ADDITIONS — hand-written, not harvested.
#
# The block above was harvested ONCE from the 2026-07-21 decks; those decks are
# frozen, so it will not be regenerated. Everything below covers lines that were
# added or reworded after that date (the S3 slide, the five-check gate) plus a
# few the harvest could not pair because the two decks split their runs
# differently. Keep new entries here, not in the generated block.
#
# Run counts MUST match what build_pptx.py emits for that line; --lang en
# reports any mismatch instead of silently dropping formatting.
# ---------------------------------------------------------------------------
TRANSLATIONS.update({
    # --- part dividers (2 runs: bold coral prefix + rest) --------------------
    "PARTE 1 — Claude Code: instalación · memoria · contexto & caching · MCP · skills · subagents & teams · automatización":
        ("PART 1 — ", "Claude Code: install · memory · context & caching · MCP · skills · subagents & teams · automation"),
    "PARTE 2 — La metodología (agnóstica): flujo con gates · CodeGraph / Serena / GSD · transferencia · ops":
        ("PART 2 — ", "The methodology (agnostic): workflow with gates · CodeGraph / Serena / GSD · transfer · ops"),
    "PARTE 3 — El grafo de conocimiento de tickets, construido con graphify: pipeline, comandos /kg y el grafo real":
        ("PART 3 — ", "The ticket knowledge graph, built with graphify: pipeline, /kg commands and the real graph"),

    # --- flow slide: the outbound gate is five checks, not three -------------
    "Verificar: 5 checks (instrumento → contrato → imagen)":
        ("Verify: 5 checks (instrument → contract → image)",),
    "■ Coral = GATE (STOP: no escribir código).   Etapa 7, los 5 checks: instrumento · contrato (wrapper) · miembros, no totales · imagen · mirar":
        ("■ ", "Coral = GATE (STOP: don't write code).   ", "Stage 7, the 5 checks: ",
         "instrument · contract (wrapper) · members, not totals · image · look"),

    # --- section 11 split into transport (A) and sharing (B) -----------------
    "11 · Sincronizar máquinas: transportar y compartir (S3)":
        ("11 · Machine sync: transport and sharing (S3)",),
    "Sincronizar máquinas (A): transportar":
        ("Machine sync (A): transport",),
    "Sincronizar máquinas (B): compartir sobre S3":
        ("Machine sync (B): sharing over S3",),

    # --- the S3 slide --------------------------------------------------------
    "El tarball resuelve transportar entre TUS máquinas. No resuelve compartir: el registro es gitignored → no se puede enlazar desde un ticket, y cada persona acaba con su propio índice privado de la misma historia.":
        ("The tarball solves ", "transport", " between YOUR machines. It doesn't solve ", "sharing",
         ": the record is gitignored → it can't be linked from a ticket, and each person ends up with "
         "their own private index of the same history."),
    "Las reglas que lo hacen seguro":
        ("The rules that make it safe",),
    "Fuente de verdad vs. derivado":
        ("Source of truth vs. derived",),
    "Lo específico de los agentes: la máquina tiene rol":
        ("The agent-specific part: the machine has a role",),
    "▸  Alcance estrecho: docs + grafo. Nada de datos de cliente":
        ("▸  ", "Narrow scope: docs + graph. No client data"),
    "▸  Escribe por sync · lee por mount de SOLO LECTURA":
        ("▸  ", "Write via sync · read via READ-ONLY mount"),
    "▸  Dry-run por defecto; --go explícito; --delete aparte":
        ("▸  ", "Dry-run by default; explicit --go; --delete separate"),
    "▸  Versionado = 30 días, no merge · protege pull Y push":
        ("▸  ", "Versioning = 30 days, not a merge · guard pull AND push"),
    "▸  Los docs mandan; el grafo se DERIVA de ellos":
        ("▸  ", "Docs rule; the graph is DERIVED from them"),
    "▸  Los ficheros por ticket casi nunca chocan":
        ("▸  ", "Per-ticket files almost never collide"),
    "▸  El grafo es el único punto real de contención":
        ("▸  ", "The graph is the only real contention point"),
    "▸  → UN solo publisher. \"Derivado\" es del fichero, no de la carpeta":
        ("▸  ", "→ ONE single publisher. \"Derived\" is per file, not per folder"),
    "▸  Varias máquinas, permisos distintos → la sesión debe saber DÓNDE está antes de actuar":
        ("▸  ", "Several machines, different permissions → the session must know WHERE it is before acting"),
    "▸  MACHINE_NAME / MACHINE_ROLE → IDENTITY.md (machine-local) ← CLAUDE.md apunta a él":
        ("▸  ", "MACHINE_NAME / MACHINE_ROLE → IDENTITY.md (machine-local) ← CLAUDE.md points at it"),
    "“ Un mount escribible sobre almacenamiento de objetos no es una comodidad: es corrupción que descubres semanas después. ”":
        ("“ ", "A writable mount over object storage isn't a convenience: it's corruption you discover weeks later.", " ”"),

    # --- reworded since the 2026-07-21 harvest -------------------------------
    "“ Contexto lean y estable rinde mejor Y cuesta menos: dos niveles optimiza ambos ejes a la vez. ”":
        ("“ ", "Lean, stable context performs better AND costs less: two tiers optimize both axes at once.", " ”"),
    "Oráculo determinista: parser / validador / _diag_*.py":
        ("Deterministic oracle: parser / validator / _diag_*.py",),
    "Claude Code no expone cache_control: lo aplica solo (system + tools + historial = prefijo). Tus decisiones de la slide anterior determinan el hit-rate.":
        ("Claude Code doesn't expose cache_control: it applies it for you (system + tools + history = prefix). "
         "Your decisions on the previous slide set the hit-rate.",),
})
