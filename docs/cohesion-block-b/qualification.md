# First installed family qualification

The first source milestone provides individual model definitions, bounded
harness execution, a Carets application, deterministic world rules and
application-owned terminal generation. The complete plan and owning Project
remain the execution queue for later tools, context, persistence, providers,
training, optimization, design-system and hub work.

## Reproduce the selected sources

The immutable [source register](sources-v1.json) selects seven independently
versioned components. Install the optional Python 3.14+ family profile with
`uv sync --extra family`, or build this reference and run:

```sh
uv build --out-dir dist
python scripts/qualify_family.py dist
```

The script installs both wheel and source artifacts in independent temporary
environments outside all source trees. It verifies every component's PEP 610
Git commit against the register, runs the real tiny Transformer path and world
checks, installs a freshly generated terminal app, runs its module and console
commands, checks dependencies and records artifact SHA-256/version/source data
in `family-qualification.json`. CI retains that receipt for each platform.

## Qualified behavior

- Thoughtformula's real ModernMicroGPT/BPETokenizer is consumed through the
  explicit Thoughtform adapter. The same model produces equivalent headless
  Hypnosis and Carets output under deterministic sampling. A tiny random model
  proves integration only, without claiming trained language/coding ability.
- Hypnosis sources run under byte/event/time budgets and managed cleanup.
  Package tests exercise explicit outcomes, errors, cancellation, bounded safe
  display, actual CLI stdio and worker-thread closure. Thread cancellation is
  cooperative at token boundaries, not forced interruption.
- A Paracosm world composes Thoughtform beings. Deterministic policies observe
  one snapshot, and invalid habitat authority preserves authoritative state.
  Package tests cover stable order, movement and atomic rejected steps.
- Compose Application generates owned Expose Interface/Carets source with
  immutable independent library selection. The reference installs outside the
  checkout and both real entry points verify model/renderer completion.
- On POSIX, an actual Hypnosis process reads q through a pseudo-terminal and
  restores original terminal attributes. The test sets terminal dimensions and
  an ANSI-capable TERM explicitly; Darwin's transient PENDIN bit is excluded
  consistently with Carets's existing terminal qualification.

CI runs installed profiles on Linux, macOS and Windows. Windows runs headless
checks and explicitly skips the native POSIX test; it does not claim native
Windows console support. Carets keeps its Python 3.10 floor and its independent
source/wheel/native regressions. The new family requires Python 3.14+.

## Boundaries and next decisions

Managed in-process messages are implemented. The selected JSONL contract remains
a wire-format decision; [JSONL-02](https://github.com/wispsy/wispsy/issues/28)
requires actual producer/consumer process proof before a command claims transport
support. Existing commands emit one JSON result.

No autonomous tool execution, Ollama provider, durable job/memory store, trained
model, specialization pipeline, adaptive search or persistent world is claimed
by this milestone. Their owning issues select existing Hidden Moves, Requ,
Backpack and Moveset/func_seq/Scriptty interfaces. Choose the first real model or
checkpoint, task/workspace capability profile and hardware budget before moving
from synthetic integration to a useful coding harness. Real training also needs
dataset/license/split/destination selection. Warewolf follows a concrete two-app
embedding contract and reusable Carets shell evidence.

Public source repositories and source PRs are complete implementation artifacts.
Package/model publication, paid providers and deployment remain separate choices.
