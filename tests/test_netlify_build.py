"""Verify that Netlify publishes the built V3.6 site, not the repo root."""
from pathlib import Path
import tomllib
import unittest

ROOT = Path(__file__).resolve().parents[1]


class NetlifyBuildConfigTests(unittest.TestCase):
    def test_site_is_built_into_publish_directory(self):
        config_path = ROOT / "netlify.toml"
        self.assertTrue(config_path.is_file())
        with config_path.open("rb") as f:
            cfg = tomllib.load(f)
        build = cfg["build"]
        self.assertEqual(build["publish"], "_site")
        self.assertEqual(build["command"],
                         "python3 scripts/v3_build_site.py --out _site")
        self.assertEqual(build["environment"]["PYTHON_VERSION"], "3.11")

    def test_build_script_creates_root_index_and_uses_allowlist(self):
        build_source = (ROOT / "scripts" / "v3_build_site.py").read_text(encoding="utf-8")
        self.assertIn('(target / "index.html").write_text(LANDING', build_source)
        self.assertIn("if files != expected:", build_source)
        self.assertIn('meta http-equiv="refresh" content="0;url=web/v3/"', build_source)

    def test_no_spa_fallback_for_standalone_pages(self):
        with (ROOT / "netlify.toml").open("rb") as f:
            config = tomllib.load(f)
        # The application is not a SPA; its 20 music pages and 4 groups
        # have physical index.html files and must retain real 404s for typos.
        self.assertNotIn("redirects", config)


if __name__ == "__main__":
    unittest.main()
