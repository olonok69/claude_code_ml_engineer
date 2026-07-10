#!/usr/bin/env python3
"""
Generador del deck "Claude Code — Sesión técnica".

Reproduce el estilo del ejemplo Super_Resolucion_Presentacion.pptx: slides en
blanco dibujadas a mano con eyebrow + título + tarjetas numeradas + agenda +
franja de conclusión + footer. Idempotente: re-ejecutar regenera el .pptx.

    pip install python-pptx
    python build_pptx.py

Salida: Claude_Code_Presentacion.pptx (16:9, 13.33 x 7.5").
"""
from __future__ import annotations
import os
from pptx import Presentation
from pptx.util import Inches, Pt, Emu
from pptx.dml.color import RGBColor
from pptx.enum.shapes import MSO_SHAPE
from pptx.enum.text import PP_ALIGN, MSO_ANCHOR
from pptx.oxml.ns import qn

# ----------------------------------------------------------------------------- paleta
BG       = RGBColor(0x0F, 0x14, 0x1A)   # slate casi negro
PANEL    = RGBColor(0x1A, 0x21, 0x2B)   # tarjeta
PANEL_2  = RGBColor(0x22, 0x2B, 0x38)   # tarjeta alt / highlight
STROKE   = RGBColor(0x2E, 0x39, 0x48)   # borde sutil
CORAL    = RGBColor(0xD9, 0x77, 0x57)   # acento primario (Anthropic)
BLUE     = RGBColor(0x7A, 0xA2, 0xC7)   # acento secundario
GREEN    = RGBColor(0x8C, 0xC2, 0x8C)
TEXT     = RGBColor(0xE8, 0xEA, 0xED)   # texto principal
MUTED    = RGBColor(0x9A, 0xA4, 0xB2)   # texto secundario
FAINT    = RGBColor(0x66, 0x70, 0x7E)   # footer
FONT     = "Segoe UI"
MONO     = "Consolas"

EMU_W, EMU_H = Inches(13.333), Inches(7.5)


# ----------------------------------------------------------------------------- helpers
def _solid(shape, color):
    shape.fill.solid()
    shape.fill.fore_color.rgb = color


def _noline(shape):
    shape.line.fill.background()


def _line(shape, color, w=0.75):
    shape.line.color.rgb = color
    shape.line.width = Pt(w)


def rect(slide, x, y, w, h, fill=None, line=None, lw=0.75, rounded=False, radius=0.08):
    shp = slide.shapes.add_shape(
        MSO_SHAPE.ROUNDED_RECTANGLE if rounded else MSO_SHAPE.RECTANGLE,
        Inches(x), Inches(y), Inches(w), Inches(h),
    )
    if rounded:
        try:
            shp.adjustments[0] = radius
        except Exception:
            pass
    if fill is None:
        shp.fill.background()
    else:
        _solid(shp, fill)
    if line is None:
        _noline(shp)
    else:
        _line(shp, line, lw)
    shp.shadow.inherit = False
    return shp


def text(slide, x, y, w, h, runs, align=PP_ALIGN.LEFT, anchor=MSO_ANCHOR.TOP,
         space_after=4, line_spacing=1.0):
    """runs: lista de párrafos; cada párrafo es lista de (txt, size, color, bold, font)."""
    tb = slide.shapes.add_textbox(Inches(x), Inches(y), Inches(w), Inches(h))
    tf = tb.text_frame
    tf.word_wrap = True
    tf.vertical_anchor = anchor
    tf.margin_left = tf.margin_right = tf.margin_top = tf.margin_bottom = 0
    for i, para in enumerate(runs):
        p = tf.paragraphs[0] if i == 0 else tf.add_paragraph()
        p.alignment = align
        p.space_after = Pt(space_after)
        p.space_before = Pt(0)
        p.line_spacing = line_spacing
        for (t, size, color, bold, font) in para:
            r = p.add_run()
            r.text = t
            r.font.size = Pt(size)
            r.font.color.rgb = color
            r.font.bold = bold
            r.font.name = font
    return tb


def R(t, size, color, bold=False, font=FONT):
    return (t, size, color, bold, font)


# ----------------------------------------------------------------------------- chrome
def base(slide, eyebrow=None, ttl=None, page=None):
    rect(slide, -0.1, -0.1, 13.53, 7.7, fill=BG)                     # fondo
    rect(slide, 0, 0, 0.22, 7.5, fill=CORAL)                         # barra lateral
    if eyebrow:
        text(slide, 0.7, 0.55, 11, 0.4,
             [[R(eyebrow.upper(), 12, CORAL, True)]])
    if ttl:
        text(slide, 0.68, 0.92, 12, 1.1, [[R(ttl, 30, TEXT, True)]])
        rect(slide, 0.72, 1.72, 1.1, 0.045, fill=CORAL)
    if page is not None:
        text(slide, 0.7, 7.02, 8, 0.35,
             [[R("Claude Code · Sesión técnica", 9.5, FAINT, False)]])
        text(slide, 11.8, 7.02, 1.2, 0.35,
             [[R(str(page), 9.5, FAINT, True)]], align=PP_ALIGN.RIGHT)


def takeaway(slide, phrase):
    """Franja de conclusión (🗣️) al pie."""
    y = 6.35
    rect(slide, 0.7, y, 11.95, 0.52, fill=PANEL_2, line=STROKE, rounded=True, radius=0.28)
    rect(slide, 0.7, y, 0.09, 0.52, fill=CORAL, rounded=True, radius=0.5)
    text(slide, 0.95, y + 0.03, 11.6, 0.46,
         [[R("“ ", 13, CORAL, True), R(phrase, 12.5, TEXT, False),
           R(" ”", 13, CORAL, True)]], anchor=MSO_ANCHOR.MIDDLE)


def cards(slide, items, top=2.1, cols=2, height=1.02, gap=0.28, badge=CORAL, bottom_takeaway=True):
    """items: lista de (num, titulo, descripcion). Rejilla de tarjetas numeradas."""
    left, right = 0.7, 12.65
    total_w = right - left
    card_w = (total_w - gap * (cols - 1)) / cols
    for idx, (num, ttl, desc) in enumerate(items):
        r, c = divmod(idx, cols)
        x = left + c * (card_w + gap)
        y = top + r * (height + gap)
        rect(slide, x, y, card_w, height, fill=PANEL, line=STROKE, rounded=True, radius=0.09)
        # badge
        rect(slide, x + 0.22, y + 0.22, 0.5, 0.5, fill=badge, rounded=True, radius=0.32)
        text(slide, x + 0.22, y + 0.24, 0.5, 0.46,
             [[R(str(num), 15, BG, True)]], align=PP_ALIGN.CENTER, anchor=MSO_ANCHOR.MIDDLE)
        text(slide, x + 0.9, y + 0.16, card_w - 1.05, 0.4,
             [[R(ttl, 14.5, TEXT, True)]])
        text(slide, x + 0.9, y + 0.5, card_w - 1.05, height - 0.55,
             [[R(desc, 11, MUTED, False)]], line_spacing=1.02)


def code(slide, x, y, w, h, lines, title=None):
    if title:
        text(slide, x, y - 0.34, w, 0.3, [[R(title, 11, BLUE, True)]])
    rect(slide, x, y, w, h, fill=RGBColor(0x0A, 0x0E, 0x13), line=STROKE, rounded=True, radius=0.05)
    runs = [[R(ln, 11.5, TEXT if not ln.startswith("#") else MUTED, False, MONO)] for ln in lines]
    text(slide, x + 0.28, y + 0.2, w - 0.5, h - 0.35, runs, line_spacing=1.12, space_after=2)


def panel_bullets(slide, x, y, w, h, header, bullets, accent=CORAL):
    rect(slide, x, y, w, h, fill=PANEL, line=STROKE, rounded=True, radius=0.06)
    text(slide, x + 0.3, y + 0.22, w - 0.5, 0.4, [[R(header, 14, accent, True)]])
    runs = []
    for b in bullets:
        runs.append([R("▸  ", 11.5, accent, True), R(b, 11.5, TEXT, False)])
    text(slide, x + 0.3, y + 0.72, w - 0.55, h - 0.9, runs, line_spacing=1.05, space_after=6)


# ----------------------------------------------------------------------------- build
def build():
    prs = Presentation()
    prs.slide_width = EMU_W
    prs.slide_height = EMU_H
    blank = prs.slide_layouts[6]

    def new():
        return prs.slides.add_slide(blank)

    # ---- 1. Portada
    s = new()
    rect(s, -0.1, -0.1, 13.53, 7.7, fill=BG)
    rect(s, 0, 0, 13.333, 0.16, fill=CORAL)
    rect(s, 0, 7.34, 13.333, 0.16, fill=CORAL)
    text(s, 1.0, 1.5, 11, 0.5, [[R("SESIÓN TÉCNICA · DEVELOPER TOOLING", 14, CORAL, True)]])
    text(s, 0.95, 2.15, 11.5, 2.0,
         [[R("Claude Code", 60, TEXT, True)],
          [R("de asistente a ", 26, MUTED, False), R("sistema de desarrollo agéntico", 26, TEXT, True)]],
         space_after=10)
    rect(s, 1.02, 4.35, 1.4, 0.05, fill=CORAL)
    text(s, 1.0, 4.6, 11.5, 0.9,
         [[R("Instalación · Memoria & sesiones · MCP · Skills & plugins · Automatización · Metodología",
             14.5, MUTED, False)]])
    text(s, 1.0, 6.7, 11, 0.4,
         [[R("Basado en la documentación oficial (code.claude.com), el curso de hooks de Anthropic, "
             "GSD y CodeGraph.", 11, FAINT, False)]])

    # ---- 2. Agenda
    s = new()
    base(s, "Agenda", "Qué vamos a recorrer", page=2)
    agenda = [
        ("01", "Instalación y uso básico", "Instalar en una línea; interactivo vs headless (-p)"),
        ("02", "Memoria, instrucciones y sesiones", "CLAUDE.md de dos niveles, permisos, sesiones que viajan"),
        ("03", "MCP", "Conectar tus herramientas: scopes y servers reales"),
        ("04", "Plugins, tools y skills", "Las 4 capas de extensibilidad + subagentes"),
        ("05", "Automatización", "Hooks, CI, scheduling y Agent SDK"),
        ("06", "Metodología real", "Agente disciplinado · GSD · CodeGraph"),
    ]
    top = 2.05
    for i, (n, t, d) in enumerate(agenda):
        r, c = divmod(i, 2)
        x = 0.7 + c * 6.15
        y = top + r * 1.35
        rect(s, x, y, 5.85, 1.15, fill=PANEL, line=STROKE, rounded=True, radius=0.07)
        text(s, x + 0.28, y + 0.16, 1.2, 0.9, [[R(n, 30, CORAL, True)]], anchor=MSO_ANCHOR.MIDDLE)
        text(s, x + 1.35, y + 0.2, 4.3, 0.4, [[R(t, 15, TEXT, True)]])
        text(s, x + 1.35, y + 0.62, 4.35, 0.45, [[R(d, 11, MUTED, False)]], line_spacing=1.0)

    # ---- 3. Instalación
    s = new()
    base(s, "01 · Instalación y uso básico", "Instalar es una línea", page=3)
    cards(s, [
        ("1", "Native (recomendado)", "curl -fsSL https://claude.ai/install.sh | bash — macOS/Linux/WSL, con auto-update."),
        ("2", "Homebrew", "brew install --cask claude-code (brew upgrade para actualizar)."),
        ("3", "Windows", "winget install Anthropic.ClaudeCode · o el instalador PowerShell."),
        ("4", "Linux pkg", "apt / dnf / apk en Debian, Fedora, RHEL, Alpine."),
    ], top=2.05, cols=2, height=1.0)
    code(s, 0.7, 4.35, 5.9, 1.35,
         ["cd tu-proyecto", "claude            # login la 1ª vez"],
         title="Arrancar en cualquier proyecto")
    panel_bullets(s, 6.9, 4.01, 5.75, 1.7, "El mismo motor en todas partes",
                  ["Terminal · VS Code / Cursor · JetBrains", "Desktop (diffs, sesiones en paralelo)",
                   "Web (claude.ai/code, tareas largas)"], accent=BLUE)
    takeaway(s, "Instalar es trivial; el valor está en cómo lo usas.")

    # ---- 4. Los dos modos
    s = new()
    base(s, "01 · Instalación y uso básico", "Dos modos: interactivo y headless", page=4)
    panel_bullets(s, 0.7, 2.05, 5.85, 2.5, "Interactivo — pensar contigo",
                  ["Abres `claude` y conversas",
                   "Plan mode: propone un plan y tú lo apruebas antes de tocar nada",
                   "Ideal para explorar, diseñar, depurar"], accent=CORAL)
    panel_bullets(s, 6.8, 2.05, 5.85, 2.5, "Headless (-p) — componible",
                  ["Un prompt: entra por stdin, sale por stdout",
                   "Encaja en tuberías Unix y en CI",
                   "La base de toda la automatización"], accent=BLUE)
    code(s, 0.7, 5.05, 11.95, 1.1,
         ["tail -200 app.log | claude -p \"avísame si ves anomalías\"",
          "git diff main --name-only | claude -p \"revisa estos ficheros por seguridad\""],
         title="El mismo Claude, dos formas de invocarlo")

    # ---- 5. Memoria: CLAUDE.md dos niveles
    s = new()
    base(s, "02 · Memoria e instrucciones", "CLAUDE.md: el patrón de dos niveles", page=5)
    panel_bullets(s, 0.7, 2.05, 5.85, 3.0, "Nivel 1 — siempre cargado (pequeño)",
                  ["Orientación mínima: qué es el proyecto, mapa de repos, comandos",
                   "Solo PUNTEROS de una línea a todo lo demás",
                   "Es la onboarding de 30s del agente",
                   "Regla write-once: el core apunta, no copia"], accent=CORAL)
    panel_bullets(s, 6.8, 2.05, 5.85, 3.0, "Nivel 2 — bajo demanda (el detalle)",
                  ["data/changes/STATUS.md — estado vivo por ticket",
                   "PLAYBOOK.md — lecciones de debugging",
                   "SHARP_EDGES.md — invariantes 'no tocar'",
                   "<TICKET>/<TICKET>.md — ~55 ledgers autocontenidos"], accent=BLUE)
    takeaway(s, "Recortamos el CLAUDE.md ~73% sin perder información: punteros, no copias.")

    # ---- 6. Jerarquía + settings + auto-memory
    s = new()
    base(s, "02 · Instrucciones, permisos y auto-memory", "Jerarquía, permisos y memoria automática", page=6)
    code(s, 0.7, 2.15, 6.0, 2.2,
         ["~/.claude/CLAUDE.md      # global usuario",
          "<repo>/CLAUDE.md         # compartido (versionado)",
          "<repo>/sub/CLAUDE.md     # al entrar en la subcarpeta",
          "<repo>/CLAUDE.local.md   # personal, no versionado"],
         title="Jerarquía de CLAUDE.md (se combinan)")
    panel_bullets(s, 7.0, 1.82, 5.65, 2.55, "Permisos = allowlist específico",
                  ["settings.json: allow / deny / ask",
                   "Reglas concretas, no Bash(*)",
                   "mcp__serena__find_symbol, pytest exacto…",
                   "El humano es dueño de push/PR/deploy"], accent=GREEN)
    panel_bullets(s, 0.7, 4.55, 11.95, 1.55, "Auto-memory",
                  ["Claude guarda aprendizajes (comandos de build, pistas de debug) entre sesiones sin que escribas nada."],
                  accent=BLUE)

    # ---- 7. Sesiones
    s = new()
    base(s, "02 · Sesiones", "Sesiones que viajan entre superficies", page=7)
    cards(s, [
        ("→", "Teleport", "claude --teleport trae una sesión web/móvil al terminal."),
        ("↺", "Remote Control", "Sigue una sesión local desde el móvil o cualquier navegador."),
        ("▣", "Desktop handoff", "/desktop pasa la sesión al Desktop para revisar diffs."),
        ("⌁", "Channels / Slack", "Empuja eventos externos o convierte un bug de Slack en un PR."),
    ], top=2.15, cols=2, height=1.1)
    takeaway(s, "El mismo motor y los mismos CLAUDE.md/settings/MCP en todas las superficies.")

    # ---- 8. MCP
    s = new()
    base(s, "03 · MCP", "Model Context Protocol: conecta tu mundo", page=8)
    text(s, 0.7, 1.9, 11.95, 0.6,
         [[R("Estándar abierto para enchufar Claude a datos y tools externas. Las tools aparecen como ",
             12.5, MUTED, False), R("mcp__<server>__<tool>", 12.5, CORAL, True, MONO), R(".", 12.5, MUTED, False)]])
    cards(s, [
        ("L", "Scope local", ".claude/settings.local.json — solo tú, esta máquina."),
        ("P", "Scope project", ".mcp.json en la raíz, versionado, compartido con el equipo."),
        ("U", "Scope user", "~/.claude.json — todos tus proyectos."),
        ("★", "Servers que uso", "serena · context7 · playwright · codegraph · supabase."),
    ], top=2.55, cols=2, height=1.0)
    code(s, 0.7, 4.95, 11.95, 1.15,
         ["claude mcp add --transport http context7 https://mcp.context7.com/mcp",
          "claude mcp list      # estado      /mcp   # auth OAuth y tools dentro de la sesión"],
         title="Añadir un server")

    # ---- 9. Plugins, tools y skills
    s = new()
    base(s, "04 · Plugins, tools y skills", "Cuatro capas de extensibilidad", page=9)
    cards(s, [
        ("1", "Tools", "Lo que Claude puede hacer: Read/Edit/Bash/Grep/Task + mcp__*. Gobernadas por permisos."),
        ("2", "Slash commands", ".claude/commands/x.md = /x. El cuerpo es el prompt. Lo invocas tú."),
        ("3", "Skills", ".claude/skills/x/SKILL.md con description. Claude la auto-selecciona; lleva scripts/plantillas."),
        ("4", "Plugins + marketplace", "Agrupan skills+comandos+agentes+MCP+hooks. /plugin install. GSD es uno."),
    ], top=2.05, cols=2, height=1.15)
    takeaway(s, "Slash command = atajo que invocas tú. Skill = capacidad que Claude decide usar.")

    # ---- 10. Automatización: anatomía de un hook
    s = new()
    base(s, "05 · Automatización", "Hooks: el control determinista", page=10)
    panel_bullets(s, 0.7, 2.0, 5.85, 3.1, "El contrato de un hook",
                  ["Payload del evento por STDIN",
                   "Eventos: PreToolUse, PostToolUse, SessionStart, Stop…",
                   "Matcher = regex sobre el nombre de la tool",
                   "exit 0 permite · exit 2 BLOQUEA (stderr → Claude)",
                   "Pre = intención (tool_input) · Post = resultado (tool_response)"], accent=CORAL)
    code(s, 6.8, 2.35, 5.85, 2.4,
         ["if (payload.tool_input",
          "     ?.file_path?.includes(\".env\")) {",
          "  console.error(\"Bloqueado: no leas .env\");",
          "  process.exit(2);   // <-- veto",
          "}",
          "process.exit(0);"],
         title="Patrón de bloqueo (JS)")
    takeaway(s, "Con instrucciones le pides que se porte bien; con un hook lo garantizas.")

    # ---- 11. Automatización: cinco hooks + 4 niveles
    s = new()
    base(s, "05 · Automatización", "De hooks a agentes programados", page=11)
    cards(s, [
        ("a", "Hooks", "Seguridad (.env), formato (prettier), type-check bloqueante, 'IA revisando IA' vía SDK."),
        ("b", "Headless / piping", "claude -p en cualquier tubería Unix o script."),
        ("c", "CI/CD", "GitHub Actions · GitLab · GitHub Code Review sobre cada PR."),
        ("d", "Scheduling", "Routines (/schedule, infra Anthropic) · Desktop tasks · /loop."),
    ], top=2.05, cols=2, height=1.05)
    code(s, 0.7, 4.5, 11.95, 1.25,
         ["import { query } from \"@anthropic-ai/claude-agent-sdk\";",
          "for await (const m of query({ prompt, options: { allowedTools: [\"Edit\"] } }))",
          "  if (m.type === \"result\") console.log(m.result);"],
         title="Agent SDK — workflows a medida (menor privilegio)")

    # ---- 12. Metodología: principio
    s = new()
    base(s, "06 · Metodología real", "El agente es un colaborador disciplinado", page=12)
    rect(s, 0.7, 2.0, 11.95, 1.15, fill=PANEL_2, line=CORAL, lw=1.0, rounded=True, radius=0.06)
    text(s, 1.0, 2.18, 11.4, 0.85,
         [[R("“La autonomía se gana por-decisión, no se concede en bloque.”", 17, TEXT, True)]],
         anchor=MSO_ANCHOR.MIDDLE)
    panel_bullets(s, 0.7, 3.4, 5.85, 2.05, "El agente posee",
                  ["Investigación y diagnóstico", "Planes e implementación", "Tests y documentación"], accent=BLUE)
    panel_bullets(s, 6.8, 3.4, 5.85, 2.05, "El humano posee",
                  ["Decisiones go/no-go y el scope", "Toda acción externa: push, PR, deploy",
                   "La aprobación del plan"], accent=GREEN)
    takeaway(s, "El modelo no gana confianza gratis: la gana decisión a decisión, con evidencia.")

    # ---- 13. Metodología: el flujo de 11 etapas
    s = new()
    base(s, "06 · Metodología real", "El flujo real de 11 etapas", page=13)
    stages = [
        ("1", "Orientar: /kg + history-first + status-first", False),
        ("2", "Triaje inbound: ¿síntoma en el contrato?", True),
        ("3", "Regresión vs. pre-existente (probarlo)", True),
        ("4", "Investigar: oráculo determinista barato", False),
        ("5", "Plan → acuerdo humano explícito", True),
        ("6", "Implementar: TDD RED → GREEN, mínimo", False),
        ("7", "Verificar + gate outbound (contrato)", True),
        ("8", "Documentar — cada cosa una vez", False),
        ("9", "Sanitizar — líneas añadidas", False),
        ("10", "Handoff: el humano hace push / PR", False),
        ("11", "Revisión bot + persistir lecciones", True),
    ]
    for i, (n, label, gate) in enumerate(stages):
        col = i // 6
        row = i % 6
        x = 0.7 + col * 6.15
        y = 2.05 + row * 0.66
        acc = CORAL if gate else PANEL_2
        rect(s, x, y, 5.85, 0.56, fill=PANEL, line=(CORAL if gate else STROKE),
             lw=(1.0 if gate else 0.75), rounded=True, radius=0.14)
        rect(s, x + 0.14, y + 0.11, 0.34, 0.34, fill=acc, rounded=True, radius=0.4)
        text(s, x + 0.14, y + 0.11, 0.34, 0.34,
             [[R(n, 11, BG if gate else TEXT, True)]], align=PP_ALIGN.CENTER, anchor=MSO_ANCHOR.MIDDLE)
        text(s, x + 0.62, y + 0.06, 5.1, 0.46, [[R(label, 11.5, TEXT, False)]], anchor=MSO_ANCHOR.MIDDLE)
    text(s, 0.7, 6.02, 11.95, 0.3,
         [[R("■ ", 11, CORAL, True), R("Los recuadros coral son GATES (puntos de decisión). "
           "Un gate rojo = STOP: no escribir código.", 11, MUTED, False)]])
    takeaway(s, "Ninguna etapa dice 'pídele al LLM que lo arregle': la potencia se canaliza por gates.")

    # ---- 14. Metodología: prevalencia de tools
    s = new()
    base(s, "06 · Metodología real", "Qué herramienta usa Claude, y cuándo", page=14)
    text(s, 0.7, 1.9, 11.95, 0.5,
         [[R("Regla del CLAUDE.md: ", 12, MUTED, False),
           R("codegraph_explore PRIMERO (survey en 1 llamada) · Serena find_referencing_symbols "
             "para el chequeo preciso antes de renombrar. ", 12, TEXT, True),
           R("Orden: barato → caro, determinista → probabilístico.", 12, MUTED, False)]])
    rows = [
        ("Orientar", "/kg (grafo de tickets → zona de peligro) · STATUS.md · git · gh", "coste 0"),
        ("Navegar (survey)", "CodeGraph codegraph_explore — fuente + rutas + blast radius + cobertura", "1 llamada"),
        ("Refactor-check", "Serena find_referencing_symbols — desambigua por clase (antes de renombrar)", "preciso"),
        ("Diagnosticar", "Oráculo determinista: parser / validador / _diag_*.py", "coste 0"),
        ("Entorno (logs, config)", "AWS CLI — CloudWatch · lambda get-function · SQS/DLQ", "read-only"),
        ("Contrato de salida", "Playwright / F12 sobre el endpoint que ve el consumidor", "reproducir"),
        ("Solo al final", "La tirada del LLM — para VERIFICAR el fix, no para diagnosticar", "metered"),
    ]
    y0 = 2.5
    for i, (etapa, tool, tag) in enumerate(rows):
        y = y0 + i * 0.6
        last = (i == len(rows) - 1)
        rect(s, 0.7, y, 11.95, 0.5, fill=(PANEL_2 if last else PANEL),
             line=(CORAL if last else STROKE), lw=(1.0 if last else 0.75), rounded=True, radius=0.12)
        text(s, 0.95, y + 0.05, 2.9, 0.4, [[R(etapa, 11.5, (CORAL if last else BLUE), True)]],
             anchor=MSO_ANCHOR.MIDDLE)
        text(s, 3.95, y + 0.05, 7.0, 0.4, [[R(tool, 11.5, TEXT, False)]], anchor=MSO_ANCHOR.MIDDLE)
        text(s, 11.1, y + 0.05, 1.4, 0.4, [[R(tag, 9.5, MUTED, False)]],
             align=PP_ALIGN.RIGHT, anchor=MSO_ANCHOR.MIDDLE)

    # ---- 15. Metodología: un ejemplo real
    s = new()
    base(s, "06 · Metodología real", "Un ejemplo real, de principio a fin", page=15)
    rect(s, 0.7, 1.95, 11.95, 0.62, fill=PANEL_2, line=CORAL, rounded=True, radius=0.1)
    text(s, 0.95, 2.0, 11.5, 0.52,
         [[R("Bug QA: ", 12.5, CORAL, True),
           R("“un campo sale vacío en la UI, pero está escrito en el PDF.”", 12.5, TEXT, False)]],
         anchor=MSO_ANCHOR.MIDDLE)
    steps = [
        ("Orientar", "/kg saca la zona de peligro (un SHARP_EDGE que restringe el fix); git/gh dan la base."),
        ("Contrato", "El campo está vacío en el JSON del endpoint (Playwright/F12) → el Lambda es responsable."),
        ("Provenance", "Re-extraer en la base previa: ya salía vacío → pre-existente, no regresión."),
        ("Investigar", "Serena + CodeGraph localizan el detector; un _diag_pdf.py determinista da la causa: SIN LLM."),
        ("Fix + verificar", "Test RED → fix por propiedad estructural (no cliente) → regresión byte-idéntica + contrato local."),
        ("Handoff", "Sanitizar → el humano hace push/PR. Un bot detecta un caso más → test + PLAYBOOK."),
    ]
    for i, (tag, desc) in enumerate(steps):
        y = 2.78 + i * 0.56
        rect(s, 0.7, y, 11.95, 0.48, fill=PANEL, line=STROKE, rounded=True, radius=0.12)
        rect(s, 0.7, y, 0.08, 0.48, fill=CORAL, rounded=True, radius=0.5)
        text(s, 0.95, y + 0.04, 2.4, 0.4, [[R(tag, 11.5, BLUE, True)]], anchor=MSO_ANCHOR.MIDDLE)
        text(s, 3.5, y + 0.04, 9.0, 0.4, [[R(desc, 11, TEXT, False)]], anchor=MSO_ANCHOR.MIDDLE)
    takeaway(s, "El modelo no gana confianza gratis: la gana decisión a decisión, con evidencia.")

    # ---- 16. Metodología: un runbook de ops (sincronizar máquinas)
    s = new()
    base(s, "06 · Metodología real", "Un runbook real: sincronizar máquinas", page=16)
    panel_bullets(s, 0.7, 2.0, 5.85, 2.6, "Outbound — copia completa",
                  ["Un tarball: workspace + ~/.claude · .aws · .ssh",
                   "-h dereferencia el symlink de .aws (crítico)",
                   "Excluye venvs / node_modules / caches / .codegraph",
                   "En destino: bootstrap (/kg) + target-setup.sh rehacen el tooling"], accent=BLUE)
    panel_bullets(s, 6.8, 2.0, 5.85, 2.6, "Inbound — solo delta",
                  ["El código ya está en GitHub → git fetch",
                   "Docs gitignored de data/ + memoria (snapshot-memory) viajan",
                   "En la principal: restore-memory → /kg-refresh reconstruye",
                   "backup + diff de STATUS.md; STOP si hubo ediciones propias"], accent=GREEN)
    panel_bullets(s, 0.7, 4.75, 11.95, 1.4, "El landing lo conduce un agente — con guardrails",
                  ["Solo no-destructivo (renombrar, no borrar) · git fetch = única op de red",
                   "El humano hace push / merge; el agente prepara y reporta con evidencia (conteos, PRs)"],
                  accent=CORAL)
    takeaway(s, "La metodología no es solo para código: memoria durable, guardrails y 'el humano hace lo externo' también en ops.")

    # ---- 17. GSD — el método hecho tooling
    s = new()
    base(s, "06 · Herramientas", "GSD: la metodología hecha tooling", page=17)
    code(s, 0.7, 2.2, 6.15, 3.2,
         ["/gsd-new-project  -> PROJECT.md + ROADMAP.md",
          "/gsd-plan-phase   -> PLAN.md  (+ gate",
          "                     gsd-plan-checker)",
          "/gsd-execute-phase-> olas paralelas,",
          "                     commits atómicos",
          "/gsd-verify-work  -> VERIFICATION.md",
          "",
          "/gsd-progress     # qué toca ahora"],
         title="Ciclo por fases, estado versionado en .planning/")
    panel_bullets(s, 7.1, 1.86, 5.55, 3.55, "Subagentes especializados",
                  ["gsd-planner — desglose + dependencias",
                   "gsd-plan-checker — ¿logrará el objetivo? (goal-backward)",
                   "gsd-executor — commits atómicos, checkpoints",
                   "gsd-code-reviewer — REVIEW.md por severidad",
                   "gsd-verifier — verifica el OBJETIVO, no solo tareas"], accent=CORAL)
    takeaway(s, "GSD automatiza los gates que la metodología aplica a mano: plan, verificación, rastro durable.")

    # ---- 17. CodeGraph — inteligencia de código local
    s = new()
    base(s, "06 · Herramientas", "CodeGraph: inteligencia de código local", page=18)
    panel_bullets(s, 0.7, 2.0, 5.85, 2.4, "Índice tree-sitter → SQLite (.codegraph/)",
                  ["Símbolos: funciones, clases, rutas, componentes",
                   "Aristas: llamadas, imports, herencia, referencias",
                   "Determinista (del AST), sin API keys",
                   "Devuelve: fuente + rutas + blast radius + cobertura"], accent=BLUE)
    code(s, 6.8, 2.2, 5.85, 1.7,
         ["codegraph init      # crea .codegraph/",
          "codegraph sync      # incremental tras editar",
          "codegraph explore \"<símbolo|pregunta>\"",
          "codegraph serve --path <repo> --mcp"],
         title="CLI  (install --location=global escribe el MCP)")
    rect(s, 6.8, 4.15, 5.85, 1.2, fill=PANEL, line=STROKE, rounded=True, radius=0.06)
    text(s, 7.05, 4.28, 5.4, 1.05,
         [[R("Primero para navegar:  ", 11, CORAL, True),
           R("fuente + callers + blast radius + cobertura en 1 consulta (trátala como YA leída). "
             "Serena find_referencing_symbols = chequeo preciso (desambigua por clase). "
             "--path fija el repo por defecto.", 11, TEXT, False)]], line_spacing=1.03)
    text(s, 0.7, 4.6, 5.85, 1.4,
         [[R("58% menos tool calls · 22% más rápido", 13, GREEN, True)],
          [R("(según sus benchmarks: casi elimina las lecturas de fichero)", 10.5, MUTED, False)]],
         space_after=4)
    takeaway(s, "Una consulta en vez de grep→abrir→seguir-import→repetir. Menos contexto, más señal.")

    # ---- 19. Grafo de conocimiento de tickets — CodeGraph para tickets/lecciones
    s = new()
    base(s, "06 · Herramientas", "Grafo de tickets: CodeGraph, pero para tickets", page=19)
    panel_bullets(s, 0.7, 2.0, 5.85, 2.4, "Grafo sobre los .md del proyecto (data/, interno)",
                  ["Nodos: tickets + símbolos + invariantes + lecciones",
                   "Aristas tipadas: references / supersedes / relacionado",
                   "Comunidades = zonas de peligro (fin-de-carta, títulos…)",
                   "Determinista, sin LLM en la consulta (lee graph.json)"], accent=BLUE)
    code(s, 6.8, 2.2, 5.85, 1.9,
         ["/kg <ticket|tema>   # vecinos  (explain)",
          "/kg <A> <B>         # camino    (path)",
          "/kg find <substr>   # nombre de nodo",
          "/kg-refresh         # reconstruir el grafo"],
         title="Skill /kg  (envuelve graphify explain/path)")
    rect(s, 6.8, 4.28, 5.85, 1.12, fill=PANEL, line=STROKE, rounded=True, radius=0.06)
    text(s, 7.05, 4.4, 5.4, 0.95,
         [[R("Primero la historia:  ", 11, CORAL, True),
           R("corre /kg <ticket|tema> ANTES de grep — saca los tickets relacionados + la zona de "
             "peligro a leer. Apunta a qué leer, no lo sustituye.", 11, TEXT, False)]], line_spacing=1.03)
    text(s, 0.7, 4.6, 5.85, 1.4,
         [[R("Reconstruible · consultable en 1 llamada", 13, GREEN, True)],
          [R("(enganchado a la regla history-first del CLAUDE.md)", 10.5, MUTED, False)]],
         space_after=4)
    takeaway(s, "El grafo es el mapa; el agente, el guía. Recall de zonas de peligro que si no tendrías que recordar.")

    # ---- 20. Cierre
    s = new()
    base(s, "Cierre", "De asistente a sistema", page=20)
    cards(s, [
        ("1", "Instalar", "Una línea; interactivo para pensar, -p para automatizar."),
        ("2", "Memoria & sesiones", "Contexto lean de dos niveles; sesiones que viajan."),
        ("3", "MCP", "Conecta tus datos, docs, navegador y tooling."),
        ("4", "Skills & plugins", "Empaqueta y distribuye flujos repetibles."),
        ("5", "Automatización", "Hooks que garantizan calidad; CI; scheduling; SDK."),
        ("6", "Metodología", "Agente disciplinado: 11 etapas, gates, tools reales."),
    ], top=1.95, cols=2, height=0.92)
    text(s, 0.7, 6.7, 12, 0.4,
         [[R("Referencias:  code.claude.com/docs  ·  github.com/tomascortereal/claude-code-setup  ·  "
             "colbymchenry.github.io/codegraph", 11, FAINT, False)]])

    out = os.path.join(os.path.dirname(os.path.abspath(__file__)), "Claude_Code_Presentacion.pptx")
    prs.save(out)
    print(f"OK  ->  {out}  ({len(prs.slides._sldIdLst)} slides)")
    return out


if __name__ == "__main__":
    build()
