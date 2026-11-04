"""Every published historical phrase index must pass its own source checks."""
import copy
from pathlib import Path
import sys
import tempfile
import unittest
from unittest.mock import patch

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / 'scripts'))
import v3_build_site as builder


class BuildRegressionTests(unittest.TestCase):
    def test_invalid_historical_indexes_block_publication_before_writes(self):
        original_load = builder.strict_load
        for index in (builder.V32_INDEX, builder.V33_INDEX, builder.V34_INDEX):
            def changed(path):
                result = original_load(path)
                if path == index:
                    result = copy.deepcopy(result)
                    result['items'] = []
                return result
            with self.subTest(index=str(index)), tempfile.TemporaryDirectory() as tmp:
                output = Path(tmp) / 'site'
                with patch.object(builder, 'strict_load', side_effect=changed):
                    with self.assertRaises(ValueError):
                        builder.build(output)
                self.assertFalse(output.exists())

    def test_late_failure_leaves_no_partial_site_and_retry_succeeds(self):
        for existing in (False, True):
            with self.subTest(existing=existing), tempfile.TemporaryDirectory() as tmp:
                output = Path(tmp) / 'site'
                if existing:
                    output.mkdir()
                with patch.object(builder, 'stamp_site_revision', side_effect=OSError('disk error')):
                    with self.assertRaises(OSError):
                        builder.build(output)
                self.assertEqual(output.exists(), existing)
                if existing:
                    self.assertEqual(list(output.iterdir()), [])
                self.assertFalse(list(Path(tmp).glob('.vong-co-build-*')))
                result = builder.build(output)
                self.assertEqual(result['status'], 'pass')
                self.assertTrue((output / 'site-version.json').is_file())

    def test_existing_site_is_never_overwritten(self):
        with tempfile.TemporaryDirectory() as tmp:
            output = Path(tmp) / 'site'
            output.mkdir()
            marker = output / 'index.html'
            marker.write_text('existing website')
            with self.assertRaises(ValueError):
                builder.build(output)
            self.assertEqual(marker.read_text(), 'existing website')

    def test_destination_created_during_build_is_preserved(self):
        with tempfile.TemporaryDirectory() as tmp:
            output = Path(tmp) / 'site'
            original = builder.stamp_site_revision
            def concurrent_write(staged):
                output.mkdir()
                (output / 'user.txt').write_text('keep')
                return original(staged)
            with patch.object(builder, 'stamp_site_revision', side_effect=concurrent_write):
                with self.assertRaises(ValueError):
                    builder.build(output)
            self.assertEqual((output / 'user.txt').read_text(), 'keep')
            self.assertEqual(len(list(output.iterdir())), 1)
            self.assertFalse(list(Path(tmp).glob('.vong-co-build-*')))

    def test_symlink_destination_is_rejected(self):
        with tempfile.TemporaryDirectory() as tmp:
            real = Path(tmp) / 'real'
            real.mkdir()
            output = Path(tmp) / 'site'
            output.symlink_to(real, target_is_directory=True)
            with self.assertRaises(ValueError):
                builder.build(output)
            self.assertEqual(list(real.iterdir()), [])

    def test_rename_failure_restores_empty_destination(self):
        with tempfile.TemporaryDirectory() as tmp:
            output = Path(tmp) / 'site'
            output.mkdir()
            with patch.object(Path, 'rename', side_effect=OSError('rename failed')):
                with self.assertRaises(OSError):
                    builder.build(output)
            self.assertTrue(output.is_dir())
            self.assertEqual(list(output.iterdir()), [])
            self.assertFalse(list(Path(tmp).glob('.vong-co-build-*')))
