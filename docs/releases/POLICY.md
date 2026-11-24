# Release policy

Every distribution has its own version and release schedule. A green main branch is a development checkpoint. PyPI is the authority for downloadable package versions; GitHub release tags identify their selected source.

## Readiness

1. Select a bounded, documented capability profile and supported Python versions. Finish required dependency publications first.
2. Use index dependencies, including optional extras. Package metadata must not contain Git/direct URL requirements. Qualify optional profiles against the versions actually selected for publication.
3. Verify the selected source with relevant installed wheel and sdist tests and platform CI. Preserve historical qualification fixtures; add new evidence for current release profiles.
4. Build once, check tag/version/name agreement, MIT license metadata and included license text, artifact contents and hashes. Do not include private data, model weights, caches or local credentials.
5. Publish the exact qualified files through the repository's `release.yaml`, environment `pypi`, using Trusted Publishing. The release event is the single publication trigger. Do not move published tags, replace files or silently skip a mismatched existing artifact.
6. Confirm the files and SHA256 hashes through PyPI, install the actual published artifact, update consumers and record any remaining adoption separately.

The first six selected packages use `0.1.0a1` preview versions: compose-application, engl, thoughtform, hypnosis, gitdx and gittycat. Existing final releases retain their versions; changed functionality receives a new version. Documentation-only changes do not by themselves require another artifact upload.

## Release presentation

Use `<distribution> v<version>` for the GitHub release title. Describe the package and the actual changes, then include exact-version installation, supported Python, qualification evidence, selected source commit, PyPI version link and a `tag...main` comparison. Mark previews as prereleases. Preserve existing historical notes when normalizing their presentation.

A source label such as `0.1.0` on main never implies that the same version on PyPI contains subsequent commits. Link consumers to [STATUS.md](STATUS.md) and the [global Project](https://github.com/orgs/wispsy/projects/31) for that distinction.

## Repository housekeeping

Use `main` as the default branch. Public main branches require pull requests, resolved conversations, and prohibit deletion and non-fast-forward updates. Add verified stable CI contexts as release repositories are qualified. Preserve stronger existing rules. Private repository protection remains dependent on the account plan; do not change visibility or buy a plan to work around that limitation.

The repository name is `wispsy/backpack_store`, distribution `backpack-store`, and import `backpack_store`. Existing GitHub URLs redirect, and historical tags and package files remain immutable. Before its next upload, verify that the PyPI Trusted Publisher uses the renamed repository identity.

Dependency adoption changes active metadata, locks and executable examples. Historical experiment manifests, artifact receipts and source-pinned qualification reports remain records of their original runs.

## Package boundaries

Gittycat should be a PyPI distribution for its installable service, CLI and backend contract. Its publication does not deploy a service. Compose Application should publish its reusable composition interfaces and explicitly selected extras. The Wispsy repository currently provides source reference workflows and unpublished-family integrations; it remains source development until its own artifact and all selected extra dependencies can be installed from the index. An umbrella release is not required for independent libraries to publish.
