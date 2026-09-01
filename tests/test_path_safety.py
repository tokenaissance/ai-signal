import shutil
import sys
import tempfile
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
SCRIPTS = ROOT / "scripts"
sys.path.insert(0, str(SCRIPTS))

try:
    import prepare_digest
    from prepare_digest import (
        fetch_text_any,
        load_local_text,
        safe_repo_relative_path,
    )
except ImportError as exc:  # pragma: no cover - depends on local deps
    raise unittest.SkipTest(f"prepare_digest import failed: {exc}") from exc


class SafeRepoRelativePathTests(unittest.TestCase):
    def test_accepts_plain_repo_relative_paths(self):
        for candidate in (
            "content/summaries/x/zh_standard/demo.md",
            "feeds/transcripts/abc.txt",
            "README.md",
        ):
            resolved = safe_repo_relative_path(candidate)
            self.assertIsNotNone(resolved, candidate)
            try:
                resolved.relative_to(ROOT.resolve())
            except ValueError:
                self.fail(f"{candidate} resolved outside ROOT_DIR")

    def test_rejects_absolute_paths(self):
        for candidate in ("/etc/hosts", "\\etc\\hosts", "/tmp/x.txt"):
            self.assertIsNone(safe_repo_relative_path(candidate), candidate)

    def test_rejects_parent_traversal(self):
        for candidate in (
            "../secrets.txt",
            "content/../../etc/passwd",
            "a/../..",
            "../../../../.ssh/id_rsa",
        ):
            self.assertIsNone(safe_repo_relative_path(candidate), candidate)

    def test_rejects_dot_segments_and_empty(self):
        for candidate in (".", "content/./x.md", "a/b/."):
            self.assertIsNone(safe_repo_relative_path(candidate), candidate)
        self.assertIsNone(safe_repo_relative_path(""))
        self.assertIsNone(safe_repo_relative_path("   "))

    def test_rejects_windows_style_paths(self):
        for candidate in ("C:/Windows/win.ini", "C:\\Windows\\win.ini", "c:/x"):
            self.assertIsNone(safe_repo_relative_path(candidate), candidate)

    def test_rejects_urls_and_non_strings(self):
        for candidate in (
            "https://evil.example/summary.md",
            "file:///etc/passwd",
            "javascript://x",
        ):
            self.assertIsNone(safe_repo_relative_path(candidate), candidate)
        self.assertIsNone(safe_repo_relative_path(None))
        self.assertIsNone(safe_repo_relative_path(123))


class LoadLocalTextTests(unittest.TestCase):
    def test_reads_existing_file_inside_checkout(self):
        text = load_local_text("README.md")
        self.assertIsNotNone(text)
        self.assertIn("AI Signal", text)

    def test_refuses_absolute_path(self):
        self.assertIsNone(load_local_text("/etc/hosts"))

    def test_refuses_parent_traversal_to_real_file(self):
        # Resolves to a real file outside the checkout; must still be refused.
        self.assertIsNone(load_local_text("../../.zshrc"))

    def test_refuses_traversal_to_temp_file(self):
        fd, name = tempfile.mkstemp(prefix="ai-signal-secret-")
        with open(fd, "w", encoding="utf-8") as handle:
            handle.write("secret")
        try:
            escape = Path(name)
            rel = escape.relative_to(ROOT.resolve())
        except ValueError:
            rel = None
        try:
            if rel is not None:
                self.assertIsNone(load_local_text(str(rel)))
            else:
                self.assertIsNone(load_local_text("../" * 8 + escape.name))
        finally:
            Path(name).unlink(missing_ok=True)


class FetchTextAnyTests(unittest.TestCase):
    def test_rejects_invalid_paths_without_network(self):
        # Invalid paths must return None immediately, before any fetch attempt.
        for candidate in ("/etc/hosts", "content/../../etc/passwd", "C:\\x"):
            self.assertIsNone(fetch_text_any(candidate), candidate)


class AttachSummaryTextTests(unittest.TestCase):
    def test_ignores_traversal_summary_path(self):
        items = prepare_digest.attach_summary_text(
            [{"id": "1", "summary_path": "../../../../etc/hosts"}]
        )
        self.assertNotIn("summary_text", items[0])

    def test_loads_safe_local_sidecar(self):
        tmp = ROOT / ".tmp-path-safety-test"
        tmp.mkdir(exist_ok=True)
        target = tmp / "sidecar.md"
        target.write_text("safe sidecar content", encoding="utf-8")
        original = prepare_digest.fetch_text_any
        prepare_digest.fetch_text_any = lambda path: None  # force local fallback
        try:
            items = prepare_digest.attach_summary_text(
                [{"id": "1", "summary_path": str(target.relative_to(ROOT))}]
            )
            self.assertEqual(items[0]["summary_text"], "safe sidecar content")
        finally:
            prepare_digest.fetch_text_any = original
            shutil.rmtree(tmp, ignore_errors=True)


if __name__ == "__main__":
    unittest.main()
