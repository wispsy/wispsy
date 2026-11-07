"""Exercise isolated installed wheel/source profiles outside the checkout."""

import argparse
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
            extras = "sequence,table" if profile == "composition" else profile
            run("uv", "pip", "install", "--python", str(python), f"{artifact}[{extras}]", cwd=outside)
            run(str(python), "-I", "-m", "unittest", "discover", "-s",
                str(ROOT / "integration_tests"), "-v", cwd=outside)
        if profile in ("sequence", "composition"):
            run(str(python), "-I", "-m", "unittest", "discover", "-s",
                str(ROOT / "lifecycle_tests"), "-v", cwd=outside)
        if profile == "composition":
            run(str(python), "-I", "-m", "unittest", "discover", "-s",
                str(ROOT / "table_tests"), "-v", cwd=outside)
        run("uv", "pip", "check", "--python", str(python), cwd=outside)
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
