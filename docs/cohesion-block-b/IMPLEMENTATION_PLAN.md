# Cohesion Block B implementation plan

Planning baseline: 19 November 2026. This is the complete architecture and work
register for the first model/harness/world family and reusable terminal
application composition. The [Cohesion Block B Project](https://github.com/orgs/wispsy/projects/28)
and owning issues are the canonical execution queue. This plan records intended
behavior, ownership and acceptance. A proposed interface is not a shipped API.

## 1. Product outcome

A developer can define an individual model with Thoughtform, supply a real
Thoughtformula Transformer and tokenizer, operate a bounded run in Hypnosis,
and observe live results in a Carets application. The same domain behavior is
usable from ordinary Python and Expose Interface commands. Paracosm can compose
model-neutral beings into a deterministic world, including an optional habitat
mind whose proposals pass through the same world rules as other actions.

Hypnosis is the first application proving reusable Carets application design.
Compose Application gains a terminal project profile using Expose Interface and
Carets alongside its existing Expose API and Spatial UI web profiles. Warewolf
is the subsequent Carets hub: one terminal owner hosting a growing collection
of explicitly selected command-line and component applications.

The project must improve the component libraries where a reusable seam is
missing. Application code must not silently replace their responsibilities.
A useful first vertical slice is deliberately smaller than a general autonomous
coding platform, a production model trainer, or a persistent game engine.

## 2. Input evidence and corrections

The supplied local design notes are: `Streaming in Carets.md`,
`Agent Harness Definition.md`, and `hypnosis, thoughtform, paracosm.md`.
Their architectural intent is adopted. They are design input, not evidence that
an illustrative Python interface exists. Their full private paths and unrelated
vault content are not required by the public source tree.

The [Thoughtformula streaming commit](https://github.com/wispsy/thoughtformula/commit/403de839c96fe6b1e4f0a35d6fdf518c4dd27a12)
adds synchronous token-ID generators on `ModernMicroGPT`, including speculative
generation. It does not provide the illustrative `Transformer.load(...)` API,
a cancellable async model service, or a complete agent harness. Use actual
`ModernMicroGPT`, `BPETokenizer`, generator and checkpoint interfaces.

[Wispsy JSONL-01](https://github.com/wispsy/wispsy/issues/14) intentionally waited
for a concrete streaming consumer. Hypnosis now provides that consumer. Adopt
its contract task without duplicating it or equating in-process streaming with
proved subprocess JSONL transport. Its existing prerequisites are complete.

Carets main already has an asyncio queue, serialized updates, commands, task
cancellation, explicit command errors, terminal ownership, forms, focus and test
fixtures. Streaming should extend those mechanisms. Applications use maintained Carets main and its tested public interfaces.
Original local terminal experiments are outside the selected implementation scope.

Thoughtform, Hypnosis and Paracosm start from the user's existing Python 3.14+
uv projects. Public source repository creation is authorized. Package releases,
weight publication, model/data downloads, paid inference and deployment are
separate concrete decisions.

## 3. Architecture and ownership

| Project | Owns | Consumes | Must remain outside |
| --- | --- | --- | --- |
| Thoughtformula | Tensors, autograd, Transformer, tokenizer, samplers, KV caches, LoRA/DPO/KTO mathematics, checkpoint representation | Standard library and its own modules | Harness policies, terminal widgets, beings, world rules |
| Thoughtform | Named individual model definitions, model references/lineage, being identity, observation/action/policy contracts, goals/memories/relationships | Optional model and memory adapters | Another Transformer/trainer, a scheduler, world authority |
| Hypnosis | Run lifecycle, context/tool policy, verification/repair, job assembly, experiment/evaluation tracking, measured harness optimization, Carets application | Explicit providers and existing component libraries | A second general pipeline engine, CLI parser, HTTP stack, database, model math |
| Paracosm | World/habitat state, deterministic clock/step, action validation, rules, authoritative accepted events, save/replay | Thoughtform contracts, optional storage and job adapters | Unchecked model-authored state, implicit weight updates, mandatory environment intelligence |
| Carets | Async terminal runtime, messages, managed streams, renderer/layout/focus/components/themes, terminal cleanup | Standard library; opt-in presentation integrations | Model protocols, domain job state, workflow checkpoints |
| Compose Application | Explicit assembly profiles, safe project generation, reference applications and installed compatibility qualification | Optional selected libraries | A mandatory umbrella runtime dependency for every library |
| Warewolf (later product) | Hub navigation, selected applications, shared terminal shell and services | Carets and explicit app manifests | Global import/plugin scanning, multiple competing terminal owners |

### 3.1 Dependency direction

Thoughtformula stays independent. Thoughtform core stays independent of
Hypnosis, Paracosm and a specific model provider. Its model adapter accepts an
explicit already-configured model/tokenizer and calls public Thoughtformula
methods. Importing the core does not import a Transformer or start work.

Hypnosis consumes neutral model/provider contracts and optionally Thoughtform.
Paracosm consumes Thoughtform and may submit jobs through an optional adapter;
Thoughtform does not import Paracosm. Application assembly imports adapters at
the selected composition root. No pair of core packages imports each other.

```mermaid
flowchart BT
    TF[Thoughtformula] --> TFA[Thoughtform model adapter]
    TFA --> H[Hypnosis]
    TFC[Thoughtform core] --> H
    TFC --> P[Paracosm]
    HM[Hidden Moves selected catalogs] --> H
    WF[Moveset / func_seq / Scriptty] --> H
    BP[Backpack Store] --> H
    BP --> P
    C[Carets] --> H
    EI[Expose Interface] --> H
    H --> CA[Compose Application references]
    C --> CA
    EI --> CA
    CA --> WW[Warewolf]
```

Arrows mean optional consumption, not that every base install requires every
lower box. A shared contract document or finite fixture does not create a
mandatory dependency on this reference repository.

## 4. Reuse register and component development opportunities

| Library | Existing capability to reuse | Missing seam to develop only when demonstrated |
| --- | --- | --- |
| Thoughtformula | Real token generators, tokenizer, model/caches, training and checkpoint APIs | Boundary qualification, cancellation at generator steps, stable model/checkpoint compatibility receipts |
| Carets | Program, Command, Msg, renderer, TerminalSession, FocusManager, forms, TestProgram | Managed bounded streams; later frame scheduling, themes, reusable shell and tables |
| Expose Interface | Typed callables, Interface, command/option definitions, usage errors | Reusable command groups/embedding only if application evidence requires it |
| Hidden Moves | Explicit providers, selected CapabilityCatalog, schemas, binding, structured invocation; workspace plugin | Model-neutral tool request/result adaptation and narrow selected capability policies |
| Moveset | Immutable sync/async linear pipeline definitions and explicit references | Compose domain stages without introducing another pipeline language |
| func_seq | Pause/resume, checkpoints, step identity, uncertain-effect recovery | Adapt domain jobs through existing Moveset compilation; no second checkpoint schema |
| Scriptty | Passive JSON/TOML job documents, explicit provider selection, command and Carets frontend patterns | Reuse job inspection/run/resume where applicable; do not fork the workflow runner |
| Backpack Store | Explicit codecs/registered models, SQLite lifecycle, checked revisions, async owner | Typed domain records for runs, memories, worlds and evaluations |
| Enforce Type | Optional structured validation/codecs | Use for richer contracts rather than duplicating schema coercion or validation |
| Kindof | Existing optional type inspection | Inspect selected callables without a new annotation parser |
| Requ | Independent HTTP transport | Ollama/provider cancellation and streamed framing belong in qualified transport adapters |
| Apiconn | Typed API operations and REST/GraphQL composition | Reusable provider operations, not model or harness state |
| Parse MD | Shared Markdown document/parser/renderer engine | Select bounded instruction/document excerpts; no new Markdown parser |
| Headless Spreadsheets | Typed tables, detached snapshots and adapters | Reusable evaluation/run/world table views consumed by terminal and web presentation |
| Escape Colors | Terminal text styling/output | Compatible noninteractive diagnostics; interactive screens retain Carets rendering ownership |
| Expose API | Native API transport, policies and registered resource adapters | Optional remote control/monitoring after a real boundary is selected |
| Spatial UI | Typed native web components/sessions | Optional experiment/world browser views over the same application services |
| Compose Application | Safe exclusive project publication, immutable source selection, source/wheel compatibility profiles | Explicit terminal generation and multi-interface assembly |
| Builtouts | Existing output/artifact composition, where its public contract fits | Evaluate an adapter before inventing a report/export framework |

Reuse means calling public, selected interfaces and improving their owning
library when necessary. It does not mean forcing every dependency into the
first milestone or building wrappers that add no behavior. The small finite
run lifecycle in Hypnosis is domain state, not a general persistent workflow
engine. The first in-memory Paracosm transition function is domain logic, not a
second database or event persistence layer.

## 5. Contracts

### 5.1 Individual model definitions and beings

A model definition identifies a model independently of a character: stable ID,
provider kind, explicit model/artifact reference, generation configuration and
later tokenizer/adapter/checkpoint lineage. A being has its own stable identity,
role, goals and selected model/policy reference. Many beings may share one base
model while keeping independent context, memory and authorization.

Core observation/action values are detached immutable domain records. An
observation identifies the actor, tick and visible information. An action is a
proposal identifying actor, action kind and target/value. A deterministic policy
can implement the contract without any model. Model text must pass explicit
structured decoding/validation before it can become an action or tool request.
No model output is executable Python, an import path, SQL or a shell command.

The initial Thoughtformula adapter is explicit: the caller supplies compatible
model and tokenizer instances plus a definition. It yields token IDs and exact
decoded text fragments through the existing generator. Validate input vocabulary,
finite sampling settings, token budget and the current context-capacity profile.
Zero budget produces nothing without invoking a known zero-budget generator
edge case. Do not hide upstream defects: track them in Thoughtformula and keep
qualification pins explicit. Close the generator on cancellation or early exit.
A tiny untrained model proves integration only; it proves no useful language or
agent capability.

### 5.2 Hypnosis runs and events

Each invocation has an explicit run ID, bounded configuration and one owner.
Events have increasing sequence numbers, run identity, a finite event kind and
bounded payload. Define started, delta/progress and exactly one normal terminal
outcome: completed, canceled, failed or limit reached. Structural failures must
not expose exception text or credentials by default. Cancellation of the
consumer/task must propagate while closing the source; never report completion
from a canceled task's cleanup.

Separate accepted model/tool events from rendering state. A renderer may retain
only a tail while the run enforces independent total output/event/time budgets.
Do not infer completion from a dropped connection, EOF without a terminal record,
a timeout or a model's statement that it finished. A stream can already have
produced useful text or external effects when it fails; that remains visible.

The initial producer is a caller-supplied async iterable, exercised offline.
A real synchronous Transformer must run behind an explicitly managed execution
boundary so it cannot monopolize the Carets event loop. Cancellation is
cooperative at token boundaries; Python threads cannot be forcibly killed.
Process isolation and hard deadlines require their own selected provider task.

### 5.3 In-process Carets streams

`Command.stream(factory, ...)` creates one invocation-owned asynchronous
message producer. The factory is lazy and called only when scheduled. A bounded
queue blocks the producer when delivery is saturated; inputs and stream messages
share serialized model dispatch. Each yielded item must be a Msg. An empty
stream is valid; application-level completion remains an application message.

Program owns producer task identities and cancellation. Program.cancel and
Program shutdown cancel/await producers and close iterators. A producer failure
becomes CommandErrorMsg with the same command ID. Existing commands, timers,
post(), batch semantics and the Python 3.10 floor stay compatible. post() remains
a synchronous event-loop-thread API; the bounded stream path must not pretend
to make arbitrary thread posting safe or bounded.

Bound queue capacity and fairness separately. A bounded queue limits producer
lead, not total state retained by the model. Frame throttling is a later task:
all messages still update the model; only redraws may coalesce. Always flush the
final state and preserve prompt key/resize/cancel handling under load.

### 5.4 JSON Lines and subprocess transport

The selected wire format is a versioned stream of newline-delimited UTF-8 JSON
objects, with one event per physical line. Escape newlines within JSON strings.
Never split a UTF-8 code point or accept duplicate keys/nonfinite numbers. Use
strict schema versions and finite structural depth. Select explicit ceilings:
64 KiB per encoded record including newline, 16 MiB per stream and 100,000
records for the first subprocess profile, or stricter caller budgets.

stdout carries records only; diagnostics go to stderr. A terminal success record
plus a successful producer exit is required for transport success. A failed
record represents an application outcome; malformed framing, wrong sequence,
oversized data, missing terminal state or nonzero process exit is a transport
failure. Never rewrite an uncertain partial run as a successful empty result.

Ordering is per producer/run; no global interleaving claim. Backpressure must
come from actual awaited writes and bounded reads. Stop upstream on downstream
failure/closure, drain or bound stderr, apply deadlines, await process shutdown
and reap children. Handle BrokenPipe, late nonzero exit, cancellation, partial
records and cleanup in actual subprocess tests. No shell parsing, implicit
coercion or globbing is added to Hidden Moves. Existing single-document commands
keep their formats and behavior. JSONL-01 selects this contract; JSONL-02 proves
implementation before any CLI advertises subprocess stream support.

### 5.5 Tools, context and memory

Hidden Moves owns capability discovery, schemas, selected catalogs and binding.
The application chooses exact providers and capability names, authorizes requests,
and configures clients/resources. Installing metadata does not activate code.
Annotations and model tool names never grant authority. Each role has its own
selected catalog and budget; unknown names fail before execution.

Context is bounded and provenance-bearing. Use explicit files/providers and
selective retrieval, not unconditional whole-vault or whole-repository prompts.
Distinguish trusted instructions, task inputs, retrieved text and tool results.
Instructions embedded in retrieved data cannot change provider activation or
authority. Persistent memory stores experiences and domain records through
Backpack, not new pickle formats or callable serialization.

Keep experiential learning, model weight updates and world evolution separate.
A new memory does not trigger fine-tuning. A model proposal does not mutate a
world. Harness optimization does not change weights unless the user selects a
separate training job.

### 5.6 Training and harness optimization

Training job stages are prepare data, validate provenance/config, load source
checkpoint, train via Thoughtformula, evaluate, write a new artifact and register
its lineage. Hypnosis owns when/why and workflow/evaluation policy; Thoughtformula
owns how gradients, optimizers and weights work. Checkpoints are explicit local
artifacts; never overwrite the source, download weights or publish a result as
an incidental step. Select dataset/license/retention and compute budget first.

Harness candidates vary explicit context selection, planning, tool sets, workflow,
verification and repair budgets. Use versioned tasks and seeds with separate
development, selection and held-out test splits. Report verified task success,
failures, latency, tokens, tool calls, repair attempts and compute/resource use.
Compare equal budgets and retain denominators and uncertainty. Store exact
source/provider/model/config/data identities. Candidate promotion and deployment
are explicit decisions; adaptive changes must pass regression and held-out gates.

### 5.7 World authority and replay

Worlds own habitats, actor membership, deterministic tick/order and validated
state transitions. Compute proposals from a defined observation snapshot, then
validate all proposals before committing a step. Do not let later policies
observe partially applied state accidentally. Initial actions are intentionally
small and typed; unsupported kinds and targets fail before mutation.

A habitat mind uses the same policy interface as a being. It can propose actions
within its allowed scope; it cannot bypass rules. Add a pure headless stepping
reference before persistence and sophisticated minds. Save/replay later records
schema/rules/source identity, seed, observations, proposals, accepted actions and
state. Backpack owns persistence; explicit replay does not rerun model inference
and pretend the output is deterministic.

### 5.8 Terminal application and hub composition

Commands call application services; Carets models observe outcomes and own local
view/focus/input state. One Program and TerminalSession own the terminal.
Long-running calls run in commands/managed producers, never awaited inside
update(). A native application must configure a renderer; renderer=None is a
headless mode, not a live display. Untrusted output is displayed as text, with
terminal control characters made visible rather than executed.

Develop design tokens and layout from two real applications: semantic colors,
spacing, surfaces, status/error roles, navigation, focus, shortcuts and narrow
terminal behavior. Reuse Style/FocusManager/widgets before adding abstractions.
Carets issue #10 remains the coherence umbrella; link new evidence to it rather
than claiming the full widget/layout roadmap is finished.

Compose Application's terminal profile uses safe exclusive creation and an
immutable selection receipt. Generated source belongs to the application.
Repeat generation never overwrites source/data or installs dependencies.
Headless check commands must be useful without opening a terminal. Existing
service/ui/live profiles preserve their qualified reference sources. Terminal
requirements must not leak into base/web installs.

Warewolf separates embedded component applications (one Program) from external
process applications (explicit stdio/lifecycle bridge). Define manifests,
selection, services and navigation before a product repository. Activation is
explicit and trusted; do not scan/import every installed package. Start with
Hypnosis plus a second real application such as Scriptty after their embedding
contracts are qualified.

## 6. Python, dependencies, packaging and compatibility

Keep existing package floors: Carets 3.10+, Thoughtformula 3.12+, and the new
family/Compose Application 3.14+. Optional profiles require the intersection of
their selected dependencies. Base imports remain side-effect-free and do not
start event loops, workers, terminals, model inference or database connections.

The new family begins with dependency-free domain cores where practical. Add
Thoughtformula, Carets, Expose Interface, Backpack and workflow dependencies
only to the implementing profile that uses them. The task authorizes these
existing ecosystem integrations, not arbitrary external runtime dependencies.
Use immutable Git source revisions until compatible independent releases are
qualified. Public source repositories are not PyPI publication or name ownership
claims. Keep uv build backends and the user's existing package versions unless
a concrete release task selects new versions. Use existing MIT ecosystem terms
for newly authored source and retain original copyright/attribution.

Build wheels and source distributions. Include the plan, contract guides and
meaningful tests in source artifacts where supported. Source profiles record
full commit IDs, distribution/import names, versions and artifact SHA-256.
Existing unrelated lockfiles, branches, worktrees and user files remain intact.

## 7. Milestones and acceptance

### M0 — Architecture and canonical queue

Adopt this plan, create the public family repositories from existing uv seeds,
reuse JSONL-01 and link cross-project tasks.
Every task has scope, acceptance, dependencies, branch and owning repository.
The original composition and Block A history remains available.

### M1 — First runnable model/harness/terminal/world slice

Deliver managed Carets streams, Thoughtform definitions and its real Transformer
adapter, a finite Hypnosis runner and Carets application, deterministic Paracosm
stepping, and terminal project generation. Demonstrate headless and UI event
consumption with a deterministic source and a tiny Transformer token smoke.
The reference must have bounded state, meaningful errors and cleanup. It need
not claim useful trained model behavior or autonomous coding.

### M2 — A useful single-agent coding harness

Integrate selected Hidden Moves tools, bounded context and skill loading,
Backpack run records, existing resumable workflows, and actual verification/
repair. Add a configured Ollama provider without a new HTTP stack. Acceptance
is a small versioned local coding task completed and checked by real tools under
explicit workspace/model/compute policy, including failure and repair cases.

### M3 — Reproducible specialization and optimization

Select data/checkpoints, orchestrate Thoughtformula training and evaluations,
track individual model lineage and memory, and compare bounded harness
configurations against a held-out baseline. Promotion is separate from search.
A model, a being and a harness each retain independent identity/version history.

### M4 — Persistent worlds and optional hierarchical agency

Save/reopen/replay worlds, integrate bounded habitat minds, export selected
experiences with provenance and support controlled collective policies.
One world, one habitat, two beings and an optional environment mind form the
minimum complete scenario. Rule validation remains authoritative.

### M5 — Reusable design system and Warewolf hub

Qualify shared shell/themes/focus/tables with multiple applications, select the
hub manifest and embedding contract, then build Warewolf with two real apps.
Prove navigation, isolation, background cancellation and one terminal restoration.
Native platform claims follow actual terminal evidence.

### M6 — Independent release selections

Select useful versions and compatible released dependencies for each package,
verify namespace/publisher routing and build exact artifacts. Uploads, tags,
releases, weight publication and deployment require separately authorized
concrete operations. Source development does not wait for synchronized releases.

## 8. Delivery batches

Use rolling batches of three to five focused PRs. Start CI as each task is ready
and continue independent work. Suggested first batch: CB-01, CARET-STREAM-01, TFORM-01, HYP-01 and PARA-01. The following batch includes PARA-01,
CA-CLI-01, JSONL-01 and CB-QA-01, plus a demonstrated focused defect if needed.

Same-repository dependencies can stack; cross-repository dependencies use exact
pushed source revisions and reconcile to merged source before qualification.
For the requested child-first squash strategy, first review and qualify each
focused child diff, squash the passing child into its parent, then qualify the
combined parent and squash it into main. Preserve all child issue/PR links in
the parent description and close child tasks only when the combined source is
on main. Do not delete a parent until no open dependent targets it. Never
force-push or rewrite shared history. Independent PRs merge directly after CI.

A failing Git operation stops dependent Git actions until diagnosed. Focused
behavior checks run after changes/conflict resolutions. Existing CI covers
unchanged work. Final main receives a brief installed startup smoke and current
CI receipts; do not duplicate an exhaustive cross-ecosystem local audit.

## 9. Verification strategy

| Surface | Required evidence |
| --- | --- |
| Managed streams | Incremental pre-exhaustion delivery, ordering, finite lead, slow consumer, input/cancel, close on all paths, source/cleanup errors, existing lifecycle tests |
| Thoughtform | Strict immutable definitions, neutral deterministic policy, actual tiny ModernMicroGPT/BPETokenizer stream, EOS/empty/zero/invalid vocabulary/context boundaries |
| Hypnosis | Event identity/order, exactly one normal terminal outcome, total output/event/time limits, consumer cancellation propagation, iterator closure, CLI stdio and safe terminal display |
| Paracosm | Deterministic snapshot observations/order, valid actions, rejected step atomicity, two beings, optional habitat policy, no implicit model import |
| Project generation | Passive render, installable generated app, actual check command, headless/UI shared domain result, existing profiles, matching repeat preserves edits/data, mismatched destination refusal |
| JSONL transport | Real subprocesses for first-record latency, bounded reads/writes, malformed/oversized/truncated framing, broken pipe, stderr, nonzero exit, cancellation and reaping |
| Persistent workflows | Independent-process resume, no replay of committed steps, explicit uncertain retry/restart, exact definition identity |
| Installed family | Wheel/source installs outside source trees, real model adapter, shared CLI/UI outcomes, artifact/source receipts, no optional import leaks |
| Native terminal | POSIX pseudoterminal/actual keyboard and cleanup where supported; synthetic Windows results are labeled separately |
| Optimization/training | Versioned datasets/tasks/splits/seeds/config, verified outcomes, baseline comparison, protected source checkpoint, lineage and explicit promotion |

Use standard-library unittest and temporary resources consistent with these
repositories. No tests that merely mirror constants; exercise the observable
contract and failure boundaries. Newly introduced CI checks should run on Linux,
macOS and Windows where meaningful. Keep network/model downloads out of normal
unit tests. Avoid claiming an offline fixture validates real provider capability.

## 10. Decisions and boundaries

1. Live model use: choose explicit local checkpoint/model endpoint and hardware
   budget before long inference. A tiny random Transformer integration test is
   permitted and makes no capability claim.
2. Training: choose dataset provenance/license, source checkpoint, evaluation
   split, destination and compute/time budget before training on real data.
3. Agent tool authority: select concrete workspace roots and capabilities before
   autonomous coding/tool execution. Provider metadata alone grants no authority.
4. World persistence: select compatible schema/rule identity and retention before
   durable world/experience adoption. Deterministic in-memory stepping is ready.
5. Design system: derive reusable shell pieces from working apps and retain the
   existing Carets layout/renderer/widget issues as their owning roadmap.
6. Warewolf: select two app contracts and trusted activation/embedding before
   creating a separate product repository.
7. Platform: native POSIX terminal support is the initial qualified boundary;
   Windows/headless compatibility does not prove native console interaction.
8. Publication/deployment: public Git repositories are authorized. Package/model
   releases, uploads, paid services and deployment require concrete authorization.

## 11. Work register

The generated register below links owning issues. Project state, issue bodies
and PR verification supersede this planning snapshot for current status.

| Task | Owner | Scope | Depends on |
| --- | --- | --- | --- |
| [CB-01](https://github.com/wispsy/wispsy/issues/24) | `wispsy` | Adopt Cohesion Block B architecture and delivery plan | — |
| [CARET-STREAM-01](https://github.com/wispsy/carets/issues/20) | `carets` | Manage bounded asynchronous message streams | CB-01 |
| [JSONL-01](https://github.com/wispsy/wispsy/issues/14) | `wispsy` | Select bounded JSON Lines streaming and error semantics | CB-01 |
| [TFORM-01](https://github.com/wispsy/thoughtform/issues/1) | `thoughtform` | Define individual models and neutral agency contracts | CB-01 |
| [HYP-01](https://github.com/wispsy/hypnosis/issues/1) | `hypnosis` | Build a bounded runner and Carets application | TFORM-01, CARET-STREAM-01 |
| [PARA-01](https://github.com/wispsy/paracosm/issues/1) | `paracosm` | Establish deterministic world stepping | TFORM-01 |
| [CA-CLI-01](https://github.com/wispsy/compose_application/issues/52) | `compose_application` | Generate application-owned terminal projects | CB-01, CARET-STREAM-01 |
| [CB-QA-01](https://github.com/wispsy/wispsy/issues/25) | `wispsy` | Qualify the first installed model-to-terminal family | HYP-01, PARA-01, CA-CLI-01 |
| [TF-BOUND-01](https://github.com/wispsy/thoughtformula/issues/20) | `thoughtformula` | Qualify token generation budget and context boundaries | — |
| [CARET-FRAME-01](https://github.com/wispsy/carets/issues/21) | `carets` | Coalesce redraws without dropping messages | CARET-STREAM-01 |
| [CARET-DS-01](https://github.com/wispsy/carets/issues/22) | `carets` | Develop application design tokens and shell composition | HYP-01 |
| [CARET-TABLE-01](https://github.com/wispsy/carets/issues/23) | `carets` | Compose terminal table snapshots and selections | CARET-DS-01 |
| [HYP-TOOLS-01](https://github.com/wispsy/hypnosis/issues/2) | `hypnosis` | Bind explicitly selected Hidden Moves capabilities | HYP-01 |
| [HYP-CONTEXT-01](https://github.com/wispsy/hypnosis/issues/3) | `hypnosis` | Retrieve bounded instructions skills and knowledge | HYP-TOOLS-01 |
| [HYP-MEMORY-01](https://github.com/wispsy/hypnosis/issues/4) | `hypnosis` | Persist typed runs and evaluation records | HYP-01 |
| [HYP-WORKFLOW-01](https://github.com/wispsy/hypnosis/issues/5) | `hypnosis` | Compose resumable jobs through existing workflow libraries | HYP-TOOLS-01, HYP-MEMORY-01 |
| [HYP-VERIFY-01](https://github.com/wispsy/hypnosis/issues/6) | `hypnosis` | Implement bounded verification and repair | HYP-CONTEXT-01, HYP-WORKFLOW-01 |
| [HYP-OLLAMA-01](https://github.com/wispsy/hypnosis/issues/7) | `hypnosis` | Integrate an explicitly configured Ollama provider | HYP-01 |
| [HYP-TRAIN-01](https://github.com/wispsy/hypnosis/issues/8) | `hypnosis` | Orchestrate selected Thoughtformula training jobs | HYP-WORKFLOW-01, TFORM-02 |
| [HYP-EVAL-01](https://github.com/wispsy/hypnosis/issues/9) | `hypnosis` | Establish held-out harness evaluations | HYP-MEMORY-01, HYP-VERIFY-01 |
| [HYP-OPT-01](https://github.com/wispsy/hypnosis/issues/10) | `hypnosis` | Optimize harness choices from measured outcomes | HYP-EVAL-01 |
| [HYP-ORCH-01](https://github.com/wispsy/hypnosis/issues/11) | `hypnosis` | Coordinate bounded multi-agent jobs | HYP-WORKFLOW-01, HYP-EVAL-01 |
| [TFORM-02](https://github.com/wispsy/thoughtform/issues/2) | `thoughtform` | Load and specialize named model definitions | TFORM-01, TF-BOUND-01 |
| [TFORM-MEM-01](https://github.com/wispsy/thoughtform/issues/3) | `thoughtform` | Model memories goals and relationships | TFORM-01 |
| [TFORM-COLLECTIVE-01](https://github.com/wispsy/thoughtform/issues/4) | `thoughtform` | Define collective and environment policy composition | TFORM-MEM-01, HYP-ORCH-01 |
| [PARA-SAVE-01](https://github.com/wispsy/paracosm/issues/2) | `paracosm` | Persist snapshots and deterministic replay | PARA-01, HYP-MEMORY-01 |
| [PARA-MIND-01](https://github.com/wispsy/paracosm/issues/3) | `paracosm` | Add optional bounded habitat minds | PARA-01, TFORM-02 |
| [PARA-EXPERIENCE-01](https://github.com/wispsy/paracosm/issues/4) | `paracosm` | Export bounded experiences for evaluation and training | PARA-SAVE-01, HYP-EVAL-01 |
| [CA-CLI-02](https://github.com/wispsy/compose_application/issues/53) | `compose_application` | Compose terminal and API clients over shared services | CA-CLI-01, HYP-TOOLS-01 |
| [WW-01](https://github.com/wispsy/wispsy/issues/26) | `wispsy` | Define Warewolf terminal hub contracts | CARET-DS-01, CA-CLI-02 |
| [WW-02](https://github.com/wispsy/wispsy/issues/27) | `wispsy` | Build the selected Warewolf hub reference | WW-01 |
| [JSONL-02](https://github.com/wispsy/wispsy/issues/28) | `wispsy` | Prove bounded subprocess event transport | JSONL-01, HYP-01 |
| [CB-QA-02](https://github.com/wispsy/wispsy/issues/29) | `wispsy` | Qualify reusable terminal applications across platforms | CB-QA-01, CARET-DS-01, JSONL-02 |
| [REL-B-01](https://github.com/wispsy/wispsy/issues/30) | `wispsy` | Select independent releases and publication profiles | CB-QA-01 |

## 12. Task acceptance register

### CB-01 — Adopt Cohesion Block B architecture and delivery plan

Owner: [wispsy](https://github.com/wispsy/wispsy/issues/24). Phase: Foundation.

Record source inventory, library ownership, dependency direction, contracts, staged milestones and executable acceptance. Preserve the existing composition plan and adopt terminal applications as an additional profile.

- Publish the complete plan with links to every owning task and source baseline.
- Keep existing library floors, APIs and independent release schedules.
- Identify concrete model/data, platform and release decisions.

### CARET-STREAM-01 — Manage bounded asynchronous message streams

Owner: [carets](https://github.com/wispsy/carets/issues/20). Phase: Streaming.

Add Command.stream accepting a trusted asynchronous iterable factory. Forward typed messages through a bounded delivery path owned by Program, with cancellation, closure and explicit errors.

- Prove incremental delivery before exhaustion, ordering, bounded producer lead and input responsiveness.
- Close sources on exhaustion, errors and cancellation; propagate producer errors as CommandErrorMsg.
- Preserve normal commands, post(), terminal cleanup and Python 3.10 support.

### JSONL-01 — Select bounded JSON Lines streaming and error semantics

Owner: [wispsy](https://github.com/wispsy/wispsy/issues/14). Phase: Streaming.

Use live Hypnosis events as the concrete consumer for the existing JSONL-01 selection. Distinguish in-process messages, JSONL records, subprocess lifetime and application completion.

- Specify UTF-8 framing, strict finite JSON, record/total limits, ordering and backpressure.
- Define cancellation, downstream failure, process errors and uncertain partial effects.
- Keep single-document behavior compatible and require subprocess proof before transport support claims.

### TFORM-01 — Define individual models and neutral agency contracts

Owner: [thoughtform](https://github.com/wispsy/thoughtform/issues/1). Phase: Foundation.

Establish model definitions separate from being identity, observation and action contracts. Supply an explicit optional adapter over real Thoughtformula token generators, never a second Transformer or tokenizer.

- Validate immutable model/being configuration and bounded generation choices.
- Demonstrate deterministic policies without importing model or orchestration packages.
- Prove real tiny Transformer token streaming, stop handling and close behavior with exact source receipts.

### HYP-01 — Build a bounded runner and Carets application

Owner: [hypnosis](https://github.com/wispsy/hypnosis/issues/1). Phase: Foundation.

Build a finite run lifecycle with caller-selected async producers, event sequencing, output/time budgets and explicit terminal outcomes. Provide Expose Interface commands and a Carets frontend consuming the same runner.

- Run an offline synthetic source incrementally through both headless and Carets views.
- Prove completion, cancellation, source failure, time/output limits and cleanup without remote services.
- Keep model math, CLI parsing, terminal ownership, general workflows and persistence in their owning libraries.

### PARA-01 — Establish deterministic world stepping

Owner: [paracosm](https://github.com/wispsy/paracosm/issues/1). Phase: Foundation.

Define bounded worlds/habitats and apply validated Thoughtform actions in deterministic actor order. Environment minds remain optional ordinary policies; world rules are authoritative.

- Repeat a seeded/synthetic episode with identical state and events.
- Reject unknown actors, invalid targets and out-of-scope actions before changing authoritative state.
- Support a habitat with two beings and an optional habitat policy without a model dependency.

### CA-CLI-01 — Generate application-owned terminal projects

Owner: [compose_application](https://github.com/wispsy/compose_application/issues/52). Phase: Composition.

Extend existing project generation with an explicit terminal profile using Expose Interface plus Carets. Reuse current safe exclusive creation and selection receipts, leaving service/ui/live profiles compatible.

- Generate runnable check and terminal commands with owned app source.
- Prove repeat generation preserves edited source and refuses mismatched existing destinations.
- Use immutable qualified source selections and validate the generated application outside its source tree.

### CB-QA-01 — Qualify the first installed model-to-terminal family

Owner: [wispsy](https://github.com/wispsy/wispsy/issues/25). Phase: Qualification.

Record immutable selected sources and execute the family from installed wheel/source distributions. Prove the real Thoughtformula adapter, terminal messages, headless CLI and world reference together.

- Retain source/version/artifact fingerprints and use fresh install processes.
- Require cross-platform CI for headless behavior and identify native POSIX terminal limits.
- Document exact passing scope, remaining tasks and final-main startup receipts.

### TF-BOUND-01 — Qualify token generation budget and context boundaries

Owner: [thoughtformula](https://github.com/wispsy/thoughtformula/issues/20). Phase: Streaming.

Review generator limits with executable probes, including zero/negative budgets, empty prompts, EOS, paged caches and context capacity. Correct any demonstrated defects in Thoughtformula itself.

- Prove zero-token requests never run a forward pass.
- Keep standard/speculative/Medusa return semantics explicit and consistent.
- Document context-capacity behavior and keep adapter guards until compatible sources are selected.

### CARET-FRAME-01 — Coalesce redraws without dropping messages

Owner: [carets](https://github.com/wispsy/carets/issues/21). Phase: Design system.

Provide optional frame scheduling for rapid streams. Serialize every model update while rendering at a bounded configurable rate, with a final frame on completion and no hidden token dropping.

- Use a deterministic clock to prove render bounds and final flush.
- Keep keys, resize and cancel responsive under producer pressure.
- Keep immediate rendering as the compatible default.

### CARET-DS-01 — Develop application design tokens and shell composition

Owner: [carets](https://github.com/wispsy/carets/issues/22). Phase: Design system.

Extend the existing coherent-framework issue #10 with application evidence: theme roles, spacing, shell regions, resize, focus, commands, status and error presentation. Reuse current Style, FocusManager and components.

- Define reusable tokens without a second renderer or terminal lifecycle.
- Prove two independent applications compose the same shell primitives.
- Specify narrow-terminal, Unicode, modal focus and accessible textual state.

### CARET-TABLE-01 — Compose terminal table snapshots and selections

Owner: [carets](https://github.com/wispsy/carets/issues/23). Phase: Design system.

Add a terminal table view over Headless Spreadsheets public snapshots and existing tabular contracts. Preserve stable row/column identity and read-only default behavior.

- Reuse typed values and source identity rather than rebuilding a table engine.
- Prove resize, selection and virtualized bounded rendering.
- Keep persistence edits in existing revision-checked source adapters.

### HYP-TOOLS-01 — Bind explicitly selected Hidden Moves capabilities

Owner: [hypnosis](https://github.com/wispsy/hypnosis/issues/2). Phase: Harness.

Accept a caller-provided selected CapabilityCatalog and typed model tool requests. Authorize tools at the application boundary, validate through the catalog and record structural outcomes.

- Unknown/unselected capabilities fail before invocation.
- Arguments/results use public Hidden Moves schema and finite JSON semantics.
- Tool cancellation and uncertain external effects remain explicit; no registry reimplementation.

### HYP-CONTEXT-01 — Retrieve bounded instructions skills and knowledge

Owner: [hypnosis](https://github.com/wispsy/hypnosis/issues/3). Phase: Harness.

Select task-relevant context from explicit roots/providers using the Hidden Moves workspace plugin and Parse MD where needed. Separate trusted instructions from retrieved untrusted content.

- Bound context bytes/tokens and expose truncation and source provenance.
- Never import code or activate providers from document text.
- Measure retrieval against held-out fixture tasks and exclude secrets from receipts.

### HYP-MEMORY-01 — Persist typed runs and evaluation records

Owner: [hypnosis](https://github.com/wispsy/hypnosis/issues/4). Phase: Harness.

Use Backpack Store public codecs/registered models for run metadata, structural events, evaluation summaries and references to caller-owned artifacts.

- Close and reopen records in an independent process.
- Redact credentials and make transcript retention explicit.
- Keep observation history distinct from checkpoint state and model weights.

### HYP-WORKFLOW-01 — Compose resumable jobs through existing workflow libraries

Owner: [hypnosis](https://github.com/wispsy/hypnosis/issues/5). Phase: Harness.

Build typed training/evaluation/tool stages with Moveset and its func_seq adapter; use Scriptty for passive job documents where useful. Do not create another persistent execution engine.

- Resume completed stages without replay.
- Require explicit retry/restart after uncertain interrupted effects.
- Bind source/config/catalog identity into the existing workflow definition version.

### HYP-VERIFY-01 — Implement bounded verification and repair

Owner: [hypnosis](https://github.com/wispsy/hypnosis/issues/6). Phase: Harness.

Define task success criteria and caller-selected verifier tools; use actual failures as repair input under finite attempts, time and output budgets.

- Prove pass, repair success, exhausted budget and verifier failure.
- Never claim success from model narration alone.
- Preserve a reviewable workspace diff and restrict tool authority by selected policy.

### HYP-OLLAMA-01 — Integrate an explicitly configured Ollama provider

Owner: [hypnosis](https://github.com/wispsy/hypnosis/issues/7). Phase: Providers.

Implement streaming chat/tool results using Requ transport and optional Apiconn operation definitions. Keep endpoint/model/auth/timeouts explicit; test with synthetic HTTP before caller-approved local-model use.

- Handle fragmented UTF-8, completion, malformed records, transport errors and cancel.
- Do not introduce a new HTTP client or hosted service.
- Record provider/model/config identity and avoid equating Ollama chat messages with raw token streams.

### HYP-TRAIN-01 — Orchestrate selected Thoughtformula training jobs

Owner: [hypnosis](https://github.com/wispsy/hypnosis/issues/8). Phase: Training.

Prepare caller-selected data, call existing Thoughtformula trainers, evaluate checkpoints and register artifacts. Training algorithms, tensors, optimizers and checkpoint formats remain in Thoughtformula.

- Require explicit dataset provenance/license, checkpoint destination and compute budgets.
- Never overwrite the source checkpoint or promote a result automatically.
- Exercise prepare/train/evaluate/register with a tiny synthetic dataset and interrupted-job recovery.

### HYP-EVAL-01 — Establish held-out harness evaluations

Owner: [hypnosis](https://github.com/wispsy/hypnosis/issues/9). Phase: Optimization.

Define versioned tasks, seeds, splits, verifier outcomes, latency, tool calls, token/compute budgets and reproducible baselines.

- Separate development, selection and held-out test tasks.
- Report success denominators, uncertainty and failures as well as aggregate scores.
- Compare candidates against a fixed baseline under equal budgets.

### HYP-OPT-01 — Optimize harness choices from measured outcomes

Owner: [hypnosis](https://github.com/wispsy/hypnosis/issues/10). Phase: Optimization.

Search bounded explicit harness configurations such as context selection, tools, workflow and repair budget. Store trial provenance and recommend candidates from evidence.

- Never train weights implicitly during a harness trial.
- Keep a held-out regression gate and explicit promotion decision.
- Reproduce a selected result from immutable task/provider/config sources.

### HYP-ORCH-01 — Coordinate bounded multi-agent jobs

Owner: [hypnosis](https://github.com/wispsy/hypnosis/issues/11). Phase: Orchestration.

Add explicit roles, dependencies, resource admission, concurrency and shared budgets using existing scheduling/workflow seams. Start sequentially on limited hardware.

- Prove no concurrency or compute-budget oversubscription.
- Propagate cancellation and preserve child task outcomes.
- Avoid mutable shared model caches without qualified serialization or isolation.

### TFORM-02 — Load and specialize named model definitions

Owner: [thoughtform](https://github.com/wispsy/thoughtform/issues/2). Phase: Models.

Resolve explicitly supplied checkpoints/tokenizers/adapters with stable model identity and lineage. Multiple beings may share a base model while keeping separate context and memory.

- Call public Thoughtformula load/save/training boundaries.
- Validate tokenizer/checkpoint/config compatibility before use.
- Keep artifact resolution passive and never download weights or train on import.

### TFORM-MEM-01 — Model memories goals and relationships

Owner: [thoughtform](https://github.com/wispsy/thoughtform/issues/3). Phase: Agency.

Define versioned domain records and optional Backpack codecs for experiences, goals and relationships. Recall policies use bounded explicit queries.

- Keep being identity stable across restart.
- Separate memory updates from weight updates and world mutation.
- Support deterministic policies and caller-selected external models equally.

### TFORM-COLLECTIVE-01 — Define collective and environment policy composition

Owner: [thoughtform](https://github.com/wispsy/thoughtform/issues/4). Phase: Agency.

Compose individual, group and environment policy roles through the same observation/action contract and explicit information scopes.

- Keep perspective and authority separate.
- Prove group policies cannot bypass world validation.
- Bound delegation depth, actions and shared-model access.

### PARA-SAVE-01 — Persist snapshots and deterministic replay

Owner: [paracosm](https://github.com/wispsy/paracosm/issues/2). Phase: Worlds.

Use Backpack Store for typed snapshots and world events, including schema/rules/seed/source identity. Support pure headless save/reopen/replay.

- Reopen and replay in separate processes with identical accepted state.
- Detect incompatible rules/schema versions before applying events.
- Do not treat model narration or harness logs as authoritative world state.

### PARA-MIND-01 — Add optional bounded habitat minds

Owner: [paracosm](https://github.com/wispsy/paracosm/issues/3). Phase: Worlds.

Represent environment minds as ordinary Thoughtform policies proposing environmental actions that Paracosm validates against declared rules.

- Run one habitat and two beings with or without a habitat policy.
- Prove rejected proposals preserve authoritative state.
- Share base models optionally without requiring a model per habitat.

### PARA-EXPERIENCE-01 — Export bounded experiences for evaluation and training

Owner: [paracosm](https://github.com/wispsy/paracosm/issues/4). Phase: Worlds.

Export versioned observations, proposals, accepted actions and outcomes with provenance for caller-selected evaluation/training jobs.

- Separate simulated claims from verified outcomes.
- Require explicit data selection/retention and split lineage.
- Keep exports deterministic and reject incompatible schemas.

### CA-CLI-02 — Compose terminal and API clients over shared services

Owner: [compose_application](https://github.com/wispsy/compose_application/issues/53). Phase: Composition.

Demonstrate one application service with direct Python, Expose Interface commands, Carets views and optional Expose API transport. Reuse shared contracts and keep presentation state local.

- Keep CLI parsing and HTTP policy in their existing libraries.
- Prove equivalent results and cleanup across selected interfaces.
- Keep web/browser profiles independent and optional.

### WW-01 — Define Warewolf terminal hub contracts

Owner: [wispsy](https://github.com/wispsy/wispsy/issues/26). Phase: Hub.

Select the application manifest, explicit entry-point discovery, trusted activation, navigation, shared services and embedding contract for Warewolf as a Carets application and hub.

- Embed components under one Program and one terminal owner.
- Separate external-process apps from in-process component apps.
- Select a concrete first pair of applications before creating a product repository.

### WW-02 — Build the selected Warewolf hub reference

Owner: [wispsy](https://github.com/wispsy/wispsy/issues/27). Phase: Hub.

Compose two explicitly selected terminal applications with shared theme/focus/navigation and independent app state; provide a bounded external-process bridge only if selected.

- Switch apps without losing state or leaking background jobs.
- Restore terminal state once on quit/error/cancel.
- Keep plugins opt-in and installations separate from activation.

### JSONL-02 — Prove bounded subprocess event transport

Owner: [wispsy](https://github.com/wispsy/wispsy/issues/28). Phase: Streaming.

Implement the selected record contract through the appropriate transport owner and an actual producer/consumer subprocess reference. Keep the in-process Carets stream adapter independent.

- Prove first record arrives before producer exits.
- Prove malformed/oversized records and downstream closure stop upstream work.
- Report partial effects, timeout, cancellation and nonzero producer exit without false completion.

### CB-QA-02 — Qualify reusable terminal applications across platforms

Owner: [wispsy](https://github.com/wispsy/wispsy/issues/29). Phase: Qualification.

Qualify source/wheel profiles, terminal restoration, process streaming, Unicode/resizing and independent applications across declared platform capabilities.

- Distinguish synthetic Windows tests from native terminal evidence.
- Record exact versions, hashes and platform limitations.
- Keep unaffected published/library profiles compatible.

### REL-B-01 — Select independent releases and publication profiles

Owner: [wispsy](https://github.com/wispsy/wispsy/issues/30). Phase: Release.

Select useful package versions, namespaces, licenses, compatible released dependencies, artifacts and authenticated publisher routing independently for each package.

- Require a separately authorized concrete package upload or release.
- Do not equate public source repositories with PyPI ownership or availability.
- Do not deploy models, services, sites or weights as part of source development.

## 13. Inspected source baseline

These are source revisions, not synchronized package releases. Ancillary entries
are an inventory of inspected local sources and must be requalified before an
integration pins them. The first installed-family receipt selects exact merged
sources separately.

| Component | Baseline | Evidence |
| --- | --- | --- |
| Carets | `e4b5314ecc5459288585d52370e36ee57507ab1f` | Runtime/commands/focus/forms/terminal/tests inspected |
| Thoughtformula | `d61dca801b4adb3addf8f72282d87281ca091f19` | Actual generators, tokenizer, context limit, public exports inspected |
| Wispsy | `530bac98059eb1de71cd09a5645c52647457611b` | Existing composition architecture and JSONL-01 queue retained |
| Compose Application | `8c17590a9d3bfc4285b0f8705b19e0e2ba50d18b` | Existing exclusive project creation and fixed web reference selection inspected |
| Expose Interface | `8c71caefe67217bb6df87e280261746a3055fc86` | Current main identity verified; callable command API inspected |
| Moveset | `95acbde15881ca9d3ca833c16bc6c93b44687fbc` | Existing linear pipelines and func_seq compilation source inventory |
| func_seq | `b1a5346feeeef3fa1f398e4dcd81c2d23345386c` | Existing pause/resume and uncertain-effect recovery contract |
| Scriptty | `f7e1d35f27f997a2e30c6f04f3626f05d8be10cf` | Selected catalogs, commands and terminal composition patterns inspected |

New repositories begin from preserved uv project seeds at Python 3.14+ and
version 0.1.0. No package publication is implied. Project issues and source PRs
record subsequent implementation and exact test receipts.
