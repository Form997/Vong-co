"""Input and source boundary regressions; no external services required."""
import io
import unittest
from unittest.mock import patch
from urllib.error import HTTPError
from urllib.request import Request
from catalog import Catalog, MAX_BYTES, MAX_CHARS, NoRedirect, SourceAccessError, _download, _valid_path


class RegressionTests(unittest.TestCase):
    def test_numeric_search_is_exact(self):
        for query, expected in [('1', [1]), ('01', [1]), ('20', [20]), ('0', []), ('21', [])]:
            with self.subTest(query=query):
                self.assertEqual([w['number'] for w in Catalog().search_ban_to(query)['works']], expected)

    def test_non_string_inputs_fail_cleanly(self):
        for value in (None, [], {}, 1):
            self.assertFalse(_valid_path(value))
            with self.assertRaises(ValueError):
                Catalog().get_ban_to(1, value)

    def test_custom_source_cannot_bypass_size_or_type_limit(self):
        for value in (None, b'bytes', 'a' * (MAX_BYTES + 1), 'Đ' * MAX_BYTES):
            with self.subTest(kind=type(value).__name__), self.assertRaises(SourceAccessError):
                Catalog(lambda *_: value).get_ban_to(1)

    def test_invalid_utf8_is_not_silently_changed(self):
        with patch('catalog._SOURCE_OPENER.open', return_value=io.BytesIO(b'\xff')):
            with self.assertRaises(SourceAccessError):
                _download('v1-frozen', 'docs/test.md')

    def test_redirect_is_not_followed(self):
        with self.assertRaises(HTTPError):
            NoRedirect().redirect_request(Request('https://raw.githubusercontent.com/test'),
                None, 302, '', {}, 'https://example.invalid/test')

    def test_rules_truncation_is_explicit(self):
        result = Catalog(lambda *_: 'a' * (MAX_CHARS + 1)).get_quy_che_v2()
        self.assertTrue(result['truncated'])
        self.assertEqual(len(result['content']), MAX_CHARS)
