# Release readiness and remaining gates

The [inventory](STATUS.md) records actual PyPI files and each public main branch.
A source difference marks work for review; it does not by itself justify another
upload. Documentation changes and independent application changes can remain
ahead of a current library artifact.

## Qualified publication batch

The initial previews are compose-application, engl, thoughtform, hypnosis, gitdx,
gittycat, paracosm and wispsy, each at `0.1.0a1`. Selected installed profiles and
platform matrices passed before publication. PyPI files are compared with exact
workflow SHA256 and byte-size receipts, and current consumers use index releases.
Hypnosis data/training uses `parse-mw==0.1.0`.

Existing package updates in this batch are Thoughtformula 0.3.1,
Headless Spreadsheets 0.1.1, Spatial UI 0.1.1, Hidden Moves 0.1.1,
Hidden Moves GitHub Projects 0.1.1, Hidden Moves Workspace 0.1.0a2,
Builtouts 0.2.0, Astree 0.1.1, APIConn 0.1.1 and Clownfish 0.6.5.
Compatible dependency ranges remain ranges; consumers that excluded a current
version or used unreleased Git sources were updated and qualified.

Two retained source releases did not upload their intended Python package:
Hidden Moves Workspace 0.1.0a1 and Clownfish 0.6.4. Their release notes explicitly
link to the successful 0.1.0a2 and 0.6.5 successors. Existing tags and native
archives are retained; actual publication is established by PyPI.

## Remaining gates

- [Pocket Python installed release qualification](https://github.com/wispsy/pocket_python/issues/993): source CI alone does not qualify a new compiled runtime publication. Preserve the active implementation queue and complete its dedicated artifact baseline before selecting the next version.
- Gitwriter remains unpublished and unqualified. Its main version label is not a downloadable release.
- [Backpack Store publisher identity](https://github.com/wispsy/backpack_store/issues/47): before its next new-version upload, verify the account-side Trusted Publisher uses owner `wispsy`, repository `backpack_store`, workflow `release.yaml`, environment `pypi`. Existing backpack-store 0.2.0 remains current; the rename/documentation changes need no replacement upload.
- [Private branch protection](https://github.com/wispsy/wispsy/issues/46): all 48 defaults are main, and all 46 public main branches are protected. Two private repositories require a supported GitHub plan for protection. No visibility or paid-plan change was made; their identities remain private.

Pretty Notebook's web application changes are outside the published library
source. The current library and pnbp compatibility package remain 0.12.0; this
audit does not deploy the web application or change its release policy.

No model weights, datasets, local checkpoints or service deployments are part of
this package publication batch. Historical experiment/source manifests remain
records of their original runs. Future functionality stays in each owning
Project; [Wispsy Releases](https://github.com/orgs/wispsy/projects/31) tracks
publication and adoption across them.
