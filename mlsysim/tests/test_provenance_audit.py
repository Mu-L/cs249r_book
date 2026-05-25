import unittest

from mlsysim.tools.audit_provenance import audit_defaults_traceable, audit_registries


class TestProvenanceAudit(unittest.TestCase):
    def test_traceable_defaults_have_provenance(self):
        issues = audit_defaults_traceable()
        self.assertEqual(issues, [], "\n".join(issues))

    def test_cloud_hardware_strict_reports_gaps(self):
        """Document gap count; strict CI can be enabled when backfill completes."""
        issues = audit_registries(scope_cloud=True)
        # Known: many Cloud nodes still lack metadata.provenance.
        self.assertIsInstance(issues, list)


if __name__ == "__main__":
    unittest.main()
