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

    def test_escape_source_text(self):
        data = ly_pages.load_dossier()
        data['sources'][0]['title'] = '<script>alert(1)</script>'
        html = ly_pages.render_dossier(data)
        self.assertNotIn('<script>alert', html)
        self.assertIn('&lt;script&gt;', html)


if __name__ == '__main__':
    unittest.main()
