# 開發環境

維護者與 AI 接手用的開發文件。產品使用方式在 [`README.md`](../README.md)；上游同步在
[`UPSTREAM.md`](UPSTREAM.md)；決策在 [`DECISIONS.md`](DECISIONS.md)。

## 架構

```text
skills/<name>/SKILL.md      產品 skill（英文，以上游為準）
        │
        ├── references/     skill 自帶的細節（部分 skill 才有）
        └── evals/           trigger／routing／behavioral 評測樣本
        │
        ▼
 安裝到 Claude Code / Codex / Cursor 等宿主後才真正可被呼叫

.claude/commands/, commands/, .gemini/commands/   上游 slash command（依宿主分裝）
agents/                     上游 agent persona（code-reviewer、test-engineer 等）
hooks/                      上游 session lifecycle hooks
references/                 根目錄共用 checklist
scripts/                    上游零依賴 Node 驗證器與 eval runner
.claude-plugin/、.codex-plugin/、.agents/、.gemini/、.opencode/   各宿主 plugin manifest
```

`skills/`、`commands/`、`.claude/commands/`、`.gemini/commands/`、`agents/`、`hooks/`、
`references/`、`evals/`、`scripts/`、既有 `docs/` 檔案，以及各宿主 plugin manifest 是要安裝或
跟隨上游的產品。其餘檔案是本 fork 的開發與治理骨架，不要一起複製進 skills 目錄。

## 本機開發（Windows）

```powershell
python -m venv .venv
.venv\Scripts\python -m pip install --upgrade pip
.venv\Scripts\python -m pip install -r requirements-dev.txt
$env:PYTHONUTF8 = "1"
pwsh -NoProfile -File tools\dev_check.ps1
```

先決條件：Python 3.14、Node.js 24、PowerShell 7。

不要對真實 Claude Code / Codex / Cursor 安裝跑完整端對端流程來當 CI。gate 驗的是規格、語法與
維護腳本；plugin 安裝煙霧測試已由上游既有的
[`.github/workflows/test-plugin-install.yml`](../.github/workflows/test-plugin-install.yml)
負責，本 fork 的 `ci.yml` 不重複它。

## Canonical gate

`tools\dev_check.ps1` 會依序：

1. `python -m compileall`（`tests` 與 `tools` 底下維護用的 `.py`）
2. `ruff check`（E9 + F）
3. `pytest tests/ -q`
4. `node scripts/validate-skills.js`
5. `node scripts/validate-commands.js`
6. `python tools/check_links.py`

CI 在 Ubuntu 跑一份等效清單（Python 3.14 + Node 24），並加一個 Windows job 跑同一套本機 gate。
上游既有的 `test-plugin-install.yml`（skill／command 全量驗證、eval、plugin 安裝煙霧測試）維持
不動，`ci.yml` 只補 Windows 可重現性與這個 fork 自己的維護腳本，不重複已經覆蓋的檢查。推 `main`
前先跑本機 gate。

## 工具設定

`pyproject.toml` **只放工具設定**，沒有 `[project]` 與 `[build-system]`：本 repo 交付的是
Markdown Agent Skills 與零依賴 Node 驗證器，不是 Python 套件。改 `ci.yml` 的 ruff 旗標時要同步
改 `pyproject.toml`。`.python-version` 釘 3.14。

`.gitattributes` 把行尾釘成 LF（上游既有設定，本 fork 沿用）。沒有它，全域
`core.autocrlf=true` 會讓工作區變 CRLF，於是 `git status` 顯示檔案 modified 但 `git diff` 是
空的。

## 依賴新鮮度

`tools/check_dependency_freshness.py` 檢查兩處宣告：`requirements-dev.txt` 的
`pytest`／`ruff` 對 PyPI，以及 `.github/workflows/*.yml` 裡每一個釘選 SHA 的 GitHub Action 對
GitHub Releases API。`.github/workflows/dependency-freshness.yml` 每月跑一次。紅燈只有兩條
誠實出口：`# freshness-hold:`（常態政策，寫在宣告那一行）或 `.github/dependency-deferrals.json`
的 `deferredLatest`（會過期）。調高宣告下限來讓報告變綠不是出口。

## 不要做的事

- 不要把產品 `SKILL.md`、command、agent persona 改寫成維護索引。
- 不要翻譯 `skills/`、`commands/`、`agents/`、`references/`、`evals/`。
- 不要提交 `.env`、API key 或客戶專案內容。
- 測試必須是靜態規格檢查，不能打真實第三方服務或 GitHub 寫入 API。
