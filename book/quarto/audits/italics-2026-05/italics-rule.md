---
paths:
  - "**/*.qmd"
---

# Italics Rule - MLSysBook

**Status.** This rule operationalizes `.claude/rules/book-prose.md` Section 1b for MIT Press release review. It does not replace `book-prose.md`; it gives agents a focused decision procedure for italic markup.

Read this together with:

1. `.claude/rules/book-prose.md` Section 1b, "Emphasis & Typographic Conventions."
2. `.claude/rules/bold.md` for the distinction between emphasis and formal-status markup.
3. MIT Press copyeditor style sheet at `/Users/VJ/Desktop/MIT_Press_Feedback/13_style_rules/data/style_sheet.txt`.

## 1. Core Rule

MIT Press permits italic as the emphasis mechanism: not bold and not underlining. MLSysBook narrows that permission because a systems textbook cannot look visually over-marked.

Every italic span must do a named job. If the span only makes prose "pop," remove it.

Allowed jobs:

- **Interrogative signpost**: italicize *how*, *what*, *why*, *when*, or *where* only when the word marks a conceptual pivot in declarative prose.
- **Contrastive pair**: italicize both sides of a direct opposition, such as *training* vs. *inference* or *logical* vs. *physical*.
- **Impossibility negation**: italicize *cannot* or *not* only for physical, mathematical, or logical impossibility.
- **Words used as words**: italicize a term when the prose is talking about the word or phrase itself.
- **Coordinating emphasis**: use italics around properties or dimensions that qualify a bold first-definition in the same passage.
- **Non-obvious coupling**: italicize *and* only when the coupling is the point, not for routine pairs.
- **Thesis punchline**: italicize a full sentence or compact clause that states the controlling insight of a section.
- **Purpose hook**: the chapter Purpose question uses underscore italics (`_Question?_`) as specified in `book-prose.md`.
- **Fallacy/pitfall statement**: the misconception sentence after `**Fallacy**:` or `**Pitfall**:` is italic.
- **Title/source style**: italicize source titles that Chicago/MIT style expects in italics, such as periodical, book, or named-work titles.
- **Math/variable style**: variables appear in italic type; prefer math mode (`$k$`, `$n$`) when the symbol is a mathematical variable rather than an English word.

## 2. Decision Test

For each italic span, ask:

1. Which allowed job does it perform?
2. Would the sentence lose meaning, contrast, or navigational structure if the italics were removed?
3. If it is a contrast, are both sides marked symmetrically?
4. If it is a thesis punchline, is the whole punchline marked rather than a single stressed verb or adjective?
5. Is the span actually a label, table entry, or mini-heading that should be roman text or a bold structural lead-in instead?

If the answer to the first question is unclear, remove the italics.

## 3. Common Removals

Remove italics from:

- Single-word intensifiers: *every*, *any*, *must*, *will*, *more*, *better*, *entire*, *already*, *before*, *after*.
- Practical negations that are not impossibilities: ordinary *not*, *cannot*, or *must* emphasis.
- Routine concept phrases: *serving hierarchy*, *ranking cascade*, *training emissions calculation*, *optimization framework*.
- Product or framework names: use roman text for PyTorch, TensorFlow, TFX, CUDA, and similar names unless Chicago title style applies.
- Table/list labels and local pseudo-headings: *Use Case*, *Complexity*, *Result*, *Verdict*, *Risk*, *Benefit*, *Recommendation*.
- Checklist or checkpoint question words where the question form already supplies the cue.

When the italic span is a functional label inside a callout or list, prefer the house structural pattern from `book-prose.md` and `bold.md`: `**Result**:`, `**Recommendation**:`, `**Risk**:`, with the colon outside the bold span.

## 4. Common Revisions

Revise, rather than simply remove, when the underlying rhetorical move is valid but the markup is wrong:

- **Half-marked contrast**: If only one side is italic, either italicize both sides or remove both.
- **Wrong contrast target**: If the sentence contrasts training and inference, do not italicize a preposition such as *during*; mark the actual terms or leave them roman.
- **Single-word thesis stress**: Replace isolated *is*, *are*, or *will* emphasis with a full italic thesis sentence only when the sentence is truly a punchline.
- **Italic lead-ins**: Convert italic lead-ins such as *Result:* or *Recommendation:* to bold structural labels when the context permits.
- **Variable references**: Convert prose-symbol italics to math mode when the symbol is a mathematical variable.

## 5. Density Rule

Italics density is a type check, not a count. A paragraph may contain several italic spans if each span has a different necessary job, but visual confetti is a defect. When a paragraph has more than three formatted elements across bold and italic, re-audit every span and remove anything that does not carry structural meaning.

## 6. Audit Workflow

For chapter release review:

1. Extract single-asterisk spans from the chapter, excluding bullets, code fences, raw math syntax, and generated code comments.
2. Classify each span against the allowed jobs above.
3. Mark each span `keep`, `remove`, or `revise`.
4. Add suggested italics only when they clarify an existing contrast, impossibility, word-as-word use, source title, or variable style issue.
5. Do not apply prose edits from the audit mechanically. The YAML finding is a review ledger; a later editing pass should apply only the recommendations that still read correctly in full context.

## 7. Reporting Format

Use this YAML shape for chapter-level audits:

```yaml
chapter: "Vol. X Ch. Y Title"
file: "book/quarto/contents/..."
summary:
  existing_italic_spans_reviewed: 0
  keep: 0
  remove: 0
  revise: 0
  suggested_additions: 0
existing_italics:
  - line: 0
    span: "*...*"
    context: "short surrounding sentence"
    kind: "interrogative-signpost|contrastive-pair|impossibility-negation|word-used-as-word|coordinating-emphasis|non-obvious-coupling|thesis-punchline|purpose-hook|fallacy-pitfall|title-source|math-variable|ornamental-emphasis|other"
    recommendation: "keep|remove|revise"
    rationale: "brief editorial rationale"
    proposed_text: null
suggested_additions: []
notes: []
```
