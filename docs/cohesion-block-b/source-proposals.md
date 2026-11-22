# Proposing the next training material

Priority remains our authored/generated materials, then explicitly approved open
sources, then other sources only after a concrete selection. A readable file or
public page is a candidate, not automatic training input. New snapshots and
generator revisions also need selection.

[HERO-SOURCE-02](https://github.com/wispsy/hypnosis/issues/27) records the owner's
21 November approval of the current Python vault/tutorials, community wiki clone
and Python 3.14 docs. The [session plan](hero-training.md#session-v2-approved-python-materials-and-longer-checkpointed-experiments)
selects exact snapshots, weights and a one-hour ceiling. This guide describes
future proposals; it does not automatically admit new material.

## Useful first materials

| Material | What to supply | How it can be checked |
| --- | --- | --- |
| Authored general knowledge | A concept, a plain explanation, contrasting examples and short questions; references for factual claims | Topic-held-out questions, source provenance and reviewed expected answers |
| Authored Python lessons | One skill per lesson, runnable reference examples, expected results and boundary cases | CPython tests of the authored reference; separate held-out inputs |
| Generated exercises | Exact templates, parameter ranges, answers/tests, difficulty and recipe version | Deterministic rebuild and independently verified answers |
| Local Python vault | An explicit file allowlist, content hashes and an authorship/reference classification | Snapshot changes and per-file provenance; growth does not enlarge the selection |
| Official Python docs | Exact version/pages, intended skills and terms/attribution | Versioned snapshot and documentation/example provenance |
| Python community wiki | Its own exact page allowlist, snapshot and terms | Separate rights/provenance review; no assumption that docs and wiki share terms |

For general knowledge, begin with explanations and worked examples that you want
Hero to learn to express. Distinguish a definition, an interpretation and a factual
claim. Preserve supporting references and uncertainty rather than inventing facts
to fill a dataset. Claim/reference training has its own [source-selection task](https://github.com/wispsy/hypnosis/issues/17).

For coding, useful early skills include reading expressions, variables, functions,
conditionals, loops and collections. Each selected lesson should include normal
and boundary behavior. Negative/zero/empty examples and new exercise families
belong in a reviewed recipe revision rather than silently changing v1. Generated
model code is not executed merely because an authored reference has tests.

## Review record

For each proposal, record these fields in the owning issue:

1. Goal and specific skill or topic.
2. Exact local files, page/version allowlist or generator recipe.
3. Original authorship versus quoted/derived material, with source and rights.
4. Expected answers or authored reference tests and who reviews them.
5. Concept/problem/source groups that must stay together across splits.
6. Desired training proportion, document/window limits and tokenizer coverage.
7. Whether local use, redistribution and model-weight publication are selected
   separately. Approval for training does not publish the source or checkpoint.

Every new run should select source/window quotas explicitly. A prepared corpus can
contain more documents or source types than a bounded model run actually consumes.
Report that distinction, unknown-token exclusions and held-out denominators.
Training time is a separate finite decision. The selected v2 session includes
the matched v1 comparison within its one-hour combined ceiling; future sessions
need a newly selected finite progression.
