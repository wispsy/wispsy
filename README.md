# Wispsy

Independent Python tools, composed through explicit capability and data contracts.

This repository holds the ecosystem plan and executable reference workflows.
Each library keeps its own purpose, dependencies, supported Python versions and
release schedule.

[Release status](docs/releases/STATUS.md) compares actual PyPI versions with each
main branch. [Wispsy Releases](https://github.com/orgs/wispsy/projects/31) tracks
publication, dependency adoption and [release policy](docs/releases/POLICY.md).

Read the [implementation plan](IMPLEMENTATION_PLAN.md) and
[Wispsy Composition Project](https://github.com/orgs/wispsy/projects/23) for
architecture, acceptance criteria and dependencies.

The references demonstrate reusable capability groups, strict JSON pipes,
Python/shell workflow equivalence and optional durable execution. Independent
[moveset](https://github.com/wispsy/moveset) and
[scriptty](https://github.com/wispsy/scriptty) packages provide linear pipelines,
passive documents, commands and an optional Carets frontend. The
[Peaches contract](docs/peaches-contract.md) selects an independent
[text workbench application](https://github.com/wispsy/peaches) using these surfaces.

The base package supports Python 3.11+ with no runtime dependencies. Optional
func_seq integration requires Python 3.14+. The current reference profiles select published package versions.
This repository remains a source-development reference while its Paracosm
family dependency awaits an account-side PyPI Trusted Publisher binding.
Package release and publication are tracked separately.

```sh
uv sync --locked
uv run wispsy-reference ' Hello   WORLD '
uv sync --locked --extra workflow
uv run python -c 'from wispsy.integration import run_catalog; print(run_catalog(" Hello WORLD "))'
uv build --out-dir dist
python scripts/check_distribution.py dist
```

The [reference workflow guide](docs/reference-workflow.md) demonstrates the same
functions through Python, selected catalog calls and actual shell pipes, and
explains how to reproduce isolated wheel/source qualification.

The optional [lifecycle reference](docs/lifecycle-reference.md) connects those
calls to func_seq on Python 3.14+, with durable pause/resume and explicit recovery.

The [table reference](docs/tabular-reference.md) preserves typed rows through
Headless Spreadsheets and detached Markdown presentation. The
[profile qualification](docs/profile-qualification.md) records dependency direction,
limits and installed cross-platform evidence. `wispsy.composition.text_workflow_document`
supplies the same reference as passive schema-1 data for Scriptty hosts.


[Cohesion Block B](docs/cohesion-block-b/IMPLEMENTATION_PLAN.md) develops
Thoughtform model definitions, the Hypnosis harness and Carets application,
Paracosm worlds, and reusable terminal application composition toward a future
Warewolf hub. The [Project](https://github.com/orgs/wispsy/projects/28) tracks its
owning tasks and explicit integration, model/data and release decisions.

The optional Python 3.14+ [installed family profile](docs/cohesion-block-b/qualification.md)
qualifies real Transformer-to-terminal output, world rules and generated terminal
commands from immutable independent sources. Native POSIX interaction is checked
separately from Windows headless compatibility.


The [Hero homegrown training chapter](docs/cohesion-block-b/hero-training.md)
selects Hero and Hero Coding, independent Engl lexical/dependency records,
reviewed data sources, progressive curricula and reproducible local training.
New source selections remain owner-reviewed; the first pilot is bounded to
15 minutes. Ollama and externally connected tools remain a later path.

The separate [homegrown training profile](docs/cohesion-block-b/hero-qualification.md)
qualifies Engl, named Hero models, approved corpus preparation, numerical resume,
persistent jobs and specialization. [Source proposals](docs/cohesion-block-b/source-proposals.md)
keep future materials and runtime decisions explicit. The independent
[balanced session profile](docs/cohesion-block-b/hero-session-qualification.md)
adds selected vault/tutorials, Python docs/wiki snapshots, source quotas and
checkpoint collections. Experimental checkpoints stay local; sanitized
measurements are published separately.

The selected Hypnosis/Carets application family has a separate [qualification profile](docs/cohesion-block-b/application-qualification.md), preserving historical terminal/world and Hero source pins.

Current index qualification uses the `release-*.json` manifests in
`docs/cohesion-block-b/`. Original source-pinned manifests remain historical
records. Paracosm is selected from its qualified immutable preview source
until its PyPI publisher is available.
