# Cohesion Block B release selection

Selected package: **carets 0.2.0**, authorized by the owner for this application
completion session. The existing public PyPI package has a 0.1.0 release; source
repository availability alone is not evidence of a package namespace. Its public
JSON metadata and published artifacts were checked before selecting this route.

| Surface | Selected result |
| --- | --- |
| Package / import namespace | carets / carets |
| Version / tag | 0.2.0 / v0.2.0 |
| Source commit | 0bec123a70dde1b762dd89622dc1954c8bacb794 |
| Core support | Python 3.10+, no runtime dependencies |
| License expression | MIT AND Unicode-3.0, with both notices in wheel/source |
| Artifacts | One pure-Python wheel and one source archive |
| Registry route | Existing PyPI Trusted Publisher, release.yaml workflow, pypi environment |
| GitHub release | Matching tag with the exact published wheel/source pair attached |
| Consumer selection | Hypnosis a7b41f3f89ac92df1e38073f5f69a9357671f227 |

Carets' optional snapshot presentation uses Headless Spreadsheets development
source 811f1e1b297cacb887164bcb78ba6be39e37c90d on Python 3.14+. Published Headless
Spreadsheets 0.1.0 predates that API, so a separately documented installation is
required. A direct Git dependency is not inserted into Carets' PyPI metadata.
[CARET-TABLE-02](https://github.com/wispsy/carets/issues/36) tracks the later
released optional dependency. It does not authorize publishing another package.

Publication follows passing exact-head source/wheel/platform and independent
application-family qualification. The release workflow checks tag/version, main
ancestry, licenses, metadata, source parity and wheel RECORD hashes, then tests
the distribution pair before the separate trusted upload job. The final record
in [CARET-REL-02](https://github.com/wispsy/carets/issues/28) must include the
workflow and registry results, uploaded SHA-256 values, matching downloaded bytes
and a fresh public installation. A prepared tag or public GitHub source alone
does not complete publication.

Hypnosis, Thoughtform, Thoughtformula, Engl, Paracosm, Wispsy, the other component
libraries and any hub/provider integrations have no new package release selected
here. No model weights, private datasets, services, sites or deployments are part
of this release. Carets #7 continues as the component growth backlog; the deferred
Ollama and next data/model/runtime selections remain separate issues.
