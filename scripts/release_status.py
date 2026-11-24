"""Read public GitHub/PyPI state; write a dated release inventory without mutations."""
from __future__ import annotations

import argparse
import base64
from concurrent.futures import ThreadPoolExecutor
from datetime import datetime, timezone
import json
from pathlib import Path
import re
import subprocess
import tomllib
from urllib.error import HTTPError
from urllib.request import urlopen

SUBPACKAGES = {
    "pretty-notebook": ["packages/pnbp-transition"],
    "hidden_moves": [f"packages/hidden-moves-{name}" for name in ("mcp", "openai", "github-projects", "workspace")],
}
PROJECT = "https://github.com/orgs/wispsy/projects/31"


def gh(*arguments: str):
    result = subprocess.run(["gh", *arguments], capture_output=True, text=True)
    if result.returncode:
        if "HTTP 404" in result.stderr:
            return None
        raise RuntimeError(result.stderr.strip())
    return json.loads(result.stdout)


def contents(repository: str, path: str, ref: str):
    data = gh("api", f"repos/{repository}/contents/{path}?ref={ref}")
    return base64.b64decode(data["content"]).decode() if data else None


def change_kind(paths: list[str], truncated: bool = False) -> str:
    """Conservative review aid: executable changes always require release review."""
    if truncated:
        return "review required (comparison truncated)"
    if not paths:
        return "current"
    administrative = re.compile(r"^(docs/|\.github/|README|LICENSE|CHANGELOG|IMPLEMENTATION_PLAN|\.gitignore|\.python-version)")
    if all(administrative.match(path) for path in paths):
        return "documentation/administration ahead"
    return "source/metadata ahead; qualification required"


def published(name: str):
    try:
        with urlopen(f"https://pypi.org/pypi/{name}/json", timeout=30) as response:
            data = json.load(response)
    except HTTPError as error:
        if error.code == 404:
            return None
        raise
    info = data["info"]
    return {
        "version": info["version"], "requires_python": info["requires_python"],
        "url": f"https://pypi.org/project/{name}/{info['version']}/",
        "files": [{"filename": item["filename"], "sha256": item["digests"]["sha256"],
                   "uploaded": item["upload_time_iso_8601"], "yanked": item["yanked"]} for item in data["urls"]],
    }


def inspect_repository(repository):
    # Defense in depth: callers cannot accidentally export private repository data.
    if repository["isPrivate"]:
        return []
    repo = repository["nameWithOwner"]
    branch = repository["defaultBranchRef"]["name"] if repository["defaultBranchRef"] else None
    if not branch:
        return []
    commit = gh("api", f"repos/{repo}/commits/{branch}")["sha"]
    records = []
    for directory in ["", *SUBPACKAGES.get(repo.split("/")[1], [])]:
        path = f"{directory}/pyproject.toml" if directory else "pyproject.toml"
        text = contents(repo, path, commit)
        project = tomllib.loads(text).get("project", {}) if text else {}
        if not project.get("name"):
            continue
        current = published(project["name"])
        record = {"repository": repo, "directory": directory, "distribution": project["name"],
                  "main_version": project.get("version"), "main_sha": commit,
                  "default_branch": branch, "requires_python": project.get("requires-python"),
                  "source_url": f"https://github.com/{repo}/tree/{commit}" + (f"/{directory}" if directory else ""),
                  "published": current, "status": "unpublished", "comparison": None}
        if current:
            tags = [f"v{current['version']}-{project['name'].removeprefix('hidden-moves-')}"] if directory and repo.endswith("/hidden_moves") else [f"v{current['version']}"]
            record["status"] = "published; source tag unverified"
            for tag in tags:
                comparison = gh("api", f"repos/{repo}/compare/{tag}...{commit}")
                if comparison is None:
                    continue
                paths = [item["filename"] for item in comparison["files"]]
                selected = [p for p in paths if p.startswith(directory + "/")] if directory else paths
                truncated = len(paths) >= 300
                record["comparison"] = {"tag": tag, "sha": comparison["base_commit"]["sha"],
                                        "ahead": comparison["ahead_by"], "paths": selected,
                                        "truncated": truncated,
                                        "url": f"https://github.com/{repo}/compare/{tag}...main"}
                record["status"] = change_kind(selected, truncated)
                if repo == "wispsy/pretty-notebook" and not directory and any(p.startswith("apps/web/") for p in paths) and not any(p.startswith("src/") or p == "pyproject.toml" for p in paths):
                    record["status"] = "application/docs ahead; library code unchanged"
                break
        records.append(record)
    return records


def render(data):
    lines = ["# Release status", "", f"Observed **{data['observed_at']}**. This is a snapshot, not a live service.", "",
             f"[Wispsy Releases]({PROJECT}) owns publication, dependency adoption and release housekeeping.", "",
             "PyPI versions identify downloadable artifacts. A version in `pyproject.toml` on `main` is a development label and does not prove publication.",
             "`current` means the recorded source comparison is empty; it does not certify every optional platform/profile. Source-tag comparisons aid review; PyPI SHA256 digests identify the actual published files.", "",
             "| Distribution | PyPI | Main label | Published source vs main |", "| --- | --- | --- | --- |"]
    for record in data["packages"]:
        current = record["published"]
        pypi = f"[{current['version']}]({current['url']})" if current else "Unpublished"
        source = f"[{record['main_version']}]({record['source_url']})"
        status = record["status"]
        if record["comparison"]:
            status = f"[{status}]({record['comparison']['url']})"
        lines.append(f"| `{record['distribution']}` | {pypi} | {source} | {status} |")
    lines += ["", "Reproduce with `python scripts/release_status.py --output docs/releases` (Python 3.11+, authenticated `gh`, public network access).",
              "The command reads public repository metadata and PyPI. HTTP/authentication errors fail the refresh; only an actual PyPI 404 means unpublished.",
              "Private repositories are excluded. Read [readiness and remaining gates](GATES.md), [the release policy](POLICY.md) and [implementation queue](IMPLEMENTATION_PLAN.md) for decisions behind this inventory.", ""]
    return "\n".join(lines)


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--owner", default="wispsy")
    parser.add_argument("--output", type=Path, default=Path("docs/releases"))
    args = parser.parse_args()
    repositories = gh("repo", "list", args.owner, "--limit", "1000", "--json", "nameWithOwner,isPrivate,defaultBranchRef")
    # Filter before dispatching any content reads or serialization.
    public = [repository for repository in repositories if not repository["isPrivate"]]
    with ThreadPoolExecutor(max_workers=4) as executor:
        packages = [item for group in executor.map(inspect_repository, public) for item in group]
    data = {"schema": 1, "observed_at": datetime.now(timezone.utc).isoformat(timespec="seconds"),
            "project": PROJECT, "public_repositories": len(public),
            "packages": sorted(packages, key=lambda item: item["distribution"].lower())}
    args.output.mkdir(parents=True, exist_ok=True)
    (args.output / "status.json").write_text(json.dumps(data, indent=2) + "\n")
    (args.output / "STATUS.md").write_text(render(data))
    print(f"Recorded {len(packages)} public distributions in {args.output}")


if __name__ == "__main__":
    main()
