import unittest

from mlsysim.core.appendix_lineage import audit_appendix_defaults
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

    def test_appendix_defaults_have_lineage(self):
        issues = audit_appendix_defaults()
        self.assertEqual(issues, [], "\n".join(issues))


if __name__ == "__main__":
    unittest.main()
