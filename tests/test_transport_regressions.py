"""Offline regressions for bounded, allowlisted API reads."""
import io
from pathlib import Path
import sys
import unittest
from urllib.error import HTTPError
from urllib.request import Request

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / 'scripts'))
from v3_6_discover import NoRedirect, load_api


class TransportTests(unittest.TestCase):
    def test_redirect_refused_before_following(self):
        request = Request('https://api.openalex.org/works',
                          headers={'Authorization': 'Bearer TEST_ONLY'})
        for status in (301, 302, 303, 307, 308):
            with self.subTest(status=status), self.assertRaises(HTTPError):
                NoRedirect().redirect_request(request, None, status, '', {},
                                               'https://example.invalid/steal')

    def test_credentials_cannot_be_sent_to_crossref(self):
        with self.assertRaises(ValueError):
            load_api('https://api.crossref.org/works', auth='TEST_ONLY')

    def test_duplicate_json_and_oversize_rejected(self):
        for body in (b'{"results": [], "results": [1]}', b' ' * 1_500_001):
            with self.subTest(size=len(body)), self.assertRaises(ValueError):
                load_api('https://api.crossref.org/works',
                         opener=lambda *a, **k: io.BytesIO(body))

    def test_os_error_retries_without_leaking_details(self):
        sleeps = []
        calls = []
        def broken(*args, **kwargs):
            calls.append(1)
            raise OSError('PRIVATE_DETAIL')
        with self.assertRaisesRegex(RuntimeError, '^Network error$'):
            load_api('https://api.crossref.org/works', opener=broken,
                     sleep=sleeps.append)
        self.assertEqual(len(calls), 3)
        self.assertEqual(sleeps, [1, 2])

    def test_valid_json_is_returned(self):
        self.assertEqual(load_api('https://api.crossref.org/works',
            opener=lambda *a, **k: io.BytesIO(b'{"message": {"items": []}}')),
            {'message': {'items': []}})
