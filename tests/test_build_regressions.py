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
