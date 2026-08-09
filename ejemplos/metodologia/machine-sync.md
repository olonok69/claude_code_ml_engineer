# Un runbook real: sincronizar el workspace entre máquinas

> **Nota de estado (actualizado).** Este runbook de tarball + USB sigue siendo válido y es
> el camino para un **bring-up completo** de una máquina nueva. Pero ya **no** es la forma
> de mantener sincronizado el registro de ingeniería del día a día: eso pasó a
> **almacenamiento compartido (S3)**. Salta a
> [§ Evolución: del tarball al almacenamiento compartido](#evolución-del-tarball-al-almacenamiento-compartido)
> al final para ver qué cambió y por qué. Lo de abajo se lee igual: los principios que
> ilustra (contexto lean, ops con guardrails, "descubre, no asumas") no cambiaron.
>
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
dir real, si `~/.gnupg` existe, la lista de repos, tamaño del último tar) — con un "confirmar antes de
confiar". Deriva con el tiempo: la lista de repos **crece** (un repo nuevo se sumó sin tocar el comando,
porque el `-C` toma el directorio entero), y el tamaño del tar también. Re-verifícala en cada viaje.

## Outbound — copia completa (comando real, sanitizado)

Tres correcciones nacidas de fallos reales están integradas: `-C` correcto, `-h` para **dereferenciar el
symlink de `.aws`** (si no, el portátil queda con un link muerto y el AWS CLI sin configurar), y omitir
`.gnupg` si no existe (si no, `tar` da error):

```bash
WS=$(ls -d /mnt/*/ILS 2>/dev/null | head -1)
STAMP=$(date +%Y%m%d)

tar -czhf ~/ils-migration-$STAMP.tar.gz \
  --exclude='*/node_modules' --exclude='*/.codegraph' \
  --exclude='*/.venv' --exclude='*/.venv-win' \
  --exclude='*/__pycache__' --exclude='*/.pytest_cache' \
  --exclude='*/.ruff_cache' --exclude='*/.mypy_cache' --exclude='*.pyc' \
  -C "$(dirname "$WS")" "$(basename "$WS")" \
  -C /home/$USER .claude .aws .ssh
ls -lh ~/ils-migration-$STAMP.tar.gz   # se espera ~1 GB+ (crece); si son KB, el -C estaba mal
```

**Copiar al USB — gotchas reales (de un viaje):**

- **WSL no auto-monta un USB.** Un USB que conectas *después* de arrancar WSL no aparece solo en
  `/mnt/<letra>` (el punto de montaje existe pero vacío). Hay que montarlo a mano:
  ```bash
  sudo mount -t drvfs F: /mnt/f    # sustituye por la letra real del USB en Windows
  ```
- **Verifica byte a byte antes de expulsar.** El mount es 9p (lento); tras `cp`, `sync` y compara tamaños
  exactos —nada de "parece que cabe":
  ```bash
  cp ~/ils-migration-$STAMP.tar.gz /mnt/f/ && sync
  stat -c %s ~/ils-migration-$STAMP.tar.gz /mnt/f/ils-migration-$STAMP.tar.gz   # deben coincidir
  ```
- **Dimensiona el USB al alza.** El bundle **crece** al sumarse repos (excluyendo venvs/caches: ~0.9 GB →
  ~1.5 GB en unas semanas). Un USB de 4 GB cabe *un* bundle, sin margen para dos.
- **Guarda un tar completo previo** como red de seguridad antes de cualquier extracción en destino.

En el portátil: **parquear** (renombrar, no borrar) cualquier workspace previo, extraer, y **recrear los
pesados excluidos** (`python -m venv`, `npm install`) por repo que vayas a ejecutar. El **binario** del
AWS CLI **no** va en el bundle (es una instalación de sistema) — se reinstala en el destino y se hace
`aws sso login` una vez (el token cacheado viaja caducado). Lo mismo con el **tooling de navegación**: el
índice `.codegraph/` se excluye (rutas absolutas, machine-local) y un `target-setup.sh` idempotente
reinstala el CLI de CodeGraph, actualiza GSD si va atrasado, **corrige el `--path` del MCP** a la raíz real
del portátil y reconstruye el índice (`codegraph init`).

## Inbound — solo delta (el retorno)

No se hace copia completa de vuelta: machacaría lo que la máquina principal hiciera mientras tanto.

1. **Código** → PRs normales desde el portátil; en la principal, solo `git fetch origin` (read-only).
2. **Docs de `data/` gitignored** → el único físico que viaja; se empaqueta desde la raíz del repo
   (paths repo-relativos) y se le acompaña un `INSTRUCTIONS.md` + `MANIFEST.txt`.

## Dos huecos que cierran unos subcomandos (bring-up + memoria)

Un caso real: el workspace lleva un **grafo de conocimiento de tickets** (skill `/kg`, ver
[`../../docs/KNOWLEDGE_GRAPH.md`](../../docs/KNOWLEDGE_GRAPH.md)). Al viajar aparecen dos huecos que se
resuelven con subcomandos idempotentes, no con pasos manuales fáciles de olvidar:

- **Bring-up desde cero (portátil nuevo).** El bundle trae el grafo ya construido, los skills y la memoria,
  pero **no** el paquete `graphify` ni un intérprete correcto. Un comando lo arregla:
  ```bash
  bash data/knowledge-graph/kg_refresh.sh bootstrap   # instala el paquete, fija el intérprete, smoke-test /kg
  ```
- **La memoria no viaja en el delta.** El inbound excluye `~/.claude` (es machine-local), así que las notas
  de memoria que escribiste en el portátil **no volverían**. Modelo *transporte-y-restaura* (mantiene
  `~/.claude/…/memory` como única fuente de verdad, no un snapshot que la pise en silencio):
  ```bash
  # En el PORTÁTIL, antes de armar el delta: parquear la memoria BAJO data/ para que viaje
  bash data/knowledge-graph/kg_refresh.sh snapshot-memory     # memory/*.md -> data/…/_memory_snapshot/
  # En la PRINCIPAL, tras aterrizar el delta: fusionar de vuelta (añade nuevos, sobrescribe
  # cambiados TRAS backup; idénticos = no-op) y reconstruir el grafo
  bash data/knowledge-graph/kg_refresh.sh restore-memory  &&  /kg-refresh
  ```

Para el **agente del portátil** (que trabaja con su propia sesión de Claude), un único punto de entrada
—`LAPTOP_START_HERE.md`— orquesta: restaurar el bundle → `bootstrap` → cómo seguir trabajando igual (skills,
`CLAUDE.md`, `/kg` history-first) → cómo mandar el incremento de vuelta. El grafo es un artefacto **derivado**:
nunca viaja de vuelta; se reconstruye donde esté el corpus actual.

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

## Evolución: del tarball al almacenamiento compartido

El runbook de arriba resuelve **transporte** entre dos máquinas tuyas. No resuelve
**compartir**. En cuanto aparecen una tercera máquina y una segunda persona, tres
costes se vuelven evidentes:

- El registro vive en un directorio gitignored → **no se puede enlazar** desde un
  ticket, un PR ni un documento de aceptación: la ruta solo resuelve en tu máquina.
- Moverse entre máquinas degenera en *empaquetar todo y copiarlo*: lento, fácil de
  olvidar y silenciosamente incompleto.
- Cada compañero se construye su **propio índice privado** de la misma historia
  supuestamente compartida. El "registro único durable" deja de existir en cuanto
  hay dos personas.

La respuesta es poner el registro en **almacenamiento de objetos compartido**, con un
modelo de operación. El modelo importa más que la tecnología:

| Regla | Por qué |
|---|---|
| **Alcance estrecho**: solo `changes/**/*.md` + el grafo | Confidencialidad y tamaño. Ensanchar después es fácil; retraer, no. |
| **Escribe por sync, lee por mount de solo lectura** | El almacenamiento de objetos **no** tiene locking ni rename atómico. Un mount escribible invita a corrupción que aparece semanas después. |
| **Dry-run por defecto**, `--go` explícito; `--delete` aparte | El caso normal es que un compañero esté empujando a la vez; un espejo exacto desde una vista local vieja **borra su trabajo**. |
| **Los docs son la fuente de verdad; el grafo es derivado** | Los ficheros por ticket casi nunca chocan. El grafo generado es el **único** punto real de contención → o se reconstruye en local, o lo publica **una** máquina. |
| **Cada máquina declara su identidad** | Ver abajo: es lo específico de trabajar con agentes. |

### Lo específico de los agentes: la máquina tiene rol

Este detalle solo aparece cuando el mismo registro es alcanzable desde varias máquinas
con **permisos distintos**, y es el más fácil de pasar por alto: una sesión de Claude
tiene que saber **en qué máquina está y qué le está permitido** *antes* de actuar. Si
no, una máquina *contributor* reconstruirá y republicará el grafo compartido —
exactamente lo único que no debe hacer— y encima lo reportará como trabajo bien hecho.

La solución es pequeña: cada máquina declara `MACHINE_NAME` y `MACHINE_ROLE` en su
config, se genera un `IDENTITY.md` **machine-local** (con comprobaciones en vivo: qué
cuenta está autenticada, si el bucket responde, si el mount está montado), y el
`CLAUDE.md` del repo **apunta a él**, así que toda sesión lee su propio rol primero.
`IDENTITY.md` es el único fichero que **no** debe ser igual en todas partes: gitignored,
nunca sincronizado, nunca empaquetado.

> Runbook completo y sanitizado (modos de acceso, roles, orden de bring-up, checklist
> previa al primer push): [`../../docs/synchro/s3-sync/README.md`](../../docs/synchro/s3-sync/README.md).
> El principio genérico, sin herramientas:
> [`../../docs/ai-agents-code-methodology/TECHNICAL.md`](../../docs/ai-agents-code-methodology/TECHNICAL.md) §7.

### Qué sigue valiendo del tarball

El bring-up completo de una máquina nueva. El almacenamiento compartido trae los
**docs y el grafo**; no trae el workspace, ni `~/.claude`, ni los venvs, ni el índice
de navegación. Para eso el bundle + `target-setup.sh` de arriba sigue siendo el
camino — y los guardrails del aterrizaje conducido por agente (no-destructivo, sin
escrituras a remoto, backup antes de sobrescribir, STOP ante ambigüedad) se aplican
igual.
