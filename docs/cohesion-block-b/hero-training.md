# Hero: homegrown model and training implementation plan

Selected on 20 November 2026. This chapter extends Cohesion Block B with Hero,
her Hero Coding specialization, Engl, explicit dataset-source review and an
end-to-end homegrown training milestone. It adopts the supplied curriculum,
English lexical/AST and Wikipedia-reference design notes as design input.
Illustrative APIs and earlier model-size projections are not shipped contracts
or evidence of useful model ability.

The [Project](https://github.com/orgs/wispsy/projects/28) and linked issues own
scope, dependencies and current state. [Engl](https://github.com/wispsy/engl)
has its own [language-foundations Project](https://github.com/orgs/wispsy/projects/29).
The existing thoughtformula roadmap retains numerical/model ownership.

## Selected outcome and priorities

- `hero`: an experimentally trained general-language/general-knowledge model and
  agent identity, starting from random Thoughtformula weights.
- `hero-coding`: a separately identified coding specialization of a selected
  Hero checkpoint, with explicit parent/recipe/data lineage.
- Hypnosis: the application that prepares approved corpora, operates training,
  evaluates results, records typed receipts and exposes progress through Carets.
- Engl: independent English lexical, morphological, dependency and later
  semantic representations, usable without a model or harness.

The immediate target task is operating model training through the harness.
Connecting an Ollama model and externally selected tools is a later path.
A completed pilot produces actual learned checkpoint artifacts and measured
results; it does not establish a general assistant or autonomous coding agent.
No candidate is promoted merely because training completed.

## Source selection is a first-class contract

The priority is internally authored/generated material, then open external
sources, then other sources only after explicit selection. The owner reviews
all new sources, including coding data, teacher outputs, vault snapshots and
new generator recipes. A source being readable, public or locally stored does
not silently add it to the approved training mixture.

[HYP-SOURCE-01](https://github.com/wispsy/hypnosis/issues/13) records the concrete
source catalog, pilot examples and decisions. The internally generated v1
arithmetic/Python recipe was explicitly approved for this pilot on 20 November.
Its approved families are addition, multiplication, parity filtering and list
aggregation. Preserve generator/version/seed identity and independently verify
the authored expected results and tests. Expanding source families needs another
selection; generated text derived from an external source retains that lineage.

The following local downloads were selected by the owner:

| Source | Available input | First use |
| --- | --- | --- |
| TinyStories | V1 train and validation text; downloaded README and commit metadata | Bounded narrative training and held-out language evaluation |
| Simple English Wikipedia | bz2 multistream XML plus bz2 offset/page/title index | Bounded simple factual prose and citation-preserving extraction |
| English Wikipedia | bz2 multistream XML plus bz2 index; separate article shard | Later knowledge expansion; bounded indexed samples now |
| Wiktionary/Wiktextract | gzipped JSONL, multiple languages | Explicit English lexical/morphological normalization |
| UD English EWT | CoNLL-U train/dev/test and repository license/readme | Annotated dependency records and linguistic fixtures |

The directory actually inspected is `Documents/Projects/_datasets` under the
owner's home. Runtime manifests take an explicit dataset root; public source
never depends on that private absolute path. TinyStories is the dataset present,
rather than the name SimpleStories. Local TinyStories metadata matches Hub
revision `f54c09fd23315a6f9c86f9dc80f725de7d8f9c64`; its card declares
`cdla-sharing-1.0`. Three downloaded entries are empty placeholders and must be
reported/excluded rather than treated as valid empty training sets. V1/V2
TinyStories overlaps are not mixed across training/evaluation.

Record source terms and attribution alongside each selection. UD's annotations
and underlying text have distinct provenance described by its README. Preserve
Wikimedia/Wiktionary attribution and share-alike information; do not relabel
external data as repository MIT source. Public source development does not
publish corpora, derived datasets or weights.

### Candidate source path

The growing `vaults/python3` is an explicitly proposed source. The inspected
snapshot has 2,486 Markdown files, about 2.9 MB, including authored notes and
pages citing Python documentation. Propose an exact file allowlist, retain each
file's references/authorship classification and record content hashes. New or
changed files must not silently enlarge the approved snapshot. Keep vault text
local. Use Parse MD's public document/code interfaces for Markdown selection.

`wiki.python.org` is a separate candidate from `docs.python.org`. Select the
community wiki's exact pages/snapshot/terms independently. For official Python
docs, propose a version-pinned tutorial/language/built-in/standard-library subset
and retain the PSF and code-example licensing information. Do not start a bulk
crawler or add either candidate to training before selection.

For future general knowledge material, seek readable explanations with stable
source/revision identity, supporting facts and checkable questions. For coding,
seek explanations plus runnable examples, exercises, tests and debugging pairs.
Other code repositories, textbooks, commercial content and teacher APIs remain
unselected until their concrete source scope is approved.

## Component responsibilities and reuse

| Owner | Selected responsibility | Reuse boundary |
| --- | --- | --- |
| Engl | Lexemes, senses, forms, POS, dependency annotations and future semantic relations | Standard-library bounded import; optional adapters; no model math/storage engine |
| Thoughtformula | Transformer/tokenizer, loss/autograd/Adam, bounded pretraining/evaluation, lossless training state | Reuse FlatTensor and ModernMicroGPT; preserve existing quantized inference formats |
| Thoughtform | Hero/Hero Coding recipes, local model artifact resolution, tokenizer/config compatibility and lineage | Public Thoughtformula artifact APIs; no independent trainer or checkpoint codec |
| Hypnosis | Source approval, corpus streams, curriculum order, jobs, resource policy, evaluation and experiment records | Existing Carets, Expose Interface, Backpack and func_seq services |
| Backpack Store | Typed durable run/metric/artifact-reference records | Explicit codecs, close/reopen and checked updates; no second SQLite schema engine |
| func_seq | Persistent stage lifecycle and uncertain-effect recovery | Prepare/train/evaluate/register trusted callables with exact definition identity |
| Moveset/Scriptty/Hidden Moves | Later selected-catalog job/tool composition | Keep existing interfaces; the initial direct training workflow does not need tool activation |
| Parse MD | Markdown/code selection for an approved vault snapshot | Do not write another Markdown parser |
| Astree | Existing HTML tree/selector/extraction boundaries | It currently parses HTML; linguistic syntax/semantics belong in Engl |
| Carets | One terminal owner and live bounded presentation | Reuse managed streams; numerical work stays off the event loop |
| Pocket Python | Future separately qualified code-exercise execution profile | Initial authored fixtures use the selected CPython; no new interpreter is written |

Wikipedia is Wikitext, not Markdown or HTML. Use a selected Wikitext parser for
markup/citation nodes rather than pretending Parse MD/Astree parses that language.
The initial optional data profile uses mwparserfromhell 0.7.2, confined to the
Wikipedia adapter. Standard XML/bz2/gzip/JSON readers remain incremental and
bounded. No new model framework, hosted service or HTTP client is introduced.

## Engl contracts

A lexeme retains a stable source-qualified identity, lemma, native POS and
explicit mapping to UD POS where known, multiple senses, glosses, examples and
tagged forms. Filter `lang_code == en` explicitly. Preserve ambiguity rather
than collapse every spelling into one meaning. Comparative/superlative degree
is grammatical; it is not intensity or a universal numerical sentiment score.
Relations and calibrated semantic dimensions are later separately evidenced data.

CoNLL-U import validates ten columns, bounded basic word IDs, a single root,
head references and acyclicity. Retain multiword/empty-node metadata and enhanced
annotations without confusing those with basic tree nodes. An annotated-tree
reader is not a parser for arbitrary unannotated English. The next Engl task
selects simple clauses/negation/comparison representations and their evaluation.

## Bounded corpus and citation extraction

The inspected 27 GB compressed full-Wikipedia dump does not need full extraction
for this pipeline. Both real multistream indexes successfully selected and
independently decompressed a 100-page block. Index records use byte offset,
page ID and page title. Validate nondecreasing offsets, dump bounds, compressed
and expanded block ceilings, XML/entity handling and page/revision identity.
A mismatched/invalid index is an error, not permission to decompress everything.

Limit records, scanned bytes, compressed/expanded blocks, document text, output
bytes and retained memory. Inspect input size/version and detect changes during
preparation. Source-stat/sample checks are labeled as such; they are not a
full-file cryptographic verification. Hash the exact selected corpus and selected
compressed blocks/records for reproducibility. Do not hash/read all 27 GB just
to build a small first sample. Never modify or extract over the source downloads.

Keep page IDs, revision IDs, source URLs, raw text identity, inline citation
markers, reference definitions and URLs/DOIs. Cleaned prose and original reference
relationships are separate data. Preserve named/reused references and label
unresolved references. A citation is a relationship, not a verified support verdict.
Bound/truncate excerpts explicitly and record truncation; do not silently present
partial evidence as the full article. No reference URL is fetched automatically.

TinyStories streams split on the actual end-of-text delimiter and preserve the
provided validation source. UD train/dev/test retains the repository split.
Group Wikipedia revisions/related topic sources and future reference documents
before assigning training/validation/test. Deduplicate exact selected content
across the selected mixture; all derived chunks inherit their parent group split.
Evaluation material never enters tokenizer fitting or training sample construction.

## Reproducible model training and artifacts

Expose pretraining/evaluation in Thoughtformula over existing numerical methods.
Validate finite integer/float limits, vocabulary IDs, context length, token/step
budgets, elapsed time and callback/cancellation boundaries. Use token-weighted
negative log likelihood and explicit token counts; detect nonfinite state.
Do not silently drop unsupported tokenizer text in held-out evaluation: report
coverage or fail the selected profile. A predeclared ASCII/code alphabet is
permitted; fitting still uses only training material, never held-out examples.

The existing inference checkpoints quantize weights and omit Adam moments.
They are useful inference artifacts but cannot establish exact training resume.
Add a versioned lossless native training artifact with float64 parameters, Adam
moments/counters, tokenizer/config identity and training progress. Validate
manifest/shape/entry/byte limits, avoid pickle, write atomically and preserve
source artifacts. Resume must match uninterrupted training under fixed data,
seed/order/config. A specialization is a new run: retain parent weights and
lineage while explicitly resetting optimizer/progress where its recipe says so.

Hero and Hero Coding use the same qualified Transformer/tokenizer foundation.
A coding child cannot silently change vocabulary or claim an unrelated model
as its parent. Store model IDs, recipe versions, artifact hashes, tokenizer
fingerprint, corpus/split/approval identities, training-source revisions and
parent artifact identities. Registration records an experimental candidate;
it does not automatically promote a default model or publish weights.

## Harness workflow and application

Use func_seq prepare/train/evaluate/register stages. Bind corpus/config/recipe
and exact source identities into the workflow definition version. Resume saved
completed stages without replay. An interrupted stage can have partial effects;
ordinary resume refuses uncertain state and retry/restart stays explicit.
Thoughtformula's training checkpoint provides numerical resume within a selected
stage; it does not replace func_seq's job state. Backpack stores typed structural
run/evaluation/artifact records; it does not replace either checkpoint format.

Expose the same job through Python, Expose Interface commands and a Carets
training view. Keep input/cancel/resize responsive; one Program owns the terminal.
Use bounded progress events and caller-owned local artifact directories. Record
source/checkpoint paths locally and keep public receipts free of private vault
text or credentials. Time limits are cooperative at numerical boundaries unless
an explicitly owned worker process supplies a hard termination boundary.

## First experiment and acceptance

The combined first local training experiment is capped at 15 minutes, selected
by the owner. Benchmark a small architecture first on the actual 16 GiB machine;
record parameter count and measured throughput before scaling. Earlier 1–5M,
10–30M and larger model suggestions are research targets, not feasible-throughput
claims for a pure-Python implementation. Select a measured pilot architecture,
retain full-precision training artifacts and a compatible inference export.

Run an approved staged curriculum and a seeded shuffled comparison over the same
selected training material, with matched step/token budgets where possible.
Continue a selected Hero checkpoint into the approved Hero Coding curriculum.
Report actual completed steps/tokens/runtime, initial/final train/held-out losses,
coverage and small-sample limits. Keep selection/held-out test data independent.
The small pilot supports pipeline validation and preliminary learning evidence;
no coherent-story, factual-reasoning or functional-coding claim follows solely
from lower language loss or syntactically valid output.

Start the bounded job only after the selected data/config artifacts exist. Report
its actual scheduled stop time in PST. While it runs, continue CI, documentation
and integration work, then collect results. Raw datasets, vault snapshots and
checkpoint weights remain local in ignored artifact directories. Publish only
selected source code and bounded structural/aggregate experiment receipts.

## Subsequent curriculum and evidence work

Progress from lexical/grammar/narrative foundations to knowledge, verifiable
reasoning, instruction, agentic trajectories and specialization, keeping replay
mixtures and regressions explicit. These are measured stages, not guaranteed
capabilities inferred from model size. New textbooks, code, teachers, curricula,
experiential sources and evaluation benchmarks pass source selection first.

Wikipedia/reference curricula preserve claim-to-reference relationships and
allow supported, partial, contradicted and insufficient-evidence outcomes.
Reference-to-summary, retrieval, synthesis and verification are different tasks;
summary-to-reference is not lossless reconstruction. Review exact lawful
reference collections and topic/source holdouts before retrieval. A visible
abstract is not automatically selected training content. Later source-approved
Wikidata/WordNet data can extend semantic records without forcing a model to
memorize every lexical relationship.

## Selected work register

| Task | Owner | Result | Prerequisites |
| --- | --- | --- | --- |
| [HERO-PLAN-01](https://github.com/wispsy/wispsy/issues/35) | `wispsy` | Define Hero homegrown curriculum and source-selection roadmap | — |
| [HYP-SOURCE-01](https://github.com/wispsy/hypnosis/issues/13) | `hypnosis` | Review and approve Hero curriculum sources | HERO-PLAN-01 |
| [ENGL-01](https://github.com/wispsy/engl/issues/1) | `engl` | Normalize English lexical and dependency records | HERO-PLAN-01 |
| [HYP-DATA-01](https://github.com/wispsy/hypnosis/issues/14) | `hypnosis` | Build bounded approved corpus streams | HYP-SOURCE-01, ENGL-01 |
| [TF-BOUND-01](https://github.com/wispsy/thoughtformula/issues/20) | `thoughtformula` | Qualify token generation budget and context boundaries | — |
| [TF-TRAIN-01](https://github.com/wispsy/thoughtformula/issues/21) | `thoughtformula` | Expose bounded pretraining and lossless training checkpoints | TF-BOUND-01 |
| [TFORM-02](https://github.com/wispsy/thoughtform/issues/2) | `thoughtform` | Load and specialize named model definitions | TFORM-01, TF-BOUND-01, TF-TRAIN-01 |
| [HYP-MEMORY-01](https://github.com/wispsy/hypnosis/issues/4) | `hypnosis` | Persist typed training runs and evaluation records | HYP-01 |
| [HYP-WORKFLOW-01](https://github.com/wispsy/hypnosis/issues/5) | `hypnosis` | Compose resumable homegrown training jobs | HYP-MEMORY-01 |
| [HYP-CURRICULUM-01](https://github.com/wispsy/hypnosis/issues/15) | `hypnosis` | Build approved internally generated curriculum material | HYP-SOURCE-01, HYP-DATA-01 |
| [HYP-TRAIN-01](https://github.com/wispsy/hypnosis/issues/8) | `hypnosis` | Orchestrate selected Thoughtformula training jobs | HYP-WORKFLOW-01, HYP-DATA-01, TFORM-02, HYP-CURRICULUM-01 |
| [HYP-EVAL-01](https://github.com/wispsy/hypnosis/issues/9) | `hypnosis` | Establish held-out homegrown training evaluations | HYP-DATA-01, TF-TRAIN-01 |
| [HERO-PILOT-01](https://github.com/wispsy/hypnosis/issues/16) | `hypnosis` | Run and record the first Hero and Hero Coding candidates | HYP-TRAIN-01, HYP-EVAL-01 |
| [HERO-QA-01](https://github.com/wispsy/wispsy/issues/36) | `wispsy` | Qualify installed Hero training and curriculum composition | HERO-PILOT-01, ENGL-01 |
| [ENGL-02](https://github.com/wispsy/engl/issues/2) | `engl` | Develop grounded English semantic representations | ENGL-01 |
| [HYP-EVIDENCE-01](https://github.com/wispsy/hypnosis/issues/17) | `hypnosis` | Select citation-linked knowledge and evidence curricula | HYP-DATA-01, HYP-SOURCE-01 |
| [HYP-VAULT-01](https://github.com/wispsy/hypnosis/issues/18) | `hypnosis` | Review and snapshot the growing Python vault curriculum | HYP-SOURCE-01, HYP-DATA-01 |

## Owning-task acceptance

### HERO-PLAN-01: Define Hero homegrown curriculum and source-selection roadmap

Adopt the three new model/language/citation notes, Hero and Hero Coding identities, Engl ownership, approved local sources and a bounded training milestone. Defer the Ollama/connected-tool path.

- Record source approval, corpus provenance/splits, numerical training/checkpoint ownership and model lineage.
- Link the existing training/artifact/workflow tasks rather than duplicate them.
- Define actual local pilot acceptance, capability limits and future dataset/evidence decisions.

### HYP-SOURCE-01: Review and approve Hero curriculum sources

Implement the explicit dataset-source selection process: internally authored/generated materials first, then open external sources, then other sources only after selection. Local python3 vault and Python wiki/docs are candidates until reviewed.

- Record approval before any new source or generator recipe enters training.
- Reject unapproved sources and changed vault snapshots at ingestion.
- Preserve provenance/rights/version and official/grouped held-out split identity.

### ENGL-01: Normalize English lexical and dependency records

Build independent typed English lexical/morphological records from bounded Wiktextract JSONL and validated dependency trees from CoNLL-U. Keep degree, polarity and intensity distinct, without invented universal word scores.

- Preserve lemmas, POS, multiple senses, tagged inflections and source identity; filter English explicitly.
- Validate basic dependency roots, references and cycles while retaining multiword/empty-node metadata.
- Provide real bounded local import receipts and source/wheel tests without a model dependency.

### HYP-DATA-01: Build bounded approved corpus streams

Read approved TinyStories, indexed Wikipedia bz2 blocks, Wiktionary and UD inputs incrementally. Preserve raw/prose/citation provenance, document IDs, deduplication and split isolation, producing bounded local corpus manifests.

- Prove indexed Wikipedia reads without extracting the full dump; reject invalid offsets/oversized blocks.
- Skip/report incomplete zero-byte downloads and preserve official TinyStories/UD held-out splits.
- Fit tokenizer inputs from training selections only; retain reference markers and page revisions.

### TF-BOUND-01: Qualify token generation budget and context boundaries

Complete the existing generation boundary task before exposing trained local artifacts.

- Prove zero-token requests perform no forward pass and invalid budgets fail explicitly.
- Keep standard/speculative/Medusa streaming and nonstream return shapes compatible.
- Bound context capacity and qualify exact supported sources.

### TF-TRAIN-01: Expose bounded pretraining and lossless training checkpoints

Extract reusable pretraining/evaluation over existing tensor/autograd/Adam operations and add atomic lossless float64/optimizer checkpoints for exact resume. Keep the existing quantized inference checkpoint interface intact.

- Bound steps/tokens/context/time, support cooperative stop and report finite token-weighted loss.
- Prove interrupted/resumed training matches uninterrupted training, including Adam moments and counters.
- Reject incompatible or malformed artifacts before unbounded allocation; do not implement model math elsewhere.

### TFORM-02: Load and specialize named model definitions

Complete local artifact resolution and define explicit Hero generalist and Hero Coding child recipes. Validate model/tokenizer/config identity and preserve full checkpoint/parent lineage.

- Load compatible local artifacts using public Thoughtformula APIs without downloads or inference on import.
- Distinguish exact training resume from a new specialization with reset optimizer state.
- Keep Hero and Hero Coding independently identifiable and register only measured experimental candidates.

### HYP-MEMORY-01: Persist typed training runs and evaluation records

Complete the existing typed run record task using Backpack Store public codecs, including approved corpus/config/artifact references and bounded training/evaluation receipts.

- Close/reopen typed records in an independent process.
- Keep transcripts optional and exclude credentials/raw corpora from structural receipts.
- Record run/parent/source identity without introducing another database or checkpoint engine.

### HYP-WORKFLOW-01: Compose resumable homegrown training jobs

Adopt func_seq for explicit trusted prepare/train/evaluate/register stages. The first homegrown training profile does not require external tools or a capability catalog; selected-catalog composition remains a later adapter.

- Resume committed stages without replay.
- Retain explicit retry/restart for uncertain interrupted effects.
- Bind exact corpus, recipe, source and configuration identity into the existing workflow version.

### HYP-CURRICULUM-01: Build approved internally generated curriculum material

Version the reviewed internal arithmetic and Python exercise recipe, deterministic verification and train/validation/test selections. Support staged order versus a seeded shuffled baseline over the same material.

- Only generate training selections from the approved recipe and source snapshot.
- Verify authored exercise answers/code tests and keep held-out examples separate.
- Report generator/version/seed/data identity; do not relabel derived external material as original.

### HYP-TRAIN-01: Orchestrate selected Thoughtformula training jobs

Complete the selected homegrown prepare/train/evaluate/register workflow with bounded local resources, explicit destinations, progress in the Carets application and exact lineage.

- Train Hero from random initialization and specialize Hero Coding from her selected checkpoint using approved data.
- Preserve source checkpoints, enforce output/resource limits and support interrupted-job recovery.
- Use Thoughtformula training/checkpoints, Thoughtform recipes, Backpack receipts and func_seq lifecycle.

### HYP-EVAL-01: Establish held-out homegrown training evaluations

Complete the first provider-independent evaluation profile with fixed splits/seeds, token-weighted losses/perplexity, tokenizer coverage, bounded syntax probes and matched-budget curriculum/shuffle baselines.

- Keep development/selection/test material and source groups separate.
- Report denominators, token/step/time budgets, failures and small-sample uncertainty.
- Do not claim factual accuracy, functional coding success or autonomous agent ability from language loss/syntax alone.

### HERO-PILOT-01: Run and record the first Hero and Hero Coding candidates

Execute the approved local pilot within a combined 15-minute training budget, with a measured architecture, curriculum/shuffle evidence and a coding specialization when its source recipe is approved.

- Retain reproducible corpus/model/source identities and before/after held-out metrics.
- Produce reloadable lossless/inference artifacts and typed run receipts without automatic promotion or upload.
- Record actual parameter/step/token/runtime totals and remaining capability/data requirements.

### HERO-QA-01: Qualify installed Hero training and curriculum composition

Qualify exact merged source/wheel profiles for corpus preparation, approved source admission, training resume, model lineage, persistent jobs and CLI/Carets progress.

- Retain independent-process source/artifact receipts and Linux/macOS/Windows checks.
- Keep full external corpora/weights out of source artifacts and standard CI.
- Verify final main startup and document concrete next source/model-scale decisions.

### ENGL-02: Develop grounded English semantic representations

Extend lexical/dependency records toward simple clauses, negation and comparisons, preserving syntactic annotations alongside explicit semantic relations. Select parser/lexicon additions with source approval.

- Keep comparative degree separate from intensity and calibrated semantic dimensions.
- Represent ambiguity and absent evidence explicitly.
- Reuse Astree at HTML boundaries; do not turn its HTML core into a language model or dictionary.

### HYP-EVIDENCE-01: Select citation-linked knowledge and evidence curricula

Prepare a source-approved claim/reference curriculum using preserved Wikipedia citation links. Select exact lawful reference sources and topic/source-group held-out evaluation before collection.

- Keep claim/support relations distinct from equal-fact or reversible-text assumptions.
- Preserve DOI/URL/revision/licensing and citation-to-claim alignment.
- Do not automatically crawl every reference or assume an accessible abstract is reusable training material.

### HYP-VAULT-01: Review and snapshot the growing Python vault curriculum

Propose exact allowlisted python3 vault files and a content-hashed snapshot, distinguishing authored notes from documentation-derived excerpts. Reuse Parse MD for structured Markdown and code sections.

- Get an explicit selection before consuming candidate vault material for training.
- Detect added/changed files without silently enlarging the approved snapshot.
- Keep private vault text local and retain original per-file references and rights.

