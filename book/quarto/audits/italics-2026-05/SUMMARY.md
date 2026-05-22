# Italics Audit Summary

Scope: main chapters only, excluding front matter, part openers, appendices, glossary, and references.

Policy basis:

- `.claude/rules/book-prose.md` Section 1b
- `/Users/VJ/Desktop/MIT_Press_Feedback/13_style_rules/data/style_sheet.txt`
- MIT Press copyedit annotation ledgers under `/Users/VJ/Desktop/MIT_Press_Feedback`

## Totals

| Metric | Count |
|---|---:|
| Chapter audit ledgers generated | 33 |
| Existing italic spans reviewed | 2,211 |
| Keep | 1,938 |
| Remove | 187 |
| Revise | 86 |
| Suggested additions | 8 |

The dominant recommendation is to keep existing italics when they perform structural work. Removal candidates are concentrated in ornamental emphasis, especially single-word stress and pseudo-heading/list-label italics. Revision candidates are mostly valid contrasts where only one side of the pair is marked.

## Main Findings

- **Keep**: interrogative signposts, words used as words, contrastive pairs, fallacy/pitfall statements, source-title style, and thesis punchlines were usually defensible.
- **Remove**: generic stress on intensifiers such as *every*, *must*, *any*, *more*, and *will* should generally become roman text.
- **Remove**: italic table/list labels and mini-headings should usually become roman labels or bold structural lead-ins.
- **Revise**: half-marked contrasts should either mark both sides or neither side.
- **Add sparingly**: only 8 additions were suggested across 33 chapters, mainly for impossibility, complete contrastive pairs, and variable/title style.

## Per-Chapter Counts

| Chapter | Reviewed | Keep | Remove | Revise | Add |
|---|---:|---:|---:|---:|---:|
| Vol. 1 Ch. 1 Introduction | 84 | 78 | 5 | 1 | 4 |
| Vol. 1 Ch. 2 ML Systems | 72 | 48 | 22 | 2 | 0 |
| Vol. 1 Ch. 3 ML Workflow | 81 | 68 | 13 | 0 | 0 |
| Vol. 1 Ch. 4 Data Engineering | 73 | 63 | 7 | 3 | 0 |
| Vol. 1 Ch. 5 Neural Network Computation | 82 | 74 | 7 | 1 | 1 |
| Vol. 1 Ch. 6 Neural Network Architectures | 117 | 114 | 2 | 1 | 1 |
| Vol. 1 Ch. 7 ML Frameworks | 145 | 137 | 6 | 2 | 2 |
| Vol. 1 Ch. 8 Training | 87 | 84 | 1 | 2 | 0 |
| Vol. 1 Ch. 9 Data Selection | 99 | 83 | 9 | 7 | 0 |
| Vol. 1 Ch. 10 Model Compression | 81 | 66 | 10 | 5 | 0 |
| Vol. 1 Ch. 11 Hardware Acceleration | 105 | 99 | 3 | 3 | 0 |
| Vol. 1 Ch. 12 Benchmarking | 78 | 66 | 10 | 2 | 0 |
| Vol. 1 Ch. 13 Model Serving | 129 | 107 | 7 | 15 | 0 |
| Vol. 1 Ch. 14 ML Operations | 105 | 98 | 6 | 1 | 0 |
| Vol. 1 Ch. 15 Responsible Engineering | 84 | 82 | 2 | 0 | 0 |
| Vol. 1 Ch. 16 Conclusion | 35 | 32 | 2 | 1 | 0 |
| Vol. 2 Ch. 1 Introduction | 114 | 107 | 6 | 1 | 0 |
| Vol. 2 Ch. 2 Compute Infrastructure | 116 | 96 | 12 | 8 | 0 |
| Vol. 2 Ch. 3 Network Fabrics | 34 | 28 | 4 | 2 | 0 |
| Vol. 2 Ch. 4 Data Storage | 65 | 57 | 5 | 3 | 0 |
| Vol. 2 Ch. 5 Distributed Training Systems | 37 | 28 | 6 | 3 | 0 |
| Vol. 2 Ch. 6 Collective Communication | 54 | 35 | 17 | 2 | 0 |
| Vol. 2 Ch. 7 Fault Tolerance | 31 | 30 | 1 | 0 | 0 |
| Vol. 2 Ch. 8 Fleet Orchestration | 45 | 40 | 4 | 1 | 0 |
| Vol. 2 Ch. 9 Performance Engineering | 38 | 37 | 1 | 0 | 0 |
| Vol. 2 Ch. 10 Inference at Scale | 24 | 18 | 3 | 3 | 0 |
| Vol. 2 Ch. 11 Edge Intelligence | 12 | 7 | 2 | 3 | 0 |
| Vol. 2 Ch. 12 Operations at Scale | 87 | 86 | 1 | 0 | 0 |
| Vol. 2 Ch. 13 Security and Privacy | 27 | 21 | 6 | 0 | 0 |
| Vol. 2 Ch. 14 Robust AI | 24 | 17 | 2 | 5 | 0 |
| Vol. 2 Ch. 15 Sustainable AI | 21 | 12 | 5 | 4 | 0 |
| Vol. 2 Ch. 16 Responsible AI | 20 | 15 | 0 | 5 | 0 |
| Vol. 2 Ch. 17 Conclusion | 5 | 5 | 0 | 0 | 0 |

## Files

Detailed per-chapter YAML ledgers were generated as temporary review artifacts and are intentionally not committed with the release-prep prose changes.

New operational rule: `.claude/rules/italics.md`.

Release-facing mirror in the MLSysBook worktree: `book/quarto/audits/italics-2026-05/`, including `italics-rule.md`.
