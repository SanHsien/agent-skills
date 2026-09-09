English | [中文版](CHANGELOG.md)

# Changelog

Format follows [Keep a Changelog](https://keepachangelog.com/en/1.1.0/); newest first.
This file records **this fork's maintenance history** only (from 2026-09-04). The product
history of upstream [`addyosmani/agent-skills`](https://github.com/addyosmani/agent-skills)
lives in its own history and in the review ledger at
[`docs/UPSTREAM.md`](docs/UPSTREAM.md). Per-commit adopt/skip reasoning is recorded in
[`docs/DECISIONS.md`](docs/DECISIONS.md).

---

## [Unreleased] - 2026-09-09

### Fixed

- **Dependency freshness was blind to every CodeQL pin.** `_USES_RE` matched only `owner/repo@`, so the three-segment `github/codeql-action/init` and `/analyze` in `codeql.yml` never reached the report. The path now allows subdirectories and the release lookup trims back to the repository that owns the tags.
- **An uncomparable "latest" no longer reads as OK.** `github/codeql-action` tags its latest release `codeql-bundle-v2.26.4`, which shares no numbering with the pinned `v4.37.4`, so the comparison silently returned "not newer" forever. The lookup now falls back to the tag list and takes the newest parseable version; when nothing is comparable the row is `CHECK FAILED` — a check that cannot fail is not a check.
- **Repinned the CodeQL action from v4.37.4 to v4.37.9** (SHA `cdf488f`) — real drift, caught on the first run after the fix.

Both defects were found while porting this checker into `SanHsien/dashi-ppt-skill`; the same fix landed in both repositories.

---

## [Unreleased] - 2026-09-04

### Added

- **Windows-first maintenance overlay.** Appended a "fork maintenance rules" section to the
  end of `AGENTS.md` and `CLAUDE.md` (existing upstream content untouched), plus `FORK.md`,
  `NOTICE.md`, `SECURITY.md`, `CODE_OF_CONDUCT.md`, `docs/DEVELOPMENT.md`, `docs/UPSTREAM.md`,
  `docs/DECISIONS.md`, maintenance scripts under `tools/` (`dev_check.ps1`,
  `check_upstream_updates.py`, `check_dependency_freshness.py`, `check_links.py`,
  `upstream_baseline.json`), the matching `tests/`, and GitHub workflows for CI, CodeQL,
  Dependabot, upstream review, and dependency freshness. CI runs Ubuntu Python 3.14 + Node 24
  (pytest, ruff E9+F, `node scripts/validate-skills.js`, `node scripts/validate-commands.js`,
  relative-link checks) plus a Windows job running the same `tools/dev_check.ps1`; the existing
  `.github/workflows/test-plugin-install.yml` (full skill/command validation, evals, plugin
  install smoke test) is left untouched and not duplicated.
- **Public entry in Traditional Chinese and English only.** `README.md` is now the Chinese
  primary file; `README.en.md` is a verbatim mirror of the upstream English README with a
  language-switcher header added. Source and license credit are preserved.

### Notes

- Product `skills/`, `commands/`, `.claude/commands/`, `.gemini/commands/`, `agents/`,
  `hooks/`, `references/`, `evals/`, `scripts/`, existing `docs/*.md` files,
  `.claude-plugin/`, `.codex-plugin/`, `.agents/`, `.gemini/`, `.opencode/`, `plugin.json`,
  `LICENSE`, `CONTRIBUTING.md`, `.gitignore`, and `.gitattributes` follow upstream as-is; this
  overlay does not touch them.
