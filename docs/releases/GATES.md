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

Additional dependent and patch releases in this batch are Thoughtformula 0.3.1,
Headless Spreadsheets 0.1.1, Spatial UI 0.1.1, Hidden Moves 0.1.1,
Hidden Moves GitHub Projects 0.1.1, Hidden Moves Workspace 0.1.0a2,
Builtouts 0.2.0, Astree 0.1.1, APIConn 0.1.1 and Clownfish 0.6.5, Evok 0.1.2 and Expose Protocol 0.1.1.
Compatible dependency ranges remain ranges; consumers that excluded a current
version or used unreleased Git sources were updated and qualified.

Two retained source releases did not upload their intended Python package:
Hidden Moves Workspace 0.1.0a1 and Clownfish 0.6.4. Their release notes explicitly
link to the successful 0.1.0a2 and 0.6.5 successors. Existing tags and native
archives are retained; actual publication is established by PyPI.

Evok 0.1.1 introduced the version flags but retained an old `info` banner.
Version 0.1.2 corrects that report; both existing package versions remain
immutable. The Homebrew tap selects the corrected Evok package and current
Clownfish package/native archive with verified download digests. The standalone
Clownfish archive is Apple Silicon (arm64); the cask states that requirement.

## Reviewed differences that do not require this batch to upload again

The inventory conservatively flags any metadata or tooling change for review.
The following comparisons have been assessed separately from runtime releases:

| Packages | Main changes beyond the current artifacts |
| --- | --- |
| Backpack Store, Desktop Interface, Expose Interface, Func Seq, JavaScript Fetch API, JavaScript JSON, Shimify | License/maintainer/repository metadata, documentation or release guidance; runtime code unchanged. Existing GitHub URLs redirect. Carry metadata into the next qualified package version. |
| Hidden Moves core | Workspace package qualification/publishing changes; the core runtime files are unchanged. |
| Hidden Moves MCP/OpenAI | Maintainer/repository metadata and exclusion of local Finder files; current dependency ranges admit the released core. |
| Immunity | Homebrew publishing helper, formula and installation documentation; packaged runtime modules unchanged. |
| Python JavaScript | Generated provenance/source links use Wispsy URLs; compiler behavior is unchanged. |

## Remaining gates

- [Pocket Python installed release qualification](https://github.com/wispsy/pocket-python/issues/993): source CI alone does not qualify a new compiled runtime publication. Preserve the active implementation queue and complete its dedicated artifact baseline before selecting the next version.
- [Gitwriter readiness](https://github.com/wispsy/gitwriter/issues/3): no package has been published or qualified. Its main version label is not a downloadable release.
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
