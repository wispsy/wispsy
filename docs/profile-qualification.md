# Selected composition profiles

The exact source requirements live in pyproject.toml and uv.lock. Every installed
wheel/source qualification prints its artifact SHA-256 plus the actual Python,
OS, package versions and direct source revisions. CI logs are the qualification
receipt; a package version alone does not identify this source-development profile.

| Profile | Python | Packages/surfaces |
| --- | --- | --- |
| Base | 3.11+ | Standard-library reference functions and passive reference document |
| Workflow/scripting | 3.11+ | Hidden Moves, moveset, scriptty and Expose Interface; actual installed commands/pipes |
| Sequence | 3.14+ | Optional func_seq lifecycle with durable fresh-process recovery |
| Table | 3.14+ | Headless Spreadsheets typed rows/source and detached Markdown rendering |
| Terminal | 3.14+ | Optional Carets model/runtime and synthetic frontend acceptance |
| Composition qualification | 3.14+ | Selected union, preserving independently optional consumers |

Linux/Windows qualify the 3.11 workflow/scripting floor. Linux/macOS/Windows qualify
the 3.14 composition profile. Each artifact installs outside the checkout. The
base import remains free of optional packages. Tests compare ordinary reference,
selected catalog, immutable Pipeline, passive workflow and actual installed CLI
results for the same Unicode inputs; durable commands pause and resume in separate
processes. Synthetic terminal input/selection/progress uses the same application
API and result shape. Existing source/lifecycle tests supply effect-count and
uncertain retry evidence. Typed table snapshots and Markdown escaping are selected
presentation checks, without hosting.

Dependency direction is explicit: scriptty → moveset → Hidden Moves; optional
moveset lifecycle → func_seq; optional scriptty presentation → Expose Interface or
Carets. Wispsy's optional table consumer uses Headless Spreadsheets. No registry,
second execution engine or terminal dependency is introduced into the base.

Hidden Moves' supported schema subset covers JSON types, enum, anyOf, object
properties/required/additionalProperties and array items, with documented annotation
keywords. Unsupported keywords are rejected. General JSON Schema negotiation,
coercion, source authentication and arbitrary object serialization are not claimed.

Pipeline/document/transport values are finite UTF-8 JSON bounded to 1 MiB and depth
32; definitions allow at most 256 steps and 32 reference path segments. The table
reference selects 1–64 rows. Func_seq retains its own 4 MiB checkpoint/document
budget and explicit uncertain-effect semantics. A completed action is not replayed
on ordinary resume; interrupted/failed actions require explicit retry/restart.

Native interactive terminal input is selected only on supported POSIX TTYs.
Carets' installed qualification includes an independent-process pseudo-terminal
single-key regression, ensuring buffered stdin does not block after readiness.
Cross-platform synthetic acceptance is not a native Windows console claim. No
untested interpreter, package revision or platform is inferred from these receipts.
Namespace reservation was confirmed by the user; authenticated publishing access,
release dependency requirements, selected release artifacts, tags and publication
remain REL-01 decisions. This milestone does not publish or deploy a product.
