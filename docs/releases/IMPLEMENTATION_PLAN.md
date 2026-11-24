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

## Current delivery and remaining gates

All six selected previews, Paracosm and Wispsy are published as `0.1.0a1`. Current dependency updates
include Thoughtformula, Hidden Moves and its Projects/Workspace packages,
Headless Spreadsheets, Spatial UI, Builtouts, Astree, APIConn and Clownfish.
The final review also qualified Evok version reporting and Expose Protocol
legacy app identity compatibility; the Homebrew tap adopts verified artifacts.
Installed artifacts and platform CI qualify their selected profiles. The global
inventory records actual PyPI files independently of development branches.

REL-11I completed the reference package: published Paracosm 0.1.0a1 replaced the
final Git requirement, and Wispsy 0.1.0a1 passed all 17 platform jobs and six
exact-artifact release profiles before publication. Actual index files and a
fresh combined optional-profile installation are verified. Historical source
manifests remain unchanged; current profiles use index release manifests.

All 48 remote defaults use main; all 46 public main branches have baseline
protection, with verified CI requirements on the qualified release repositories.
Two private repositories require a supported GitHub plan for protection; no
visibility or paid-plan change is included. Backpack Store's renamed publisher
identity must be verified before its next upload.

Pocket Python's compiled runtime needs its dedicated installed release
qualification (wispsy/pocket_python#993). The release audit does not substitute
source CI for that gate. Gitwriter remains unpublished and unqualified.
Pretty Notebook's current web application work does not change the packaged
0.12.0 library or its pnbp compatibility distribution.

No model weights, datasets, deployments or local checkpoints are included.
