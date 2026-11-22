# Balanced session qualification

This independent v2 profile adds approved Markdown/archive snapshots, balanced
source sampling, immutable checkpoint history, exact continuation and a typed
local collection. The [v1 homegrown profile](hero-qualification.md) and
[terminal/world profile](qualification.md) keep their existing source pins.

Use Python 3.14+ and build the reference package:

```sh
uv build --out-dir dist
python scripts/qualify_session.py dist
```

The [source register](hero-sources-v2.json) pins Hypnosis, Thoughtform and their
components. The qualifier installs wheel and source artifacts in separate fresh
environments outside all source checkouts, verifies PEP 610 revisions and package
compatibility, and runs a small authored fixture. It does not read the owner's
training material or launch the one-hour experiment.

The fixture snapshots twelve authored Markdown lessons, prepares them with the
approved internal generator, and checks both source families receive training
windows with no training unknown-character exclusions. It trains a tiny v2 model,
continues it with Adam state preserved into a new destination, checks unchanged
parent bytes, indexes immutable intermediate/final artifacts idempotently, and
reads the filtered six-entry collection from a fresh process. Hypnosis's own
installed training suite additionally compares continued weights and optimizer
moments against uninterrupted training and qualifies limits/identity refusals.

Linux, macOS and Windows run this profile. `session-qualification.json` contains
artifact hashes, Python/platform and installed component revisions; CI uploads
one receipt per platform under the owner's existing authorization. The receipt
contains no source text, model weights, private paths or local training inventory.
An installed fixture establishes composition/packaging, not the quality of a
trained assistant or the completion of the separate real experiment.

The [implementation plan](IMPLEMENTATION_PLAN.md#session-v2-approved-python-materials-and-longer-checkpointed-experiments)
records the selected corpus, model, mixture, time contract and acceptance.
[HERO-SESSION-02](https://github.com/wispsy/hypnosis/issues/34) owns actual
measurements and retained local checkpoints. Native training state and quantized
inference remain distinct artifacts; no model-weight publication or promotion
follows from these checks.
