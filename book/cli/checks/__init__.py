"""
Binder-native check implementations.

Check logic that powers ``./book/binder check <group> --scope …`` lives here
as ordinary Python modules. ``book/cli/commands/validate.py`` imports from
this package and converts results to ``ValidationIssue`` records.

Standalone scripts under ``book/tools/`` may remain as thin CLIs for ad-hoc
use, but they must import from ``cli.checks`` — not the other way around.

See ``book/cli/README.md`` → "Check implementation layout".
"""
