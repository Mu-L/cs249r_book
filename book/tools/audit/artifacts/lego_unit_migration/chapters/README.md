# Per-chapter gate artifacts (parallel-safe)

**Do not edit `../JOURNAL.md` or `../PLAYBOOK.md` while gating a chapter.**
Those files are merged in batch from this directory to avoid serialization conflicts.

## Each worker owns one file set

| File | Purpose |
|------|---------|
| `volN_chapter.md` | Human gate log (steps 0–13) |
| `volN_chapter_llm.json` | LLM coherence report (`--report` path) |
| `volN_chapter.status.yaml` | Machine-readable sign-off (for `sync_lego_journal.py`) |

## Status YAML schema

```yaml
chapter: vol1/data_selection
cells: 23
llm: PASS          # PASS | FAIL | WARN
cells_audit: "23/23"
html: PASS
sign_off: false
commit: null
updated: "2026-05-26"
blocker: null      # set if stopped
```

## Lessons (parallel-safe)

Append one line per insight to `_lessons_pending.md` (not PLAYBOOK.md):

```
- [vol1/data_selection] 2026-05-26: <lesson>
```

Maintainer runs `sync_lego_journal.py` to refresh `JOURNAL.md` from all `*.status.yaml` files.
