# Homegrown training qualification

This profile qualifies installed composition of Engl, Thoughtformula,
Thoughtform and the Hypnosis training application. It is independent of the
earlier terminal/world family profile and its immutable source register.

## Reproduce

Use Python 3.14+, build this repository, and install the explicitly selected
training profile in temporary environments outside all source checkouts:

```sh
uv build --out-dir dist
python scripts/qualify_hero.py dist
```

The [source register](hero-sources-v1.json) selects exact Git revisions for
Hypnosis and every component in its training profile. The qualifier installs
both wheel and source artifacts, verifies PEP 610 source identities, checks
dependencies and prints version/source/artifact receipts. Local receipts stay
in ignored `hero-qualification.json`; CI retains one receipt artifact per
platform and prints it in the job log. Linux, macOS and Windows run the same
installed fixture.

## Qualified contracts

- Engl normalizes authored English lexical records and basic CoNLL-U dependencies
  without importing a model or harness.
- Corpus preparation admits selected source IDs and rejects candidates. Related
  authored problem variants share a deterministic split group. Raw external
  datasets are not part of the source distribution or standard CI.
- Hero starts from a named recipe; Hero Coding loads a fresh selected Hero parent,
  preserves its architecture/tokenizer and starts a new optimizer trajectory.
  Parent checkpoint bytes remain unchanged.
- Hypnosis composes existing func_seq stage progress, Thoughtformula numerical
  state and Backpack typed receipts. Exact resume and new specialization remain
  distinct. Completed stages reopen without repeated training. Cooperative pause/
  retry is qualified. A force-killed process may leave a func_seq ownership lock;
  inspect its recorded owner before manually clearing a confirmed stale lock.
  Retry authority does not bypass a live writer or remove locks automatically.
- Passive local artifacts bind recipe, tokenizer, corpus, native checkpoint and
  parent identities. Installed fresh-process receipt reads preserve those links.
- Hypnosis's own installed training suite additionally verifies real commands,
  Carets progress, cooperative worker joining, nonzero-step pause/retry, bounded
  source preparation and strict completed-job result recollection.

## Evidence and limits

The local pilot produced experimental Hero and Hero Coding artifacts. Native
training and quantized inference formats remain separate. Raw source material
and weights stay outside Git. The owner-approved sanitized
[pilot report](https://github.com/wispsy/hypnosis/tree/main/experiments/hero-pilot-v1)
contains measurements and hashes without training text or weights. The matched
shuffle comparison remains open in [HERO-PILOT-01](https://github.com/wispsy/hypnosis/issues/16).
No curriculum advantage or model promotion is inferred from installed fixtures.

The probes measure next-token loss/coverage and syntax only. They do not prove
factual accuracy, working generated code, useful assistant behavior or autonomous
operation of training tools. Windows qualifies headless/test presentation; native
console support remains the separate Carets contract.

The owner selected the current vault/tutorials, official Python 3.14 docs and
community wiki clone on 21 November in [HERO-SOURCE-02](https://github.com/wispsy/hypnosis/issues/27).
The independent [v2 profile](hero-session-qualification.md) covers balanced
sampling, history and continuation without changing this v1 source register.
[The proposal guide](source-proposals.md) continues to govern future material.
