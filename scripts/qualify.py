"""Exercise isolated installed wheel/source profiles outside the checkout."""

import argparse
import hashlib
import json
from pathlib import Path
import subprocess
import sys
import tempfile

ROOT = Path(__file__).resolve().parents[1]


def run(*command: str, cwd: Path) -> None:
    subprocess.run(command, cwd=cwd, check=True)


def qualify(artifact: Path, profile: str) -> None:
    with tempfile.TemporaryDirectory(prefix="wispsy-qualification-") as temporary:
        outside = Path(temporary)
        environment = outside / "environment"
        run("uv", "venv", str(environment), "--python", sys.executable, cwd=outside)
        python = environment / ("Scripts/python.exe" if sys.platform == "win32" else "bin/python")
        run("uv", "pip", "install", "--python", str(python), str(artifact), cwd=outside)
        run(str(python), "-I", "-c",
            "import importlib.util, wispsy.reference; "
            "assert importlib.util.find_spec('hidden_moves') is None; "
            "assert importlib.util.find_spec('func_seq') is None", cwd=outside)
        run(str(python), "-I", "-m", "unittest", "discover", "-s", str(ROOT / "tests"), "-v", cwd=outside)
        if profile in ("workflow", "sequence", "composition"):
            extras = "sequence,table,scripting,terminal" if profile == "composition" else "workflow,scripting" if profile == "workflow" else profile
            run("uv", "pip", "install", "--python", str(python), f"{artifact}[{extras}]", cwd=outside)
            run(str(python), "-I", "-m", "unittest", "discover", "-s",
                str(ROOT / "integration_tests"), "-v", cwd=outside)
        if profile in ("sequence", "composition"):
            run(str(python), "-I", "-m", "unittest", "discover", "-s",
                str(ROOT / "lifecycle_tests"), "-v", cwd=outside)
        if profile == "composition":
            run(str(python), "-I", "-m", "unittest", "discover", "-s",
                str(ROOT / "table_tests"), "-v", cwd=outside)
        if profile in ("workflow", "composition"):
            run(str(python), "-I", "-m", "unittest", "discover", "-s",
                str(ROOT / "composition_tests"), "-v", cwd=outside)
        run("uv", "pip", "check", "--python", str(python), cwd=outside)
        receipt = '''import importlib.metadata as m, json, platform
items = []
for name in ("wispsy", "hidden-moves", "moveset", "scriptty", "func-seq", "carets", "headless-spreadsheets", "expose-interface", "click"):
    try: distribution = m.distribution(name)
    except m.PackageNotFoundError: continue
    direct = distribution.read_text("direct_url.json")
    items.append({"name": name, "version": distribution.version, "source": json.loads(direct) if direct else None})
print(json.dumps({"python": platform.python_version(), "system": platform.system(), "packages": items}, sort_keys=True))
'''
        run(str(python), "-I", "-c", receipt, cwd=outside)
    print(json.dumps({"schema": 1, "artifact": artifact.name, "sha256": hashlib.sha256(artifact.read_bytes()).hexdigest(), "profile": profile}, sort_keys=True))
    print(f"Qualified {artifact.name}: {profile}", flush=True)


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("directory", type=Path)
    parser.add_argument("--profile", choices=("base", "workflow", "sequence", "composition"), default="workflow")
    arguments = parser.parse_args()
    if arguments.profile in ("sequence", "composition") and sys.version_info < (3, 14):
        parser.error("The sequence profile requires Python 3.14 or newer")
    directory = arguments.directory.resolve()
    artifacts = sorted([*directory.glob("*.whl"), *directory.glob("*.tar.gz")])
    if len(artifacts) != 2:
        parser.error("Expected one wheel and one source archive")
    for artifact in artifacts:
        qualify(artifact, arguments.profile)


if __name__ == "__main__":
    main()
