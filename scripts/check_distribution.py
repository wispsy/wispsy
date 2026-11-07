"""Inspect built distribution metadata and the public package boundary."""

from email.parser import BytesParser
from pathlib import Path
import sys
import tarfile
import zipfile


def check(directory: str) -> None:
    artifacts = sorted(Path(directory).iterdir())
    wheels = [path for path in artifacts if path.suffix == ".whl"]
    sources = [path for path in artifacts if path.name.endswith(".tar.gz")]
    assert len(wheels) == len(sources) == 1, "Expected one wheel and one source archive"
    with zipfile.ZipFile(wheels[0]) as archive:
        names = archive.namelist()
        assert "wispsy/__init__.py" in names
        assert "wispsy/py.typed" in names
        metadata, = [name for name in names if name.endswith(".dist-info/METADATA")]
        message = BytesParser().parsebytes(archive.read(metadata))
        assert message["Name"] == "wispsy"
        assert message["Requires-Python"] == ">=3.11"
        assert all("extra ==" in item for item in message.get_all("Requires-Dist", []))
        assert not any(".venv/" in name or "__pycache__/" in name for name in names)
    with tarfile.open(sources[0]) as archive:
        names = archive.getnames()
        assert any(name.endswith("/IMPLEMENTATION_PLAN.md") for name in names)
        assert any(name.endswith("/src/wispsy/__init__.py") for name in names)
    print("Wheel and source metadata verified")


if __name__ == "__main__":
    check(sys.argv[1])
