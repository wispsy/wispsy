# Optional lifecycle reference

Python 3.14+ is required for func_seq. The ordinary reference and Hidden Moves
workflow profile remain Python 3.11+. Install this profile explicitly:

```sh
uv sync --locked --extra sequence
uv run python -m wispsy.sequence ' Hello WORLD ' --checkpoint reference.progress.json --pace function
uv run python -m wispsy.sequence ' Hello WORLD ' --checkpoint reference.progress.json
```

The first invocation completes normalization and pauses before the report. The
second invocation builds the same trusted definition in a new process, retains
the completed output and finishes the report. Further ordinary invocations return
completed results without executing either step again. Keep the input text and
definition version the same when resuming.

```python
from wispsy.sequence import build_script

script = build_script(" Hello WORLD ")
paused = script.run(checkpoint="reference.progress.json", pace="function")
completed = script.run(checkpoint="reference.progress.json")
assert completed.results["report"]["text"] == "hello world"
```

`build_script` installs no handlers and opens no files. It maps exactly two
synchronous selected catalog calls to `func_seq.Script` with explicit step IDs
and a backward JSON result reference. Func_seq owns execution, pause, checkpoint
validation, atomic writes, concurrency ownership, resume and uncertainty.
This proof is deliberately small; it is not a general pipeline compiler.
Asynchronous catalog capabilities are rejected during construction; general
mixed sync/async compilation belongs to the later moveset adapter.

The optional dependency uses an interpreter marker because package extras cannot
declare a separate package Python floor. Selecting the extra on an older Python
does not make lifecycle supported: the sequence module explicitly rejects that
interpreter, and qualification refuses the profile below 3.14.

## Definition identity and recovery

The source profile pins Hidden Moves and func_seq to immutable revisions in
`pyproject.toml` and `uv.lock`. The default definition version is
`text-reference-v1`. Change it whenever the functions, captured catalog state,
defaults or relevant environment configuration change. Wrappers have stable
module/qualified names; the executor's manifest cannot detect changes inside
their closures. A future general compiler needs an adopted mapping/catalog
identity contract rather than relying on callable names alone.

Checkpoint state is passive JSON; loading it does not reconstruct Python code.
Func_seq validates its definition fingerprint before invoking an operation.
An input or version mismatch fails instead of silently starting again.
Checkpoint files contain selected inputs/results and belong in caller-controlled
storage; the reference has no automatic storage discovery.

An uncertain step raises `RecoveryRequiredError` on ordinary resume. Inspect its
effects, then explicitly select `--retry` to repeat that step or `--restart` to
repeat the whole workflow. These options delegate directly to func_seq. They
provide neither rollback nor exactly-once effects. A hard-terminated process can
leave a checkpoint lock; follow func_seq's existing ownership/recovery contract.

## Installed evidence

```sh
uv build --out-dir dist
uv run python scripts/check_distribution.py dist
uv run python scripts/qualify.py dist --profile sequence
```

Qualification first proves that base installation has neither optional package.
It then installs the lifecycle profile and exercises catalog/shell equivalence,
public module invocation, pause, fresh-process resume, completed-run non-replay,
definition/input mismatches and explicit retry/restart of a synthetic failed
operation. A local receipt file records actual call counts across processes.
No desktop interaction, remote service or real application effect is involved.

CI verifies both wheel and source artifacts on Python 3.14/Linux, macOS and
Windows, plus the Python 3.11 workflow floor on Linux and Windows. This evidence
qualifies the selected immutable sources; it does not qualify unrelated package
versions, a future DSL, a general pipeline adapter or hosted deployments.
