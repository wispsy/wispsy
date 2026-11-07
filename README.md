# Wispsy

Independent Python tools, composed through explicit capability and data contracts.

This repository holds the ecosystem plan and executable reference workflows.
Each library keeps its own purpose, dependencies, supported Python versions and
release schedule.

Read the [implementation plan](IMPLEMENTATION_PLAN.md) and
[Wispsy Composition Project](https://github.com/orgs/wispsy/projects/23) for
architecture, acceptance criteria and dependencies.

The references demonstrate reusable capability groups, strict JSON pipes,
Python/shell workflow equivalence and optional durable execution. Independent
[moveset](https://github.com/wispsy/moveset) and
[scriptty](https://github.com/wispsy/scriptty) packages provide linear pipelines,
passive documents, commands and an optional Carets frontend. Peaches' integrated
product contract follows these working surfaces.

The base package supports Python 3.11+ with no runtime dependencies. Optional
func_seq integration requires Python 3.14+. This is a source-development reference;
package release and publication are tracked separately.

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
