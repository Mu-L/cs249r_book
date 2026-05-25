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
            source="Test Citation",
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
            source="Test Citation",
            url="https://example.com",
        )
        self.assertEqual(assump.source, "Test Citation")
        md = assump.render_markdown()
        self.assertIn("Test MFU", md)
        self.assertIn("https://example.com", md)
        self.assertIn("Test Citation", md)

    def test_gpu_mttf_source_mentions_reliability_literature(self):
        from mlsysim.core import defaults

        prov = defaults.GPU_MTTF_HOURS.provenance
        self.assertIn("Kokolis", prov.ref)
        self.assertIn("Zu", prov.ref)
        self.assertIn("Barroso", prov.ref)

    def test_carbon_constants_share_iea_catalog_id(self):
        from mlsysim.core import defaults

        self.assertEqual(
            defaults.CARBON_NORWAY_GCO2_KWH.provenance.id,
            defaults.CARBON_POLAND_GCO2_KWH.provenance.id,
        )

    def test_system_assumption_with_pint(self):
        assump = TraceableConstant(
            15.0,
            name="Test Overhead",
            description="Overhead in ms.",
            source="Test Citation",
        )
        quant = assump * ureg.ms
        self.assertIsInstance(quant, pint.Quantity)
        self.assertEqual(quant.magnitude, 15.0)
        rate = 1.0 / quant
        self.assertAlmostEqual(rate.magnitude, 1 / 15.0)


if __name__ == "__main__":
    unittest.main()
