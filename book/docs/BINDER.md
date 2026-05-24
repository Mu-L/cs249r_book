# Book Binder CLI

The **Book Binder** (`./book/binder`) is the single entry point for building, checking, fixing, and formatting the MLSysBook.

## Author workflow (typical)

Most chapter work needs only **build** (and optionally **preview**). You do not need to run `check` or `fix` by hand — **pre-commit runs those on every commit** via the same `./book/binder check …` commands documented below.

```bash
# From repository root — one-time per clone
./book/binder setup

# Day to day: build what you're editing
./book/binder build html --vol1 vol1/ml_systems      # fast HTML chapter
./book/binder build pdf --vol1 vol1/ml_systems       # PDF chapter
./book/binder build epub --vol1 vol1/ml_systems      # EPUB chapter
./book/binder build html --vol1                      # whole Volume I site
./book/binder build pdf --vol1                       # whole Volume I PDF

# Optional: live reload while editing
./book/binder preview vol1/ml_systems

# When a commit is blocked, pre-commit prints the failing binder command.
# Re-run that command locally to see details, or:
./book/binder check refs --path book/quarto/contents/vol1/ml_systems/ml_systems.qmd
```

Commit as usual; hooks handle validation. Run `./book/binder check all --vol1` only when you want a full local sweep before pushing.

## Public API policy

Binder is the **single source of truth** for book automation in this repository.

- **Checks:** `./book/binder check <group> [--scope …]` — every `book-check-*` pre-commit hook dispatches here.
- **Fixes:** `./book/binder fix <topic> <action>` — maintenance and content repair (alias: `maintain`).
- **Formats:** `./book/binder format <target>` — auto-formatters (some pre-commit hooks use `format … --check`).
- Use `./book/binder …` from the **repository root**. If your shell is already in `book/`, `./binder …` is equivalent.
| Implementation | Where check logic lives |
|----------------|-------------------------|
| **Preferred** | `book/cli/checks/*.py` — imported by `validate.py` |
| **Inline** | `book/cli/commands/validate.py` — small regex/graph checks |
| **Transitional** | importlib/subprocess into `book/tools/` (being migrated) |

Scripts under `book/tools/` are not the public API. Pre-commit, CI, and editors call `./book/binder check …` only.
- The VS Code extension, pre-commit, and CI must call Binder subcommands — not scripts directly.

**Documentation map**

| Audience | Document |
|----------|----------|
| Authors & daily use | This file (`book/docs/BINDER.md`) — command reference |
| Check/fix implementation | [`book/cli/README.md`](../cli/README.md) — architecture, adding scopes, EPUB layers |
| Scope registry (code) | `book/cli/commands/validate.py` → `GROUPS` dict |
| Pre-commit wiring | `.pre-commit-config.yaml` — one hook per check group (or explicit `--scope`) |

Run `./book/binder check` with no arguments to print the live group/scope catalogue (authoritative; docs may lag).

## Quick start (full reference)

```bash
# First time setup (from repository root)
./book/binder setup
./book/binder doctor

# Build & preview — primary author commands (see BUILD.md)
./book/binder build html --vol1 vol1/training
./book/binder preview vol1/introduction

# Checks — usually pre-commit only; run locally when debugging a failed hook
./book/binder check all --vol1
./book/binder check refs --path book/quarto/contents/vol1/introduction/introduction.qmd

# Fixes — maintenance / repair (rare in daily chapter work)
./book/binder fix repo-health
./book/binder fix headers add --vol1 --dry-run

# Live command reference
./book/binder help
./book/binder check refs help    # per-group scopes and error codes
```

## Installation

The binder lives at `book/binder` (Python entry point → `book/cli/`). Ensure it is executable:

```bash
chmod +x book/binder
```

Requires Python 3.10+ and project dependencies (Rich, etc.). Run `./book/binder doctor` to verify Quarto, Java/epubcheck, and other tooling.

---

## Check — validation (`check <group>`)

> **Authors:** you usually skip this section. Pre-commit invokes these automatically on commit. Use it when a hook fails and you need the full error output, or when maintaining the check suite.

### Command shape

```bash
./book/binder check <group> [--scope <name>] [--vol1|--vol2] [--path PATH] [--json]
./book/binder check all [--vol1|--vol2]          # every group's curated scopes
./book/binder check <group> --all-scopes         # include opt-in / heavy scopes
./book/binder check <group> help                 # scopes + error codes for one group
```

`validate` is a backward-compatible alias for `check` (same parser). Prefer **`check`**.

**Important:** the first argument after `check` must be a **group name** (e.g. `refs`, `labels`), not a legacy flat name. Scopes such as `inline-python` or `duplicates` require `--scope`.

### Check groups (25 + `all`)

| Group | What it validates | Common scopes |
|-------|-------------------|---------------|
| `refs` | Cross-refs, citations, inline `{python}` refs | `cross-refs`, `citations`, `inline`; opt-in: `inline-python`, `self-ref` |
| `labels` | Duplicate and orphan `@fig-` / `@tbl-` / … labels | `duplicates`, `orphans` |
| `headers` | Section IDs (`{#sec-…}`) and headline case | `ids`, `case` |
| `bib` | Bibliography hygiene | `hygiene` |
| `footnotes` | Definition shape, placement, integrity | `definition-shape`, `placement`, `integrity` |
| `figures` | Captions, div syntax, alt text, label-required | default set in `check figures help` |
| `markup` | Low-level markup (patterns, div fences, callouts) | `patterns`, `div-fences`, `callouts` |
| `prose` | Contractions, duplicate words, above/below, … | see `check prose help` |
| `punctuation` | Em-dash, slash, vs., e.g./i.e., en-dash ranges | |
| `numbers` | Unit spacing, binary units, percent rules | |
| `math` | `\times` spacing, attribute LaTeX leaks, LEGO fmt/suffix canonical | `canonical`, `render-audit` (opt-in) |
| `structure` | Heading levels, parts, Purpose sections | |
| `code` | Python `echo: false`, `_str` LaTeX leaks, LEGO dead code | `lego-dead-code` |
| `tables` | Grid→pipe, content hygiene, caption-required | |
| `listings` | `#lst-` divs carry `lst-cap` | |
| `index` | `\index{}` placement, anti-patterns, xrefs | |
| `images` | Formats, external URLs, SVG XML | |
| `json` | JSON syntax in book tree | |
| `units` | mlsysim physics unit tests | |
| `notation` | Iron-law symbol consistency | |
| `spelling` | aspell on prose / TikZ | opt-in (needs aspell) |
| `epub` | Source hygiene; opt-in: smoke, epubcheck | `hygiene --fix` auto-repairs source |
| `sources` | Source-note / citation formatting | |
| `references` | External .bib verification (hallucinator) | opt-in, network |
| `content` | Content tree structure | opt-in |

### Examples

```bash
# Pre-commit-equivalent: all curated checks on Volume I
./book/binder check all --vol1

# Single file, inline Python execution
./book/binder check refs --scope inline-python --path book/quarto/contents/vol1/training/training.qmd

# Inline `{python}` variable references
./book/binder check refs --scope inline --path book/quarto/contents/vol1/introduction/introduction.qmd

# LEGO fmt / suffix discipline (also runs as part of `check math` on commit)
./book/binder check math --scope canonical --path book/quarto/contents/vol1/training/training.qmd

# Label hygiene
./book/binder check labels --scope duplicates --vol1
./book/binder check labels --scope orphans --vol1

# External bibliography audit (optional dependency)
./book/binder check references --scope hallucinator -f book/quarto/contents/vol1/backmatter/references.bib --limit 10

# Machine-readable output (CI / editor integration)
./book/binder check refs --json --quiet
```

Exit codes: `0` = passed, `1` = failures or command error.

### Pre-commit ↔ binder mapping

Every `book-check-*` hook in `.pre-commit-config.yaml` calls `./book/binder check …`. The hook ID mirrors the group; scopes are embedded in the `entry` when needed.

| Pre-commit hook | Binder command |
|-----------------|----------------|
| `book-check-headers` | `check headers` |
| `book-check-structure` | `check structure` |
| `book-check-labels-orphans` | `check labels --scope orphans` |
| `book-check-labels-duplicates` | `check labels --scope duplicates` |
| `book-check-refs` | `check refs` |
| `book-check-footnotes` | `check footnotes` |
| `book-check-figures` | `check figures` |
| `book-check-images` | `check images` |
| `book-check-tables` | `check tables` |
| `book-check-listings` | `check listings` |
| `book-check-tables-format` | `format tables --check` |
| `book-check-markup` | `check markup` |
| `book-check-code` | `check code` |
| `book-check-prose` | `check prose` |
| `book-check-punctuation` | `check punctuation` |
| `book-check-numbers` | `check numbers` |
| `book-check-math` | `check math` (includes `canonical` scope for LEGO fmt discipline) |
| `book-check-notation` | `check notation` |
| `book-check-index` | `check index` |
| `book-check-sources` | `check sources` |
| `book-check-json` | `check json` |
| `book-check-units` | `check units` |
| `book-check-epub` | `check epub` (scope `hygiene`) |
| `book-check-bib` | `check bib` |
| `book-check-math-render-audit` | `check math --scope render-audit` (manual stage) |

To reproduce a hook locally:

```bash
pre-commit run book-check-refs --files book/quarto/contents/vol1/introduction/introduction.qmd
# equivalent:
./book/binder check refs --path book/quarto/contents/vol1/introduction/introduction.qmd
```

### Bibliography (`.bib` + pre-commit)

Committed `.bib` files go through pre-commit in this order:

1. **`bib-apply-mechanical`** — safe field fixes on staged `.bib` only
2. **`bibtex-tidy`** — layout
3. **`./book/binder check bib --scope hygiene`** — same errors as `book/tools/bib_lint.py` (see `book/tools/bib_lint_baseline.json`)

Normalize the whole tree by hand:

```bash
./book/binder bib normalize              # all git-tracked *.bib
./book/binder bib normalize --vol1
```

Metadata refresh: `./book/binder bib update` (betterbib sync + citekey propagation).

---

## Fix — maintenance (`fix <topic> <action>`)

> **Authors:** rarely needed day to day. Pre-commit and `./book/binder fix …` overlap only for optional housekeeping (repo health, image compression, section IDs).

Canonical namespace for repairs and housekeeping. `maintain` is an alias for `fix`.

| Topic | Actions | Example |
|-------|---------|---------|
| `glossary` | `paths` | `./book/binder fix glossary paths [--vol1\|--vol2]` |
| `images` | `compress` | `./book/binder fix images compress --all --smart-compression [--apply]` |
| `repo-health` | `check` (optional) | `./book/binder fix repo-health [--json] [--min-size-mb N]` |
| `headers` | `add`, `repair`, `list`, `remove` | `./book/binder fix headers add --vol1 --dry-run` |
| `footnotes` | `cleanup`, `reorganize`, `remove` | `./book/binder fix footnotes cleanup --vol1 --dry-run` |

**Related commands (not under `fix`):**

- `./book/binder headings check|dry-run|apply` — headline-case enforcement (also runs as `check headers --scope case`)
- `./book/binder check epub --scope hygiene --fix` — auto-repair SVG/BibTeX EPUB source issues
- `./book/binder bib normalize|sync|clean|update` — bibliography tooling

---

## Build & preview (summary)

| Command | Description | Example |
|---------|-------------|---------|
| `build [html\|pdf\|epub] [chapter[,…]]` | Build book or chapter(s) | `./book/binder build pdf --vol1 vol1/intro` |
| `preview [chapter]` | Live dev server | `./book/binder preview vol1/intro` |
| `pdf\|html\|epub reset` | Reset fast-build config | `./book/binder pdf reset --vol1` |

See [BUILD.md](BUILD.md) and [DEVELOPMENT.md](DEVELOPMENT.md) for full build workflows.

### Management commands

| Command | Description |
|---------|-------------|
| `setup` | Configure environment and pre-commit |
| `clean` | Remove build artifacts |
| `switch <format>` | Switch active Quarto config symlink |
| `list` / `status` | Chapters and config status |
| `doctor` | Tooling health check |
| `help` | Command reference |

**Note:** `publish` is not a Binder subcommand. Release publishing uses GitHub Actions and scripts under `book/tools/scripts/publish/`.

---

## Chapter names

Chapters can be referenced by their short names. Common examples:

- `intro` → Introduction chapter
- `ml_systems` → Machine Learning Systems chapter
- `nn_computation` → Neural Computation chapter
- `training` → Training chapter
- `ops` → MLOps chapter

Use `./binder list` to see all available chapters.

## Build Outputs

| Format | Output Location | Description |
|--------|-----------------|-------------|
| HTML | `build/html/` | Website format with navigation |
| PDF | `build/pdf/` | Academic book format |

## Publishing

Release publishing is **not** a Binder subcommand. Use GitHub Actions and scripts under `book/tools/scripts/publish/`. The sections below describe historical `publish` behavior and may be outdated — see your team's release runbook.

<details>
<summary>Legacy publish documentation (historical)</summary>

The former `publish` CLI command has been removed from Binder.

### 1. Interactive Mode (Default)

When called without arguments, `publish` runs the interactive wizard:

```bash
# Interactive publishing wizard
./binder publish
```

**What interactive mode does:**

1. **🔍 Pre-flight checks** - Verifies git status and branch
2. **🧹 Cleans** - Removes previous builds
3. **📚 Builds HTML** - Creates web version
4. **📄 Builds PDF** - Creates downloadable version
5. **📦 Copies PDF** - Moves PDF to assets directory
6. **💾 Commits** - Adds PDF to git
7. **🚀 Pushes** - Triggers GitHub Actions deployment

### 2. Command-Line Trigger Mode

When called with arguments, `publish` triggers the GitHub Actions workflow directly:

```bash
# Trigger GitHub Actions workflow
./binder publish "Description" [COMMIT_HASH]

# With options
./binder publish "Add new chapter" abc123def --type patch --no-ai
```

**What command-line mode does:**

1. **🔍 Validates environment** - Checks GitHub CLI, authentication, branch
2. **✅ Validates commit** - Ensures the dev commit exists (if provided)
3. **🚀 Triggers workflow** - Uses GitHub CLI to trigger the publish-live workflow
4. **📊 Provides feedback** - Shows monitoring links and next steps

**Options:**
- `--type patch|minor|major` - Release type (default: minor)
- `--no-ai` - Disable AI release notes
- `--yes` - Skip confirmation prompts

**Requirements:**
- GitHub CLI installed and authenticated (`gh auth login`)
- Must be on main or dev branch
- Dev commit must exist (if provided)

### Publishing Workflow:

```bash
# Development workflow
./binder preview intro          # Preview a chapter
./binder build                  # Build complete HTML
./binder build pdf              # Build complete PDF
./binder publish                # Publish to the world
```

### After Publishing:

- **🌐 Web version**: Available at https://harvard-edge.github.io/cs249r_book
- **📄 PDF download**: Available at https://harvard-edge.github.io/cs249r_book/assets/downloads/Machine-Learning-Systems.pdf
- **📈 GitHub Actions**: Monitors build progress at https://github.com/harvard-edge/cs249r_book/actions

### Requirements:

- Must be on `main` branch
- No uncommitted changes
- Git repository properly configured

</details>

## Advanced Features

### Unified Multi-Chapter Builds

The binder supports building multiple chapters together in a single Quarto render command:

```bash
# Build multiple chapters together (HTML)
./binder build intro,ml_systems

# Build multiple chapters together (PDF)
./binder build pdf intro,ml_systems

# Preview multiple chapters together
./binder preview intro,ml_systems
```

**Benefits:**
- ✅ **Faster builds**: Single Quarto process instead of multiple
- ✅ **Shared context**: Dependencies loaded once
- ✅ **Unified processing**: Cross-references and quizzes processed together
- ✅ **Better UX**: Single browser window opens with complete site

### Fast Build Mode

Fast builds use selective rendering to only build essential files plus target chapters:

**HTML Fast Build** (project.render):
```yaml
render:
  - index.qmd
  - 404.qmd
  - contents/frontmatter/
  - contents/core/target-chapter.qmd
```

**PDF Fast Build** (comments out unused chapters):
```yaml
chapters:
  - index.qmd
  - contents/frontmatter/foreword.qmd
  - contents/core/target-chapter.qmd
  # - contents/core/other-chapter.qmd  # Commented for fast build
```

#### Selective PDF Chapter Building

When you run `./binder build pdf intro`, the system automatically:

1. **Creates a backup** of the original PDF configuration
2. **Comments out all chapters** except the target chapter and essential files
3. **Builds only the selected content**:
   - ✅ `index.qmd` (always included)
   - ✅ `contents/core/introduction/introduction.qmd` (target chapter)
   - ❌ `contents/backmatter/glossary/glossary.qmd` (commented out)
   - ❌ `contents/backmatter/references.qmd` (commented out)
4. **Restores the original configuration** after build completion

**Example output:**
```bash
./binder build pdf intro

📄 Building chapter(s) as PDF: intro
🚀 Building 1 chapters (pdf)
⚡ Setting up fast build mode...
📋 Files to build: 2 files
✓ - index.qmd
✓ - contents/core/introduction/introduction.qmd
✓ Fast build mode configured (PDF/EPUB)
```

This ensures that in Binder environments, you get exactly what you need: a PDF containing only the index and your target chapter, with all other chapters automatically commented out during the build process.

#### Cloud Binder Compatibility

The selective PDF build system works seamlessly in cloud environments like [mybinder.org](https://mybinder.org):

**For cloud Binder users:**
```bash
# In a Jupyter terminal or notebook cell
!./binder build pdf intro

# Or using the Python CLI directly
!python binder build pdf intro
```

**Key benefits for cloud environments:**
- ✅ **Reduced memory usage** - Only builds essential chapters
- ✅ **Faster build times** - Skips unnecessary content
- ✅ **Automatic cleanup** - Restores configuration after build
- ✅ **No manual editing** - Everything is automated

**What gets built:**
- Always includes `index.qmd` for proper book structure
- Includes your target chapter (e.g., `introduction.qmd`)
- Comments out all other chapters automatically
- Comments out backmatter (glossary, references) for minimal builds

### Configuration Management

The binder automatically manages Quarto configurations:

- **`_quarto-html.yml`**: Website build configuration
- **`_quarto-pdf.yml`**: Academic PDF build configuration
- **`_quarto.yml`**: **Symlink** to active configuration (currently → `config/_quarto-html.yml`)

**Important**: The `_quarto.yml` file is a symlink that points to the active configuration. This allows the binder to quickly switch between HTML and PDF build modes without copying files.

**Quarto Executable**: The system quarto executable (`/Applications/quarto/bin/quarto`) is NOT a symlink - it's a regular executable file.

Use `./binder switch <format>` to change the active configuration symlink.

## Development Workflow

### Typical Chapter Development

```bash
# 1. Start development on a chapter
./binder preview intro

# 2. Make edits, save files (auto-rebuild in preview mode)

# 3. Build multiple related chapters together
./binder build intro,ml_systems html

# 4. Check full book before committing
./binder build * pdf
```

### Before Committing

```bash
# Clean up any build artifacts
./binder clean

# Run health check
./binder doctor

# Build full book to ensure everything works
./binder build
./binder build pdf
```

## Troubleshooting

### Common Issues

**"Chapter not found"**
- Use `./binder list` to see available chapters
- Check that the chapter QMD file exists
- Verify the chapter path in configuration files

**"Build artifacts detected"**
- Run `./binder clean` to remove temporary files
- Use `./binder doctor` to verify system health

**"Config not clean"**
- The binder detected a previous fast build configuration
- Run `./binder clean` to restore normal configuration

**"Symlink issues"**
- If `_quarto.yml` is not a symlink: `ln -sf config/_quarto-html.yml book/_quarto.yml`
- Check current symlink target: `ls -la book/_quarto.yml`
- The symlink should point to either `config/_quarto-html.yml` or `config/_quarto-pdf.yml`

### Performance Tips

- Use fast builds (`./binder build chapter html`) for development
- Use unified builds (`./binder build ch1,ch2 html`) for multiple chapters
- Only use full builds (`./binder build * format`) for final verification
- Preview mode auto-rebuilds on file changes

## Further reading

- [BUILD.md](BUILD.md) — build instructions
- [DEVELOPMENT.md](DEVELOPMENT.md) — development setup
- [`book/cli/README.md`](../cli/README.md) — check/fix architecture, adding scopes, EPUB layers
