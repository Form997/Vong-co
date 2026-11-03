"""Bài kiểm thử ngoại tuyến cho công cụ đo dung lượng trên GitHub."""

import contextlib
import importlib.util
import io
import json
import pathlib
import sys
import unittest
from unittest.mock import patch

SOURCE = pathlib.Path(__file__).resolve().parents[1] / "scripts" / "thong-ke-dung-luong.py"
spec = importlib.util.spec_from_file_location("size_reporter", SOURCE)
reporter = importlib.util.module_from_spec(spec)
spec.loader.exec_module(reporter)


class FakeResponse(io.BytesIO):
    def __init__(self, payload):
        super().__init__(json.dumps(payload).encode("utf-8"))


class SizeReporterTests(unittest.TestCase):
    def test_conversion_boundaries(self):
        cases = {
            0: "0 byte (0 bit)",
            1: "1 byte (8 bit)",
            1023: "1023 byte (8184 bit)",
            1024: "1.00 KiB",
            1048576: "1.00 MiB",
            1073741824: "1.00 GiB",
        }
        for value, expected in cases.items():
            with self.subTest(value=value):
                self.assertEqual(reporter.human_size(value), expected)

    def test_only_blob_sizes_count(self):
        payload = {
            "sha": "fixed-tree", "truncated": False,
            "tree": [
                {"type": "blob", "path": "README.md", "size": 100},
                {"type": "tree", "path": "docs"},
                {"type": "blob", "path": "docs/a.md", "size": 924},
            ],
        }
        with patch.object(reporter, "urlopen", return_value=FakeResponse(payload)) as mocked:
            result = reporter.get_snapshot("Form997/Vong-co", "v1-frozen")
        self.assertEqual(result["bytes"], 1024)
        self.assertEqual(result["files"], 2)
        self.assertEqual(result["KiB_binary"], 1)
        self.assertEqual(result["tree_sha"], "fixed-tree")
        self.assertIn("/git/trees/v1-frozen?recursive=1", mocked.call_args.args[0].full_url)

    def test_ref_is_encoded(self):
        payload = {"sha": "abc", "truncated": False, "tree": []}
        with patch.object(reporter, "urlopen", return_value=FakeResponse(payload)) as mocked:
            reporter.get_snapshot("Form997/Vong-co", "release/v3.0")
        self.assertIn("release%2Fv3.0", mocked.call_args.args[0].full_url)

    def test_truncation_rejected(self):
        payload = {"sha": "abc", "truncated": True, "tree": [{"type": "blob", "size": 100}]}
        with patch.object(reporter, "urlopen", return_value=FakeResponse(payload)):
            with self.assertRaisesRegex(RuntimeError, "cắt ngắn"):
                reporter.get_snapshot("Form997/Vong-co", "v2-development")

    def test_missing_size_rejected(self):
        payload = {"sha": "abc", "truncated": False, "tree": [{"type": "blob"}]}
        with patch.object(reporter, "urlopen", return_value=FakeResponse(payload)):
            with self.assertRaisesRegex(RuntimeError, "Thiếu kích thước"):
                reporter.get_snapshot("Form997/Vong-co", "v1-frozen")

    def test_json_cli(self):
        payload = {"sha": "abc", "truncated": False, "tree": [{"type": "blob", "size": 2048}]}
        output = io.StringIO()
        with patch.object(reporter, "urlopen", return_value=FakeResponse(payload)):
            with patch.object(sys, "argv", ["size-reporter", "--refs", "v1-frozen", "--json"]):
                with contextlib.redirect_stdout(output):
                    code = reporter.main()
        self.assertEqual(code, 0)
        self.assertEqual(json.loads(output.getvalue())[0]["bytes"], 2048)

    def test_markdown_cli(self):
        payload = {"sha": "abc", "truncated": False, "tree": [{"type": "blob", "size": 3072}]}
        output = io.StringIO()
        with patch.object(reporter, "urlopen", return_value=FakeResponse(payload)):
            with patch.object(sys, "argv", ["size-reporter", "--refs", "v1-frozen"]):
                with contextlib.redirect_stdout(output):
                    code = reporter.main()
        self.assertEqual(code, 0)
        self.assertIn("3.00 KiB", output.getvalue())
        self.assertIn("3,072", output.getvalue())

    def test_cli_error_on_truncation(self):
        payload = {"sha": "abc", "truncated": True, "tree": []}
        output = io.StringIO()
        with patch.object(reporter, "urlopen", return_value=FakeResponse(payload)):
            with patch.object(sys, "argv", ["size-reporter", "--refs", "v1-frozen"]):
                with contextlib.redirect_stderr(output):
                    code = reporter.main()
        self.assertEqual(code, 1)
        self.assertIn("cắt ngắn", output.getvalue())

    def test_token_is_sent_via_header_only(self):
        payload = {"sha": "abc", "truncated": False, "tree": []}
        with patch.dict(reporter.os.environ, {"GITHUB_TOKEN": "test-token"}):
            with patch.object(reporter, "urlopen", return_value=FakeResponse(payload)) as mocked:
                reporter.get_snapshot("Form997/Vong-co", "v1-frozen")
        request = mocked.call_args.args[0]
        self.assertEqual(request.get_header("Authorization"), "Bearer test-token")
        self.assertNotIn("test-token", request.full_url)


if __name__ == "__main__":
    unittest.main()
