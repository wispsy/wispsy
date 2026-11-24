# Wispsy preview qualification

Wispsy 0.1.0a1 contains executable reference workflows. The base package has no
runtime dependencies and supports Python 3.11+. Optional profiles select exact
published packages; sequence, table, terminal, family and application integrations
require Python 3.14+. No model weights or datasets are distributed.

The release event builds one wheel and one sdist. `scripts/check_release.py`
checks the selected tag, identity, Python support, MIT license, index-only
requirements and payload boundary, and writes SHA256/byte-size receipts.
Qualification downloads those exact files and runs:

| Python | Profile | Command |
| --- | --- | --- |
| 3.11 | Workflow, scripting and base isolation | `python scripts/qualify.py dist --profile workflow` |
| 3.14 | Composition, sequence, tables and terminal | `python scripts/qualify.py dist --profile composition` |
| 3.14 | Models, world rules and generated terminal commands | `python scripts/qualify_family.py dist` |
| 3.14 | Homegrown tiny learning fixtures | `python scripts/qualify_hero.py dist` |
| 3.14 | Balanced session fixtures | `python scripts/qualify_session.py dist` |
| 3.14 | Hypnosis/Carets application | `python scripts/qualify_application.py dist` |

Each command installs both artifacts into separate temporary environments outside
the checkout and checks dependency consistency. The existing PR matrix covers
Linux, macOS and Windows. Native terminal interaction is qualified on POSIX;
Windows checks the headless contract.

The `release-*.json` manifests record current index versions. Original source
manifests preserve historical runs. Tiny deterministic training checks qualify
composition and numerical resume, not model quality or production training.

Publication uses `.github/workflows/release.yaml`, environment `pypi`, and
Trusted Publishing. It uploads the same qualified files, without rebuilding or
silently skipping existing files. After publication, compare actual PyPI hashes
with `release-artifacts.json`, install from the index and record the result in
[Wispsy Releases](https://github.com/orgs/wispsy/projects/31).
