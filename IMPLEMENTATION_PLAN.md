# Wispsy implementation plan

Adopted foundation: 7 November 2026. The [GitHub Project](https://github.com/orgs/wispsy/projects/23)
and linked issues own current scope, dependencies and delivery status. This plan
records architecture and acceptance, rather than a second status tracker.

## Purpose and names

Wispsy is an ecosystem of independently useful Python libraries. This repository
is its architecture home and executable composition reference. It will prove
that ordinary typed functions can be discovered, selected, connected and exposed
without forcing every application to install the entire ecosystem.

Peaches is the eventual cohesive application/programming experience that brings
the pieces together. Its expressive API and any small domain-specific language
should emerge from working examples. It is not a miscellaneous utility library
or an alternative name for the capability registry.

The first useful result is a typed text-normalization/report workflow that runs
as Python, selected catalog calls and shell pipes. An optional lifecycle profile
adds explicit pause and durable process restart through func_seq. This gives the
later pipeline API concrete data-flow and recovery evidence.

## Ownership

| Package | Owns | Keeps outside its core |
| --- | --- | --- |
| `hidden_moves` | `MoveSpec`, `Registry`, `Moves`, reusable `MoveSet` groups; definitions, binding, schemas, selected invocation | Workflow state, shell parsing, application authorization |
| `kindof` | Typed object/type inspection | Implicit negotiation or coercion |
| `enforce_type` | Explicit validation/coercion where the caller selects it | Unrequested conversion of pipeline values |
| `moveset` (planned) | `Pipeline` composition, explicit argument mappings and result references | A second durable execution engine |
| `func_seq` | Sequential execution lifecycle, cooperative pause, async execution, checkpoints and explicit recovery | Workflow-document grammar, terminal ownership |
| `scriptty` (planned) | Passive workflow definitions and scripting commands over the composition API | Terminal primitives or a general shell |
| `carets` | Reusable terminal input, components, focus, rendering and application primitives | Workflow parsing and execution |
| `expose_interface` | Command-line presentation of ordinary callable APIs | Owning their application behavior |
| `expose_api`, `expose_protocol`, `spatial_ui` | Optional HTTP, protocol and graphical presentation | Reimplementing composition/lifecycle |
| `backpack_store` | Optional durable records, provenance and execution receipts | Mandatory storage for every pipeline |
| `headless_spreadsheets` | Typed tables, portable interchange and table-source contracts | Mandatory UI or workflow engine |
| `compose_application` | Existing optional storage/API/UI composition profiles | A duplicate of this workflow roadmap |
| `wispsy` | Architecture, source-qualified references and ecosystem coordination | Replacement implementations of sibling libraries |
| `peaches` (planned) | Selected integrated product and expressive composition surface | A universal dependency required by every sibling |

`MoveSet("text")` groups capabilities; `moveset.Pipeline` will connect them.
The similar names describe different responsibilities. A group can be installed
into a registry and selected into a catalog without executing any operation.

Carets is a toolkit consumed by an interactive scripting frontend. The same
workflow remains usable in a script, service or application without a terminal.
Expose Interface and the other presentation adapters call the same application
API. They do not become dependencies of the capability or composition cores.

## Existing foundation and reuse

The source review used Hidden Moves `88a95fd75359cb250c067027d8ff95014da6fcbb`
and func_seq `b1a5346feeeef3fa1f398e4dcd81c2d23345386c`. Hidden Moves already
has explicit provider loading, selected catalog snapshots, schema-aware argument
validation, supported model conversion and finite JSON result serialization.
It lacks the brief's reusable MoveSet and stdin composition interface.

Func_seq already has versioned Script definitions, backward JSON references,
sync/async execution, boundary pacing, atomic checkpoints, uncertainty markers
and explicit retry/restart. These are reused, not recreated. This session proves
composition through its public API without changing the executor.

Carets' current roadmap owns terminal lifecycle, protocol coverage, constraints,
focus, widgets, forms and test fixtures. Its existing issues remain canonical.
The [Hidden Moves CLI adoption](https://github.com/wispsy/expose_interface/issues/8)
also remains in Expose Interface's queue. No unrelated migration PR is absorbed
into this work.

## Data and invocation contracts

1. Inputs to structured capability calls are JSON objects matching the selected
   capability's input schema. Python functions keep their ordinary direct API.
2. Outputs may be scalar JSON or structured records. Validate the declared output
   schema and serialize only finite JSON-compatible values. Never stringify an
   arbitrary object as a fallback.
3. Connections are explicit. A scalar output `"hello"` is not automatically
   compatible with `{"text": "hello"}`. A named wrapper option or pipeline
   mapping supplies that relationship; missing paths and invalid argument shapes
   fail before the dependent operation is invoked.
4. Use the existing catalog's documented JSON Schema subset. Neither kindof nor
   enforce_type silently widens it. Any later negotiated conversion is a named,
   selected adapter with its own contract and tests.
5. Provider loading executes trusted Python. Installing a provider does not
   activate it; registration does not authorize exposure. Select exact names and
   configure target resources outside public tool arguments.
6. The CLI transports one bounded UTF-8 JSON document per process. Reject malformed
   JSON, duplicate keys and non-finite values. Keep results on stdout, diagnostics
   and opt-in machine-readable errors on stderr, with nonzero failure exits.
   Explicit scalar wrapping is available; shell globbing, parsing and expansion
   remain shell responsibilities.
7. JSON Lines, streaming, branching, concurrent execution, distributed scheduling
   and compensation are separate scopes. Their partial-effect and cancellation
   rules need concrete requirements before implementation.

The reference has no external side effects. Optional persistent examples use
synthetic local receipts and caller-selected checkpoint paths. A completed step
must not replay during ordinary resume. A failed or interrupted action may have
already affected the world, so retry/restart requires an explicit choice.
There is no exactly-once or automatic rollback claim.

## Execution and definition identity

The composition layer determines which operation receives which values.
Func_seq determines when it executes and where progress is committed. A future
moveset adapter should compile definitions to Script steps rather than introduce
another checkpoint schema or state machine.

Stable named wrappers and explicit step IDs connect selected catalog calls to
func_seq. The reference records a script version and exact source profile.
The application must change the definition version when callable behavior,
captured catalog state, defaults or relevant environment configuration changes;
func_seq's manifest does not hash source code or authenticate the environment.
Pipeline-to-Script compilation and mapping identity are defined in the adopted
[pipeline contract](docs/pipeline-contract.md).

## Python and dependency policy

Keep support floors per package and per installed profile. Raising every package
to 3.14 would unnecessarily remove useful standalone support; pretending a
func_seq integration supports 3.11 would be incorrect.

| Surface | Initial support | Dependency direction |
| --- | --- | --- |
| Wispsy base reference functions | Python 3.11+ | Standard library only |
| Hidden Moves and its composition reference | Python 3.11+ | Optional qualified Hidden Moves source |
| Func_seq lifecycle reference | Python 3.14+ | Optional qualified Hidden Moves + func_seq sources |
| Carets standalone | Its existing Python 3.10+ contract | No change in this session |
| Kindof standalone | Its existing Python 3.14+ contract | Optional inspection only |
| Future moveset/scriptty base | Select in PIPE-01; prefer 3.11+ if feasible | Lightweight capability composition |
| Peaches/presentation profiles | Intersection of selected dependencies | Explicit extras and compatibility receipts |

CI verifies the declared floors and selected current interpreter. Optional
profiles use immutable source revisions until compatible releases are qualified.
The base install must not import or require optional adapters. Each package keeps
its own version and release schedule; no synchronized ecosystem version is implied.

## Ordered work

| Task | Owning issue | Result | Depends on |
| --- | --- | --- | --- |
| WP-01 | [wispsy#1](https://github.com/wispsy/wispsy/issues/1) | Architecture, plan, queue, package/CI foundation | — |
| HM-SET-01 | [hidden_moves#38](https://github.com/wispsy/hidden_moves/issues/38) | Reusable named groups, atomic installation and documentation | WP-01 |
| HM-JSON-01 | [hidden_moves#39](https://github.com/wispsy/hidden_moves/issues/39) | Strict stdin JSON, explicit wrapping, error/stdio contract | HM-SET-01 |
| WF-01 | [wispsy#2](https://github.com/wispsy/wispsy/issues/2) | Installed Python/catalog/shell workflow equivalence | HM-SET-01, HM-JSON-01 |
| SEQ-01 | [wispsy#3](https://github.com/wispsy/wispsy/issues/3) | Optional lifecycle, fresh-process resume and recovery proof | WF-01 |
| PIPE-01 | [wispsy#4](https://github.com/wispsy/wispsy/issues/4) | Select concrete pipeline API and independent package identity | WF-01, SEQ-01 |
| PIPE-02 | [wispsy#5](https://github.com/wispsy/wispsy/issues/5) | Independent linear moveset core with explicit references | PIPE-01 |
| PIPE-03 | [wispsy#6](https://github.com/wispsy/wispsy/issues/6) | Optional compilation to func_seq | PIPE-02, SEQ-01 |
| SCRIPT-01 | [wispsy#7](https://github.com/wispsy/wispsy/issues/7) | Passive versioned JSON/TOML workflow documents | PIPE-02 |
| SCRIPT-02 | [wispsy#8](https://github.com/wispsy/wispsy/issues/8) | Inspect/run/resume commands through Expose Interface | SCRIPT-01, PIPE-03 |
| TERM-01 | [wispsy#9](https://github.com/wispsy/wispsy/issues/9) | Optional Carets interactive frontend | SCRIPT-02, Carets prerequisites |
| TABLE-01 | [wispsy#10](https://github.com/wispsy/wispsy/issues/10) | Normalization-to-table/presentation reference | PIPE-02 |
| PEACH-01 | [wispsy#11](https://github.com/wispsy/wispsy/issues/11) | Select integrated product and evidence-led DSL scope | SCRIPT-02, TERM-01, TABLE-01 |
| QA-01 | [wispsy#12](https://github.com/wispsy/wispsy/issues/12) | Installed cross-package/platform qualification | PIPE-03, SCRIPT-02, TABLE-01 |
| REL-01 | [wispsy#13](https://github.com/wispsy/wispsy/issues/13) | Select useful namespace releases and publication profile | WF-01, SEQ-01 |
| JSONL-01 | [wispsy#14](https://github.com/wispsy/wispsy/issues/14) | Optional streaming contract, selected only when needed | HM-JSON-01, PIPE-01 |

Carets prerequisites are [lifecycle #1](https://github.com/wispsy/carets/issues/1),
[terminal ownership #2](https://github.com/wispsy/carets/issues/2),
[focus #4](https://github.com/wispsy/carets/issues/4),
[forms/services #8](https://github.com/wispsy/carets/issues/8) and
[testing #9](https://github.com/wispsy/carets/issues/9). Their owning Project
determines readiness and completion; links do not claim those features exist.
TABLE-01 reuses the existing Tabular Interfaces and Cohesion contracts.

## First implementation session

Deliver WP-01, HM-SET-01, HM-JSON-01, WF-01 and SEQ-01 as five focused PRs.
Push each ready branch and start CI before continuing with the next task.
HM-JSON-01 builds on HM-SET-01; SEQ-01 builds on WF-01. Cross-repository source
profiles initially select the exact pushed implementation and are reconciled to
merged sources before final qualification.

Squash passing PRs in dependency order. Reconcile each immediate dependent
against current main, retain parent branches until dependents are retargeted,
and preserve shared history. Require relevant fresh checks after integration
changes. Final main gets a brief installed startup/reference smoke and its CI
receipt, rather than another redundant exhaustive local sweep.

The foundation session ended at the PIPE-01/REL-01 decisions. The adopted
[pipeline contract](docs/pipeline-contract.md) selects independent `wispsy/moveset`
and `wispsy/scriptty` repositories and unlocks the pipeline/document implementation.
Terminal prerequisites, integrated product scope and selected releases retain
their issue-level gates.

## Verification and release boundaries

Use standard-library unittest, temporary files, synthetic functions and actual
subprocesses. Grouping tests prove atomicity, ordering and binding isolation.
CLI tests prove stream separation, finite bounded parsing, error exits and real
pipe behavior. Workflow checks compare all selected invocation surfaces; lifecycle
checks verify restart and replay counts in separate processes. Build both wheel
and source distributions and exercise installed profiles outside the source tree.

The initial source version is `0.0.1.dev0`, not a published release. No empty
placeholder packages are needed to make the reference useful. REL-01 checks
namespace ownership, useful contents, license, exact version/artifact identity
and trusted publishing before a selected functional release. Public package pages
alone do not prove ownership, and a 404 does not guarantee a name can be registered.
Hosted sites, external services and deployment are separate scopes.
