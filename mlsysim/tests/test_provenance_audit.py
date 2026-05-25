import unittest

from mlsysim.tools.audit_provenance import (
    audit_defaults_traceable,
    audit_infra_grids,
    audit_registries,
)


class TestProvenanceAudit(unittest.TestCase):
    def test_traceable_defaults_have_provenance(self):
        issues = audit_defaults_traceable()
        self.assertEqual(issues, [], "\n".join(issues))

    def test_all_registries_have_provenance(self):
        issues = audit_registries(scope_cloud=False)
        self.assertEqual(issues, [], "\n".join(issues))

    def test_infra_grids_have_provenance(self):
        issues = audit_infra_grids()
        self.assertEqual(issues, [], "\n".join(issues))


if __name__ == "__main__":
    unittest.main()
