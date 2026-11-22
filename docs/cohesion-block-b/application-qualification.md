# Application profile qualification

`application-sources-v1.json` selects the integrated Hypnosis/Carets application
profile independently of historical terminal/world, Hero v1 and session v2 pins.
The Python 3.14 source/wheel qualifier installs exact dependency revisions,
checks their direct-URL commit identities and versions, runs the application
family tests outside the checkout, and checks dependency consistency. Sanitized
receipts include artifact hashes and interpreter/platform versions.

The family tests exercise actual saved-artifact verification/repair and heldout
configuration selection, independent Hypnosis and StatusDesk shell consumers,
actual process JSONL alongside the unchanged single-document command, and an
explicit native zero-step artifact syntax probe whose checkpoint bytes do not
change. POSIX additionally opens the actual application CLI on a pseudo-terminal,
sends a buffered key and checks terminal restoration. Windows tests are synthetic
and process-level; there is no native Windows console claim. Unicode width remains
the documented Carets policy rather than a universal font-shaping guarantee.

Run `uv build --out-dir dist`, `python scripts/check_distribution.py dist`, then
`python scripts/qualify_application.py dist`. The CI application matrix runs on
Linux/macOS/Windows and retains application-qualification.json. Hypnosis' own
matrix also retains per-profile source/wheel receipts. These artifacts contain
no prompts, private paths, source bodies, generated vocabulary, raw exceptions
or weights. No external training data or model is downloaded by these fixtures.

Carets 0.2.0 publication is authorized separately and follows this profile's
passing exact-source checks. The optional table snapshot API is pinned from
Headless Spreadsheets development source because its published 0.1.0 predates
that API. Historical profiles continue to exercise their original sources.

Selected merged sources: Hypnosis `a7b41f3f89ac92df1e38073f5f69a9357671f227` and Carets `0bec123a70dde1b762dd89622dc1954c8bacb794`. The local full suites passed 74 Hypnosis tests and 58 Carets tests; installed CI separately qualifies each optional profile. Final acceptance includes the Windows LF source-identity correction, direct-signal worker outcome settlement, and shared focus/layout/read-only navigation regressions.
