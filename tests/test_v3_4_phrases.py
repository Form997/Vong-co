"""V3.4 keeps the two Cổ Bản ledgers distinct and does not certify a performance."""
from __future__ import annotations

import copy
from html.parser import HTMLParser
from pathlib import Path
import sys
import tempfile
import unittest

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / 'scripts'))
from v3_validate import CATALOG, strict_load
from v3_3_validate import INDEX as V33_INDEX
from v3_4_validate import INDEX, validate_v34
from v3_build_site import build


class IdCollector(HTMLParser):
    def __init__(self):
        super().__init__()
        self.ids = []
        self.fragments = []

    def handle_starttag(self, tag, attrs):
        attrs = dict(attrs)
        if 'id' in attrs:
            self.ids.append(attrs['id'])
        if tag == 'a' and attrs.get('href', '').startswith('#'):
            self.fragments.append(attrs['href'][1:])


class V34Tests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.data = strict_load(INDEX)
        cls.old = strict_load(V33_INDEX)
        cls.catalog = strict_load(CATALOG)
        cls.systems = {x['variant_id']: x for x in cls.data['items']}
        cls.cb = [x for x in cls.data['items'] if x['piece_id'] == 4]

    def test_separate_systems_and_preserve_v33(self):
        self.assertEqual(validate_v34(self.data, self.catalog), [])
        self.assertEqual(len(self.data['items']), 6)
        self.assertEqual(len({x['piece_id'] for x in self.data['items']}), 5)
        self.assertEqual(sum(len(x['phrases']) for x in self.data['items']), 252)
        self.assertEqual(sorted(len(x['phrases']) for x in self.cb), [34, 68])
        for item in self.old['items']:
            self.assertEqual(self.systems[item['variant_id']], item)
        self.assertEqual(self.data['performance_status'], 'pending')
        self.assertEqual(self.data['rights_status'], 'unverified')

    def test_wrong_page_swapped_system_or_false_rights_rejected(self):
        for mutate in (
            lambda d: d['items'][next(i for i,x in enumerate(d['items']) if x['piece_id']==4)]['phrases'][0].__setitem__('printed_music_page', 999),
            lambda d: d['items'][next(i for i,x in enumerate(d['items']) if x['piece_id']==4)].__setitem__('variant_id', 'WRONG'),
            lambda d: d.__setitem__('performance_status', 'approved'),
            lambda d: d.__setitem__('rights_status', 'verified'),
            lambda d: d['items'][0]['phrases'][0].__setitem__('number', 999),
        ):
            d = copy.deepcopy(self.data)
            mutate(d)
            self.assertTrue(validate_v34(d, self.catalog))

    def test_build_renders_both_separate_systems_and_unique_links(self):
        with tempfile.TemporaryDirectory() as temp:
            dst = Path(temp) / 'site'
            result = build(dst)
            self.assertEqual((result['indexed_lesson_pieces'], result['indexed_lesson_systems'],
                              result['indexed_lesson_phrases']), (5, 6, 252))
            slug = next(x['slug'] for x in self.catalog['items'] if x['id'] == 4)
            html = (dst / 'bai' / slug / 'index.html').read_text(encoding='utf-8')
            self.assertEqual(html.count('class="phrase-row"'), 102)
            for item in self.cb:
                self.assertIn(item['variant_id'], html)
                self.assertIn(f"{len(item['phrases'])}/{len(item['phrases'])}", html)
            self.assertIn('0/20', html)
            self.assertNotIn('#page=', html)
            self.assertNotIn('<audio', html)
            p = IdCollector()
            p.feed(html)
            self.assertEqual(len(p.ids), len(set(p.ids)), 'IDs must be unique across both systems')
            self.assertTrue(set(p.fragments).issubset(set(p.ids)))


if __name__ == '__main__':
    unittest.main()
