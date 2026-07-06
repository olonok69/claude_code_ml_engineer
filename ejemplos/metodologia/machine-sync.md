# Un runbook real: sincronizar el workspace entre máquinas

> Procedimiento real (sanitizado) para mover el workspace ILS entre la **máquina principal** y un
> **portátil** (viajes). Es un buen ejemplo de tres cosas de la metodología a la vez:
> **memoria durable cargada bajo demanda**, **ops conducidas por el agente con guardrails**, y
> **"descubre, no asumas"**. Vive en `data/` (gitignored) — es contenido de máquina/ops, nunca se
> commitea.
>
> En el `CLAUDE.md` no está el runbook entero: hay un **puntero de una línea** ("¿mover el workspace
> main ⇄ portátil? carga `data/machine-sync/RUNBOOK.md`"). Se carga **solo cuando hace falta**. Es la
> disciplina de contexto lean en acción.

## La idea: sincronización asimétrica

| Dirección | Estrategia | Por qué |
|---|---|---|
| **Outbound** (principal → portátil, antes de viajar) | **COPIA COMPLETA** | Un tarball lleva todo el workspace + config de home; el portátil arranca desde un estado idéntico y limpio. |
| **Inbound** (portátil → principal, a la vuelta) | **SOLO DELTA** | El código ya está en GitHub → se trae con `git fetch`. Solo los docs gitignored de `data/` (unos MB) viajan en un tarball pequeño. |

Medio de transferencia: **USB** (monta en WSL como `/mnt/<letra>`). Un USB FAT32 no preserva
permisos/symlinks de Linux — da igual: todo va dentro del `.tar.gz`, que los preserva internamente.

## Principio transversal: "descubre, no asumas"

Las rutas y el layout de dotfiles **difieren por máquina**. Los comandos **derivan** la raíz del
workspace en vez de hardcodearla:

```bash
WS=$(ls -d /mnt/*/ILS 2>/dev/null | head -1)   # deriva la raíz, no la asume
echo "workspace: $WS"
# Re-chequea los "machine facts" cuando pase tiempo (drift):
ls -ld /home/$USER/.aws /home/$USER/.gnupg /home/$USER/.ssh /home/$USER/.claude
```

Una **tabla de "machine facts"** documenta lo que varía (raíz del workspace, si `~/.aws` es symlink o
dir real, si `~/.gnupg` existe, tamaño del último tar) — con un "confirmar antes de confiar".

## Outbound — copia completa (comando real, sanitizado)

Tres correcciones nacidas de fallos reales están integradas: `-C` correcto, `-h` para **dereferenciar el
symlink de `.aws`** (si no, el portátil queda con un link muerto y el AWS CLI sin configurar), y omitir
`.gnupg` si no existe (si no, `tar` da error):

```bash
WS=$(ls -d /mnt/*/ILS 2>/dev/null | head -1)
STAMP=$(date +%Y%m%d)

tar -czhf ~/ils-migration-$STAMP.tar.gz \
  --exclude='*/node_modules' \
  --exclude='*/.venv' --exclude='*/.venv-win' \
  --exclude='*/__pycache__' --exclude='*/.pytest_cache' \
  --exclude='*/.ruff_cache' --exclude='*/.mypy_cache' --exclude='*.pyc' \
  -C "$(dirname "$WS")" "$(basename "$WS")" \
  -C /home/$USER .claude .aws .ssh
ls -lh ~/ils-migration-$STAMP.tar.gz   # se esperan cientos de MB; si son KB, el -C estaba mal
```

En el portátil: **parquear** (renombrar, no borrar) cualquier workspace previo, extraer, y **recrear los
pesados excluidos** (`python -m venv`, `npm install`) por repo que vayas a ejecutar. El **binario** del
AWS CLI **no** va en el bundle (es una instalación de sistema) — se reinstala en el destino y se hace
`aws sso login` una vez (el token cacheado viaja caducado).

## Inbound — solo delta (el retorno)

No se hace copia completa de vuelta: machacaría lo que la máquina principal hiciera mientras tanto.

1. **Código** → PRs normales desde el portátil; en la principal, solo `git fetch origin` (read-only).
2. **Docs de `data/` gitignored** → el único físico que viaja; se empaqueta desde la raíz del repo
   (paths repo-relativos) y se le acompaña un `INSTRUCTIONS.md` + `MANIFEST.txt`.

## El landing lo conduce un agente — con guardrails

El `INSTRUCTIONS.md` del delta está escrito **para un agente de coding** en la máquina principal. Su único
trabajo es **aterrizar el delta de forma segura**, no implementar nada. Extractos (sanitizados):

> *"Eres un agente en la máquina PRINCIPAL. Tu ÚNICO trabajo es aterrizar este delta con seguridad. NO
> estás implementando features, NI mergeando PRs, NI haciendo push."*

Guardrails obligatorios:

- **Solo no-destructivo.** Nada de `rm -rf`/reset/overwrite salvo lo especificado. **Nunca dos operaciones
  de movimiento de ficheros a la vez** en un mount Windows `/mnt/c|d` (una sesión previa perdió un
  workspace por un `rm`/`chmod` concurrente ahí).
- **Sin escrituras git a remoto.** Ni commit/push/merge/PR. `git fetch` (read-only) es la única op de red.
- **Backup antes de sobrescribir.** El único fichero que el delta puede pisar es `STATUS.md`: copiar a
  `STATUS.md.mainbak` **primero**, luego `diff`.
- **STOP y pregunta** si se cumple una "condición STOP" (p. ej. el `diff` revela que la máquina principal
  hizo sus **propias** ediciones a `STATUS.md` → no estaba dormida → no machacar; restaurar y preguntar).
- **Descubrir paths** (Step 0): `find … -name document-parser-lambda`, no asumir la ruta.
- **Verificar y reportar**: contar ficheros esperados, estados de PR, y resumir sin haber hecho ningún
  commit/push.

```bash
# Reconciliación de STATUS.md — con juicio, no ciega:
cp data/changes/STATUS.md data/changes/STATUS.md.mainbak   # backup PRIMERO
tar -xzf "$TARBALL" -C "$REPO"                             # paths relativos a la raíz del repo
diff data/changes/STATUS.md.mainbak data/changes/STATUS.md # ¿solo adiciones? -> quedarse la nueva
#                                                            ¿la principal tenía ediciones propias? -> STOP
```

## Por qué es un buen ejemplo para la charla

Reúne los principios de la metodología en una tarea de **ops**, no de código:

- **Memoria durable, bajo demanda:** el runbook no está en el `CLAUDE.md` always-loaded; hay un puntero.
- **El humano es dueño de lo externo:** el agente aterriza el delta pero **no** hace push/merge; y para si
  hay ambigüedad.
- **Evidencia antes que afirmaciones:** contar ficheros, `diff`, estados de PR — reportar hechos.
- **No-destructivo + "descubre, no asumas":** renombrar en vez de borrar; derivar rutas.

> Detalle completo (todos los pasos, la tabla de machine-facts, los gotchas de `hash -r` y del shadowing
> del CLI) en el `RUNBOOK.md` original del proyecto. Aquí va lo reutilizable y sanitizado.
