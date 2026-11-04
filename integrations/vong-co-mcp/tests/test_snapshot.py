"""Offline provenance, tamper detection and committed-source export regressions."""
import hashlib
import json
import os
from pathlib import Path
import subprocess
import tempfile
import unittest
from unittest.mock import patch
from catalog import BRANCHES, Catalog, MAX_BYTES, SourceAccessError, SourceNotFound
from snapshot import LocalSource, approved_sources, export_snapshot

PATH = 'ban-to/01-luu-thuy-truong/README.md'
BODY = '# Lưu Thủy Trường\nDị bản vắn và trường.\n'


def fixture(root):
    records = []
    for branch, path in sorted(approved_sources()):
        present = path == PATH or path.endswith('v2-bien-ban-nghiem-thu.md')
        text = BODY if path == PATH else 'CHỜ NGHIỆM THU'
        digest = hashlib.sha256(text.encode()).hexdigest() if present else None
        if present:
            dest = root / branch / path
            dest.parent.mkdir(parents=True, exist_ok=True)
            dest.write_text(text, encoding='utf-8')
        records.append({'branch': branch, 'path': path, 'sha256': digest})
    manifest = {'schema_version': 1, 'repository': 'Form997/Vong-co',
                'commits': {b: str(i)*40 for i,b in enumerate(BRANCHES.values(),1)}, 'files': records}
    (root / 'manifest.json').write_text(json.dumps(manifest), encoding='utf-8')
    return manifest


class SnapshotTests(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        self.addCleanup(self.tmp.cleanup)
        self.root = Path(self.tmp.name)
        self.manifest = fixture(self.root)

    def test_offline_read_is_commit_pinned_without_network(self):
        with patch('catalog._SOURCE_OPENER.open', side_effect=AssertionError('network')):
            store = Catalog(LocalSource(self.root))
            result = store.get_ban_to(1)
            self.assertEqual(result['content'], BODY)
            self.assertIn('/' + '1'*40 + '/', result['source_url'])
            self.assertEqual(result['content_sha256'], hashlib.sha256(BODY.encode()).hexdigest())
            self.assertEqual(result['source_mode'], 'offline_snapshot')
            self.assertFalse(store.get_nghiem_thu(1)['accepted'])
            status = store.get_source_status()
            self.assertFalse(status['network_fallback'])
            self.assertEqual(status['inventory_files'], 61)
            self.assertNotIn(str(self.root), json.dumps(status))

    def test_changed_file_is_rejected_on_every_read(self):
        source = LocalSource(self.root)
        self.assertEqual(source('v1-frozen', PATH), BODY)
        (self.root / 'v1-frozen' / PATH).write_text('modified')
        with self.assertRaisesRegex(SourceAccessError, 'checksum'):
            source('v1-frozen', PATH)

    def test_missing_inventory_differs_from_deleted_local_file(self):
        source = LocalSource(self.root)
        with self.assertRaises(SourceNotFound):
            source('v2-development', 'docs/ke-hoach-v2.md')
        (self.root / 'v1-frozen' / PATH).unlink()
        with self.assertRaises(SourceAccessError):
            source('v1-frozen', PATH)

    def test_invalid_manifests(self):
        for mutate in (
            lambda m: m['files'].pop(),
            lambda m: m['files'].append(m['files'][0]),
            lambda m: m['files'][0].update(path='../secret.md'),
            lambda m: m['commits'].update({'v1-frozen': 'main'}),
            lambda m: m['files'][0].update(branch=[]),
            lambda m: m.update(schema_version=True),
        ):
            with self.subTest(mutate=mutate):
                data = json.loads(json.dumps(self.manifest))
                mutate(data)
                (self.root / 'manifest.json').write_text(json.dumps(data))
                with self.assertRaises(SourceAccessError):
                    LocalSource(self.root)

    def test_duplicate_keys(self):
        (self.root / 'manifest.json').write_text('{"files": [], "files": []}')
        with self.assertRaises(SourceAccessError):
            LocalSource(self.root)

    def test_symlink_and_traversal(self):
        source = LocalSource(self.root)
        file = self.root / 'v1-frozen' / PATH
        file.unlink()
        file.symlink_to(self.root / 'manifest.json')
        with self.assertRaises(SourceAccessError):
            source('v1-frozen', PATH)
        with self.assertRaises(ValueError):
            source('v1-frozen', '../manifest.json')

    def test_oversized_file(self):
        source = LocalSource(self.root)
        (self.root / 'v1-frozen' / PATH).write_bytes(b'x'*(MAX_BYTES+1))
        with self.assertRaisesRegex(SourceAccessError, 'size limit'):
            source('v1-frozen', PATH)

    def test_server_explicit_offline_configuration(self):
        from server import configured_catalog
        with patch.dict(os.environ, {'VONG_CO_SOURCE_DIR': str(self.root)}):
            self.assertEqual(configured_catalog().get_source_status()['mode'], 'offline_snapshot')
        with patch.dict(os.environ, {'VONG_CO_SOURCE_DIR': str(self.root/'missing')}):
            with self.assertRaises(SourceAccessError):
                configured_catalog()

    def test_search_word_order_and_spaces(self):
        for query in ('thuy luu', '  LƯU    THỦY ', 'truong sau bac'):
            self.assertEqual(Catalog().search_ban_to(query)['works'][0]['number'], 1)


class ExportTests(unittest.TestCase):
    def test_committed_sources_and_existing_destination(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            repo = root/'repo'
            repo.mkdir()
            def git(*args):
                return subprocess.run(['git','-C',str(repo),*args],check=True,
                                      capture_output=True,text=True).stdout.strip()
            git('init','-q')
            git('config','user.name','Snapshot Test')
            git('config','user.email','snapshot@example.invalid')
            file = repo/PATH
            file.parent.mkdir(parents=True)
            file.write_text(BODY,encoding='utf-8')
            git('add','.')
            git('commit','-qm','fixture')
            for branch in BRANCHES.values():
                git('branch',branch)
            commit = git('rev-parse','HEAD')
            file.write_text('uncommitted',encoding='utf-8')
            output = root/'snapshot'
            status = export_snapshot(repo,output)
            self.assertEqual(set(status['commits'].values()),{commit})
            self.assertEqual(status['available_files'],2)
            self.assertEqual(LocalSource(output)('v1-frozen',PATH),BODY)
            with self.assertRaises(ValueError):
                export_snapshot(repo,output)
            self.assertEqual(LocalSource(output)('v1-frozen',PATH),BODY)
            self.assertFalse(list(root.glob('.vong-co-snapshot-*')))


class OfflineProtocolTests(unittest.IsolatedAsyncioTestCase):
    async def test_offline_tools_and_tampering_over_mcp(self):
        from mcp import Client
        import server
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            fixture(root)
            with patch.object(server, 'store', Catalog(LocalSource(root))):
                with patch('catalog._SOURCE_OPENER.open', side_effect=AssertionError('network')):
                    async with Client(server.mcp) as client:
                        status = await client.call_tool('get_source_status', {})
                        self.assertEqual(status.structured_content['mode'], 'offline_snapshot')
                        result = await client.call_tool('get_ban_to', {'bai_so': 1})
                        self.assertFalse(result.is_error)
                        self.assertEqual(result.structured_content['content'], BODY)
                        (root / 'v1-frozen' / PATH).write_text('tampered')
                        error = await client.call_tool('get_ban_to', {'bai_so': 1})
                        self.assertTrue(error.is_error)
