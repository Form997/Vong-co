import sys
import tempfile
import unittest
from pathlib import Path
from html.parser import HTMLParser
from urllib.parse import urlsplit
sys.path.insert(0, str(Path(__file__).resolve().parents[1] / 'scripts'))
from v3_build_site import build
from site_navigation import navigation_for


class Links(HTMLParser):
    def __init__(self):
        super().__init__()
        self.links = []
    def handle_starttag(self, tag, attrs):
        attrs = dict(attrs)
        if tag == 'a' and 'data-task' in attrs:
            self.links.append(attrs)


class NavigationTests(unittest.TestCase):
    def test_links_resolve_from_every_published_directory(self):
        with tempfile.TemporaryDirectory() as temp:
            root = Path(temp) / 'site'
            result = build(root)
            for name in result['published_files']:
                if not name.endswith('.html') or name == 'index.html':
                    continue
                with self.subTest(page=name):
                    parser = Links()
                    parser.feed((root / name).read_text())
                    self.assertEqual(len(parser.links), 4)
                    self.assertEqual(sum('aria-current' in a for a in parser.links), 1)
                    for link in parser.links:
                        target = urlsplit(link['href'])
                        path = root / name if not target.path else (root / name).parent / target.path / 'index.html'
                        self.assertTrue(path.is_file(), str(path))
                        self.assertIn('id="'+target.fragment+'"', path.read_text())
    def test_home_anchors_preserve_query_and_nested_pages_have_context(self):
        self.assertIn('href="#tra-cuu"', navigation_for('web/v3/index.html'))
        self.assertIn('data-task="ly" aria-current="page"', navigation_for('ly/02-ly-con-sao-go-cong/index.html'))
        self.assertIn('data-task="search" aria-current="page"', navigation_for('bai/01-luu-thuy-truong/index.html'))
