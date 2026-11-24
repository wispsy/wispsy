# Release audit implementation plan

The [Wispsy Releases Project](https://github.com/orgs/wispsy/projects/31) is the canonical queue. Package implementation Projects remain independent. Publication and downstream adoption are separate completion states.

| Task | Scope | Acceptance and dependency |
| --- | --- | --- |
| REL-01 | Public release inventory | Date, PyPI files/hashes, main SHA/version, source comparison, reproducible read-only refresh, private repositories excluded. |
| REL-02 | Hypnosis Parse MW migration | `parse-mw==0.1.0`, citation spans/reuse/groups preserved, malformed/bounded inputs covered, installed data/training qualification. |
| REL-03 | Main branch policy | Default `main`, protected public branches, stronger rules preserved, account-plan exceptions recorded privately. |
| REL-04 | Backpack Store identity | Repository rename preserves history, active links and metadata use canonical identity, distribution/import compatibility retained. |
| REL-05 | Gitdx preview | Existing native client/storage scopes qualified from wheel/sdist; publish 0.1.0a1, verify index files and receipt. |
| REL-06 | Gittycat preview | After published Gitdx preview; qualify paired backend, management/authentication and CLI contracts. |
| REL-07 | Engl preview | Base and CLI installed on supported platforms with index dependencies; publish 0.1.0a1 and verify actual files. |
| REL-08 | Thoughtform preview | Publish required Thoughtformula functionality first; qualify tiny deterministic model definitions without distributing weights. |
| REL-09 | Hypnosis preview | After REL-02, Engl/Thoughtform and required tool/context dependencies exist on PyPI; qualify selected profiles. |
| REL-10 | Compose Application preview | Publish required Spatial UI/Headless Spreadsheets functionality first; qualify reusable composition extras. |
| REL-11 | Existing updates and consumers | Classify changes after each published source tag, publish ready functional updates under new versions, update compatible current consumers. Failed/missing qualification stays explicit. |
| REL-12 | Uniform release descriptions | Distribution/version titles, exact installation and source/PyPI/development links; preserve original release notes. |

## Execution

Work in focused PRs, start platform CI as each is ready, and continue independent preparation while checks run. Merge passing work in dependency order. Create a release only after its required dependencies and artifact checks pass. Retain SHA256 receipts from the publishing workflow and compare them with PyPI before closing publication tasks. Refresh the inventory and update the Project after each publication batch.

## Initial findings and limits

All remote defaults have been normalized to main and all 46 public main branches have baseline protections. Two private repositories require a paid GitHub plan for the requested protection; their identities are excluded from this public record. Backpack has been renamed to backpack_store with redirects and history preserved.

Hypnosis's Parse MW migration passed 27 installed profile/platform checks. Engl and Gitdx preview preparation adds exact-artifact publication gates. Other previews wait on current index dependencies. In particular, Hidden Moves Workspace is an unpublished distribution and needs its own publisher/readiness decision before a complete Hypnosis context/application preview can be qualified.

The initial source comparison also identifies functional updates in Thoughtformula, Hidden Moves, Headless Spreadsheets, Spatial UI, Astree, Builtouts and Pocket Python. A comparison is a review candidate, not a publication approval gate by itself. Builtouts has a failing audited main check to diagnose. Pocket Python has extensive source qualification; reuse the successful matching-head evidence and its existing release procedure rather than repeating an unrelated interpreter roadmap.

No model weights, datasets, deployments or local checkpoints are included in this package release work.
