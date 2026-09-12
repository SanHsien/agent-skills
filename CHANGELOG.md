[English](CHANGELOG.en.md) | 中文版

# 變更紀錄

格式參考 [Keep a Changelog](https://keepachangelog.com/zh-TW/1.1.0/)，新的在上面。
本檔只記錄**本 fork 的維護歷史**（2026-09-04 起）；上游
[`addyosmani/agent-skills`](https://github.com/addyosmani/agent-skills) 的產品演進見其自身歷史
與 [`docs/UPSTREAM.md`](docs/UPSTREAM.md) 的審查清冊。逐筆採用／略過的理由記在
[`docs/DECISIONS.md`](docs/DECISIONS.md)。

---

## [Unreleased] - 2026-09-11

### 同步

- **上游批次審查到 `6ca0cd7`（PR #567、issue #565）。** 採用 observability 的 runbook 撰寫小節、context-engineering 的 Context Budget Management 一節（含兩輪 review 修正）、`commands/planning.toml` 與 `.gemini/commands/planning.toml` 補上不完整 plan 不可覆寫的防線，以及 11 個 skill description 補詞與 eval rank-1 門檻 80 → 95。另從未合併的 #563 取回 `scripts/run-evals.js` 遇到 `null` grader expectation 會丟 `TypeError` 的修正，本 fork 有同一缺陷。#564、#566、#567 暫緩到合併，理由見 [`docs/DECISIONS.md`](docs/DECISIONS.md)。

### 變更

- **CodeQL action 重釘 v4.37.9 → v4.38.0**（commit SHA `b96794f`，由 annotated tag `v4.38.0` 解出）。依賴新鮮度檢查對 fork 持有的 `codeql.yml` 報 `REVIEW UPDATE`，下次排程會紅。

### 修復

- **本機自我掃描自掃描器升版起就一直是紅的。** baseline 記的是 `scanner_version: 2.11.0`，PATH 上的 `skillspector` 已是 2.11.2；精確 fingerprint 綁掃描器版本，46 筆因此全部失效，每次 gate 都把 baseline 裡的 finding 報成新的。CI 不安裝掃描器，所以只有本機看得到。以 2.11.2 重產成 26 筆（16 筆 RP1／PE3 已由既有規則涵蓋、4 筆是對到同一 finding 的重複項），理由逐字保留，並在每筆記下所屬 skill。細節見 [`docs/DECISIONS.md`](docs/DECISIONS.md)。

## [Unreleased] - 2026-09-09

### 修復

- **依賴新鮮度的 Actions 查詢改帶 token。** 匿名 `api.github.com` 是每小時 60 次、hosted runner 共用同一個位址額度；超過之後每一列 Action 的 `latest` 都變成 `unknown`，整個 Actions 半邊靜默失聲。`_github_json` 現在在環境有 `GITHUB_TOKEN`／`GH_TOKEN` 時送 `Authorization: Bearer`，workflow 的檢查步驟也補上 `GH_TOKEN: ${{ github.token }}`。沒有 token 仍可運作，只是走匿名額度。（缺陷由 `SanHsien/commerce-agents` 那條線先發現。）


- **依賴新鮮度漏看了每一個 CodeQL pin。** `_USES_RE` 只匹配 `owner/repo@`，而 `github/codeql-action/init`
  是三段路徑，所以 `codeql.yml` 裡的兩個 pin 從來沒進過報告。路徑改為允許子目錄，查 Releases 時再
  截回擁有 tag 的 repo。
- **無法比較的 latest 不再報 OK。** `github/codeql-action` 的 `releases/latest` 回 `codeql-bundle-v2.26.4`，
  與 workflow 釘的 `v4.37.4` 不同編號系統，解析不出數字就一路報 OK。現在解析失敗會改查 tag 列表取最新
  可解析版本；真的比不了就記 `CHECK FAILED`——不會失敗的檢查不是檢查。
- **CodeQL action 重釘 v4.37.4 → v4.37.9**（SHA `cdf488f`），修好檢查後第一次跑就抓到的實際漂移。

兩個缺陷是在 `SanHsien/dashi-ppt-skill` 移植本檔的檢查器時發現的，同源同修。

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
