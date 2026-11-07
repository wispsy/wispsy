# Peaches text workbench

Adopted from the installed pipeline, scripting, terminal and table references on
7 November 2026. Repository/distribution/import identity is
[`wispsy/peaches`](https://github.com/wispsy/peaches), `peaches`, `peaches`.
It is independently versioned. The namespace is reserved according to the user's
confirmation; publication access and release artifacts remain REL-01 work.

## Demonstrable workflow

A user supplies text, inspects the selected normalization/report workflow, runs it
as a library or command, optionally pauses/resumes durable progress, then consumes
typed reports as a table or escaped Markdown. A terminal optionally edits the same
inputs and explicitly confirms the required capabilities. Every surface returns
the same report; terminal installation is not needed for library or CLI execution.

The public application surface is a small TextWorkbench with a passive workflow
document, selected catalog assembly, async report execution and optional table and
terminal methods. Expose Interface presents commands. The workbench supplies a
curated application, while reusable lower layers keep their ordinary APIs.

| Owner | Responsibility |
| --- | --- |
| Wispsy reference | Ordinary typed normalize/report functions and schema-1 reference document |
| Hidden Moves | Selected capability definitions, binding, schemas and invocation |
| Moveset | Immutable linear mapping, references and definition identity |
| Scriptty | Passive documents, versioned outcomes and application execution API |
| Func_seq | Optional checkpoints, pause/resume and explicit uncertain recovery |
| Carets | Optional terminal input, focus/forms, rendering and resource lifetime |
| Headless Spreadsheets | Optional typed table/source and detached Markdown presentation |
| Peaches | Curated workbench API, explicit profile selection and user commands |

The base supports Python 3.11+ with only the selected scripting/reference packages.
CLI adds Expose Interface. Lifecycle, table and terminal profiles require 3.14+.
Each optional profile uses exact qualified sibling revisions; a functional release
must replace development-only source requirements with selected release profiles.
No storage, HTTP, graphical hosting or external account is required.

## Definition and grammar policy

Use Scriptty's existing strict schema-1 JSON/TOML, including explicit literal/input/
reference/object/array expressions and source diagnostics. There is no demonstrated
need for a second grammar or DSL. Peaches exposes this document through inspect
and delegates validation; it does not evaluate code or infer coercion from text.
Any later grammar requires a concrete workflow, passive parsing, source ranges,
compatibility/version rules and a separately scoped issue.

## First application milestone

Record PEACH-02 before implementation: deliver the independent functional package
with TextWorkbench, equivalent inspect/report/optional table/terminal commands,
explicit lifecycle recovery, isolated wheel/source tests and supported-floor/
platform CI. Build on the already qualified references without duplicating their
parser, registry, executor, terminal or table contracts. Keep publication and
deployment separate. PEACH-02 must depend on this contract and QA-01/TERM-01;
merge this decision before merging the integrated application.
