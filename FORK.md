# Fork 維護說明

本 repo fork 自 [`addyosmani/agent-skills`](https://github.com/addyosmani/agent-skills)，
沿用 MIT License 與完整 Git 歷史。

## 為什麼維護 fork

- 保留原作者持續更新的工程 Agent Skills（spec、planning、TDD、review、ship 等全生命週期）。
- 採 Windows-first 維護：Windows 11 + PowerShell 是主要開發、除錯與完整驗收環境。
- 公開入口改以繁體中文為主，英文鏡像放 `README.en.md`。
- 建立可重現的 Windows 開發 gate、Windows CI job，以及逐筆審查的上游追蹤。
- 產品 Skills／Commands／Agents 仍可直接安裝到 Claude Code、Codex、Cursor 等宿主。

**回貢判準：修的是上游的 bug 就送回去；這裡獨創的文件／Windows 維護骨架留在這裡。**

## 與上游的差異

| 項目 | 說明 |
|---|---|
| `README.md` | 繁中主檔；英文原文在 `README.en.md` |
| `AGENTS.md` / `CLAUDE.md` | 上游內容保留，尾端加一節本 fork 的維護規則 |
| `NOTICE.md` / `FORK.md` | 來源、授權與同步說明 |
| `tools/dev_check.ps1` | Windows 本機一鍵 gate |
| `tools/check_upstream_updates.py` | 上游 commit／PR／issue 三軸未審查追蹤 |
| `tools/check_dependency_freshness.py` | GitHub Actions 釘選版本與 `requirements-dev.txt` 新鮮度檢查 |
| `tools/check_links.py` | 維護文件之間的相對連結檢查 |
| `.github/workflows/ci.yml` | Ubuntu（Python 3.14 + Node 24：ruff／pytest／連結／node 驗證器）+ Windows job 跑 `dev_check.ps1` |
| `.github/workflows/upstream-check.yml` | 每週對 `upstream/main` 做未審查 commit／PR／issue 檢查 |
| `.github/workflows/dependency-freshness.yml` | 每月檢查依賴新鮮度 |
| `docs/DECISIONS.md`、`docs/UPSTREAM.md`、`docs/DEVELOPMENT.md` | fork 維護文件 |

產品 `skills/`、`commands/`、`agents/`、`hooks/`、`references/`、`evals/`、`scripts/`、
既有 `docs/` 檔案、`.claude-plugin/`、`.codex-plugin/`、`.agents/`、`.gemini/`、`.opencode/`
以上游為準，除非有已記錄的 fork 修正。

## 分支與 remote

- `origin/main`：SanHsien 維護線，也是唯一長期分支。
- 嚴格保持「單一最新分支、單一最新 release、單一最新 tag」：本倉庫在 GitHub 與本機只保留唯一最新版本之單一 tag 與 release（目前為 0.6.9），升版時清理舊 tag，不留歷史 tag 堆疊。
- 日常修改直接推 `origin/main`。只有需要他人審查或高風險改動時才開 branch → PR。
- `upstream/main`：Addy Osmani 原始專案，只追蹤、不推送。
- Dependabot 或外部 fork 的變更同樣走 PR，讀 diff 並通過 CI 後再合併。

不要 `git push upstream`。同步方式見 [`docs/UPSTREAM.md`](docs/UPSTREAM.md)。

上游更新英文 `README.md` 時，把新產品說明翻進本 fork 的繁中 `README.md`，並同步
`README.en.md`。

## 換一台電腦怎麼開發

```powershell
git clone https://github.com/SanHsien/agent-skills.git
cd agent-skills
python -m venv .venv
.venv\Scripts\python -m pip install --upgrade pip
.venv\Scripts\python -m pip install -r requirements-dev.txt
pwsh -NoProfile -File tools\dev_check.ps1
```

只想安裝 Skills、不開發時，見 [`README.md`](README.md) 的安裝章節。
