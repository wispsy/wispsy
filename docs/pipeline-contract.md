# Linear pipeline contract

Adopted 7 November 2026 from the installed text and lifecycle references.

## Package identities

`wispsy/moveset` owns distribution/import `moveset`; `wispsy/scriptty` owns
distribution/import `scriptty`. They are independent repositories, packages and
version lines. Wispsy remains the architecture and cross-package reference home.
The user confirmed the intended namespaces are reserved for publication. This
source milestone does not authenticate publication permissions or select a release.

Moveset supports Python 3.11+ and uses the explicitly selected Hidden Moves catalog
for capability descriptions, argument validation and result serialization. Its
optional `sequence` profile requires Python 3.14+ and func_seq. Scriptty supports
Python 3.11+ with moveset; its CLI adds Expose Interface, and its lifecycle profile
adds the moveset sequence adapter. Terminal and table presentations stay optional.
Development profiles pin immutable sibling revisions; publication needs separately
qualified released requirements.

## Definitions and binding

```python
from moveset import Input, Pipeline, Ref, Step

definition = Pipeline(
    "text-report", version="1",
    steps=(
        Step("normalize", "text.normalize", {"text": Input("text")}),
        Step("report", "text.report", {"text": Ref("normalize")}),
    ),
    outputs={"report": Ref("report")},
)
bound = definition.bind(selected_catalog, catalog_version="text-v1")
result = bound.run({"text": " Hello   WORLD "})
assert result.outputs["report"]["text"] == "hello world"
```

Pipeline, Step, Input and Ref definitions are immutable snapshots. Step IDs are
unique bounded ASCII identifiers. Capability names must already be selected in
the caller's catalog. There is no provider discovery or registration while binding
or running. Input selects a top-level run input plus an optional key/index path;
Ref selects an earlier step result. References may occur inside explicit argument
objects/lists. A literal object cannot be mistaken for a reference in the Python
API. The passive document format uses tagged expressions to preserve this property.

Validate all IDs, selection, backward references, input availability and static
argument shapes before any call. Validate resolved argument values using the
catalog before each dependent call. Result paths cannot in general be proven
before their producer executes: missing paths fail with step context before the
consumer runs. No general schema compatibility inference or implicit coercion is
promised. Values cross boundaries as copied, finite JSON; records and scalars keep
their shape. Definitions/results returned to callers cannot mutate later runs.

Run synchronously only when every selected operation is synchronous; reject a
declared async step before the first effect. `arun` awaits mixed sync/async calls
in definition order, on the caller's event loop. Sync functions run on the calling
thread. An unexpected awaitable in sync execution is closed where possible and
fails explicitly. Step failures include the step ID and capability; original
exceptions remain chained. Cancellation propagates. Each ordinary run starts
fresh; there is no automatic retry, concurrency, checkpoint or rollback.

Bound definitions include caller-supplied `catalog_version` in their fingerprint,
along with selected input/output schemas, async flags, mappings, pipeline name,
version and output expressions. Catalog version must change when callable code,
bound resources, configuration or defaults change. A fingerprint is compatibility
identity, not source attestation or authorization.

## Lifecycle compilation

Compilation is lossless for this linear JSON contract: translate each explicit
mapping into func_seq arguments and backward references, keeping the same step
IDs and catalog-validated wrappers. Include the bound fingerprint and run inputs
in the compiled Script version/manifest, so mapping, schema, catalog-version,
definition and input changes reject existing checkpoints. Resolve outputs from
the completed results without adding a synthetic effect step.

Func_seq owns progress, atomic checkpoint writes, cooperative boundary pause,
async cancellation, resume, restart and explicit uncertain-step retry. Expose its
Script/Control API instead of building another state machine or checkpoint format.
A failed/cancelled callable may already have had effects. Recovery never implies
exactly-once delivery. Fresh-process tests must prove completed steps are not
replayed and changed definitions/inputs cannot resume old progress.

## Documents and interfaces

Scriptty starts with bounded, strict schema-1 JSON/TOML documents, not a new grammar.
Each expression has exactly one tag: `value`, `input`, `ref`, `object` or `array`.
Unknown keys/versions, duplicate JSON keys, non-finite values, forward references
and unsupported paths fail with source/step locations. Parsing never imports a
provider or executes workflow code. The host binds an explicit catalog and its
version; CLI provider selection is a separate trusted-code boundary.

List/inspect/run/resume commands call the same library API through Expose Interface.
Carets consumes that API after its own prerequisites pass. Table consumers use
Headless Spreadsheets' existing contracts. Peaches' product/grammar decision
follows those working examples. Streaming, branches, parallel work, shell parsing
and distributed scheduling remain separate scopes.
