# AI Disclosure — Draft for Acknowledgments

**Status:** Canonical content lives in:
- `book/quarto/contents/vol1/frontmatter/ai_use.qmd`
- `book/quarto/contents/vol2/frontmatter/ai_use.qmd`

Both files are committed to the repo but **not yet wired into the build** — the
`_quarto-*-vol1.yml` and `_quarto-*-vol2.yml` configs do not include them. To
integrate when ready, add `- contents/vol1/frontmatter/ai_use.qmd` between
`about.qmd` and `acknowledgements.qmd` in each volume's `chapters:` list, and
the HTML sidebar nav entries in the corresponding `_quarto-html-vol*.yml`.

This file documents the process: three rounds of adversarial review complete
(skeptical-educator, peer CS prof, hostile reader). Final hostile-reader
verdict: "attack softened" — the single-screenshot dunk vectors are closed.
Vol1 and Vol2 use identical text per author decision 2026-05-20.

**Open question to resolve before commit:** Should "cross-reference and notation
consistency" be expanded to "cross-reference, terminology, and notation
consistency"? The CS-prof reviewer recommended adding "terminology" — the
harder corpus-wide discipline of keeping concept terms (e.g. "activation",
"feature map", "tensor") consistent across 20 chapters. Single-word add, no
reviewer flagged a downside.

---

## A Note on AI Assistance {.unnumbered}

Every chapter of this book was researched, written, and rewritten by me. I also
used AI tools throughout.

This book teaches the engineering of machine learning systems. Its companion
labs, simulator, and hardware kits ask students to engineer these systems
themselves, not just read about them. Writing the book without the tools it
teaches about would have asked students to engage with infrastructure their
teacher chose to avoid. Students learn more about these tools by seeing them
used responsibly.

In practice, AI helped me brainstorm framings I then chose between, survey
literature, draft passages I then rewrote substantially, and audit the
manuscript for cross-reference and notation consistency. Every source AI
surfaced I then read in the original before keeping it — hallucination is real,
and an unverified citation has no place in a textbook. The intellectual
framework, the examples, the chapter-to-chapter argument, and the choice of
what to include and what to leave out are mine. The errors that remain are
mine too. In keeping with MIT Press policy, AI systems are not listed as
authors.
