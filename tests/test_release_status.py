"""Release inventory privacy and conservative source comparison contracts."""
import importlib.util
from pathlib import Path
import unittest

spec = importlib.util.spec_from_file_location("release_status", Path(__file__).resolve().parents[1] / "scripts/release_status.py")
release_status = importlib.util.module_from_spec(spec)
spec.loader.exec_module(release_status)


class ReleaseStatusTests(unittest.TestCase):
    def test_private_repository_is_never_read_or_exported(self):
        self.assertEqual(release_status.inspect_repository({"isPrivate": True}), [])

    def test_executable_and_incomplete_comparisons_require_review(self):
        self.assertEqual(release_status.change_kind([]), "current")
        self.assertEqual(release_status.change_kind(["docs/usage.md", "README.md"]), "documentation/administration ahead")
        self.assertIn("qualification required", release_status.change_kind(["src/library.py"]))
        self.assertIn("qualification required", release_status.change_kind(["pyproject.toml"]))
        self.assertIn("truncated", release_status.change_kind(["docs/usage.md"], True))

    def test_unpublished_is_not_rendered_as_the_main_version(self):
        data = {"observed_at": "2026-11-24T00:00:00Z", "packages": [{"distribution": "example", "published": None, "main_version": "9.0.0", "source_url": "https://example.test/main", "status": "unpublished", "comparison": None}]}
        self.assertIn("| `example` | Unpublished | [9.0.0]", release_status.render(data))
