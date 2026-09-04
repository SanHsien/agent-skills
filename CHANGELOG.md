[English](CHANGELOG.en.md) | 中文版

# 變更紀錄

格式參考 [Keep a Changelog](https://keepachangelog.com/zh-TW/1.1.0/)，新的在上面。
本檔只記錄**本 fork 的維護歷史**（2026-09-04 起）；上游
[`addyosmani/agent-skills`](https://github.com/addyosmani/agent-skills) 的產品演進見其自身歷史
與 [`docs/UPSTREAM.md`](docs/UPSTREAM.md) 的審查清冊。逐筆採用／略過的理由記在
[`docs/DECISIONS.md`](docs/DECISIONS.md)。

---

## [Unreleased] - 2026-09-04

### 新增

- **Windows-first 維護骨架。** `AGENTS.md`／`CLAUDE.md` 尾端加上 fork 維護規則一節（不動既有
  上游內容）、`FORK.md`、`NOTICE.md`、`SECURITY.md`、`CODE_OF_CONDUCT.md`、`docs/DEVELOPMENT.md`、
  `docs/UPSTREAM.md`、`docs/DECISIONS.md`、`tools/` 維護腳本（`dev_check.ps1`、
  `check_upstream_updates.py`、`check_dependency_freshness.py`、`check_links.py`、
  `upstream_baseline.json`）、對應的 `tests/`，以及 `.github/` 的 CI／CodeQL／Dependabot／
  上游檢查／依賴新鮮度 workflow。CI 在 Ubuntu 跑 Python 3.14 + Node 24（pytest、ruff E9+F、
  `node scripts/validate-skills.js`、`node scripts/validate-commands.js`、相對連結檢查），
  加一個 Windows job 跑同一套 `tools/dev_check.ps1`；上游既有的
  `.github/workflows/test-plugin-install.yml`（skill／command 全量驗證、eval、plugin 安裝煙霧
  測試）維持不動，不重複覆蓋。
- **公開入口只留繁中與英文。** `README.md` 改為繁中主檔，`README.en.md` 為上游英文原文的逐字
  鏡像（加語言切換列）。來源與授權 credit 保留，個人事業／贊助段落上游本來就沒有，不需另行剔除。

### 說明

- 產品 `skills/`、`commands/`、`.claude/commands/`、`.gemini/commands/`、`agents/`、`hooks/`、
  `references/`、`evals/`、`scripts/`、既有 `docs/*.md`、`.claude-plugin/`、`.codex-plugin/`、
  `.agents/`、`.gemini/`、`.opencode/`、`plugin.json`、`LICENSE`、`CONTRIBUTING.md`、
  `.gitignore`、`.gitattributes` 以上游為準，本次疊加不觸碰。
