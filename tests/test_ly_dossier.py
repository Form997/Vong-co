import copy
import json
from pathlib import Path
import sys
import unittest
from unittest.mock import patch

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / 'scripts'))
import ly_pages


class LyDossierTest(unittest.TestCase):
    def test_source_specific_score_and_no_acceptance(self):
        data = ly_pages.load_dossier()
        self.assertFalse(data['performance_accepted'])
        self.assertEqual(len(data['sources']), 4)
        score = next(s for s in data['sources'] if s['id'] == 'S2')
        self.assertTrue(score['url'].endswith('#page=96'))
        self.assertIn('trang in 87', score['scope'])
        html = ly_pages.render_dossier(data)
        self.assertIn('Chưa nghiệm thu diễn xướng', html)
        self.assertNotIn('<audio', html)
        self.assertNotIn('<iframe', html)

    def test_reject_orphan_claim_and_unsafe_url(self):
        baseline = ly_pages.load_dossier()
        for mutation in ('orphan', 'url', 'acceptance', 'duplicate'):
            data = copy.deepcopy(baseline)
            if mutation == 'orphan':
                data['claims'][0]['sources'] = ['missing']
            elif mutation == 'url':
                data['sources'][0]['url'] = 'javascript:alert(1)'
            elif mutation == 'acceptance':
                data['performance_accepted'] = True
            else:
                data['sources'].append(data['sources'][0])
            with self.subTest(mutation=mutation), patch.object(Path, 'read_text', return_value=json.dumps(data)):
                with self.assertRaises(ValueError):
                    ly_pages.load_dossier()

    def test_second_dossier_keeps_sources_and_counts_separate(self):
        data = ly_pages.load_dossier('02-ly-con-sao-go-cong')
        self.assertEqual(data['id'], 'LY-002')
        self.assertEqual(len(data['sources']), 6)
        html = ly_pages.render_dossier(data)
        self.assertIn('<h1>Lý con sáo Gò Công</h1>', html)
        self.assertIn('12 câu', html)
        self.assertIn('17 câu, 2 nhịp', html)
        self.assertIn('#page=116', html)
        self.assertNotIn('#page=96', html)
        self.assertIn('/ly/02-ly-con-sao-go-cong/', html)
        self.assertIn('data/ly/02-ly-con-sao-go-cong.json', html)
        self.assertIn('../01-ly-cay-bong/', html)
        self.assertFalse(data['performance_accepted'])

    def test_unknown_slug_cannot_read_arbitrary_path(self):
        for slug in ['../../README', '03-unreviewed', '/tmp/secret']:
            with self.subTest(slug=slug), patch.object(Path, 'read_text') as read:
                with self.assertRaises(ValueError):
                    ly_pages.load_dossier(slug)
                read.assert_not_called()

    def test_comparison_requires_own_source(self):
        data = ly_pages.load_dossier('02-ly-con-sao-go-cong')
        data['comparison'][0]['sources'] = ['S99']
        with patch.object(Path, 'read_text', return_value=json.dumps(data)):
            with self.assertRaises(ValueError):
                ly_pages.load_dossier('02-ly-con-sao-go-cong')

    def test_escape_source_text(self):
        data = ly_pages.load_dossier()
        data['sources'][0]['title'] = '<script>alert(1)</script>'
        html = ly_pages.render_dossier(data)
        self.assertNotIn('<script>alert', html)
        self.assertIn('&lt;script&gt;', html)


if __name__ == '__main__':
    unittest.main()
