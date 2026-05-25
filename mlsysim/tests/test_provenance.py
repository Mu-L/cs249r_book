import unittest
import pint
from mlsysim.core.provenance import TraceableConstant
from mlsysim.core.constants import ureg


class TestTraceableConstant(unittest.TestCase):
    def test_system_assumption_behaves_like_float(self):
        assump = TraceableConstant(
            0.85,
            name="Test MFU",
            description="A test assumption.",
            citation="Test Citation",
        )
        self.assertIsInstance(assump, float)
        self.assertEqual(assump, 0.85)
        self.assertEqual(assump * 2, 1.7)
        self.assertAlmostEqual(1.0 - assump, 0.15)
        self.assertEqual(assump / 2, 0.425)
        self.assertGreater(assump, 0.80)

    def test_system_assumption_preserves_metadata(self):
        assump = TraceableConstant(
            0.50,
            name="Test MFU",
            description="A test assumption.",
            citation="Test Citation",
            url="https://example.com",
            bib_keys="test2020",
            source_type="literature",
            last_verified="2025-03-06",
        )
        self.assertEqual(assump.bib_keys, "test2020")
        md = assump.render_markdown()
        self.assertIn("Test MFU", md)
        self.assertIn("https://example.com", md)
        self.assertIn("test2020", md)

    def test_gpu_mttf_bib_keys_match_book(self):
        from mlsysim.core import defaults

        self.assertIn("kokolis2025", defaults.GPU_MTTF_HOURS.bib_keys)
        self.assertIn("zu2024tpuv4", defaults.GPU_MTTF_HOURS.bib_keys)
        self.assertIn("barroso2019", defaults.GPU_MTTF_HOURS.bib_keys)

    def test_system_assumption_with_pint(self):
        assump = TraceableConstant(
            15.0,
            name="Test Overhead",
            description="Overhead in ms.",
            citation="Test Citation",
        )
        quant = assump * ureg.ms
        self.assertIsInstance(quant, pint.Quantity)
        self.assertEqual(quant.magnitude, 15.0)
        rate = 1.0 / quant
        self.assertAlmostEqual(rate.magnitude, 1 / 15.0)


if __name__ == "__main__":
    unittest.main()
