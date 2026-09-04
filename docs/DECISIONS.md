# 維護決策

## 2026-09-04：建立 Windows-first 維護型 fork

**決定**：fork `addyosmani/agent-skills`，保留 MIT 與完整歷史，預設分支維持 `main` 以降低與
上游同步摩擦。本線聚焦繁中公開入口、Windows 開發 gate、Windows CI，以及逐筆審查的上游追蹤。

**理由**：上游已有 25 個可安裝的工程 Agent Skills、9 個 slash command 與 4 個 agent persona，
覆蓋 spec 到 ship 的完整生命週期，符合維護者用 Claude Code／Codex／Cursor 落地工程紀律的需求。
缺的是 Windows 11 上可重現的開發／驗收骨架，以及繁中入口。授權是 MIT，fork 修改同樣走 MIT。

**限制**：

- 不把 fork 包裝成原創專案，不移除原作者與 MIT 標示。
- `skills/*/SKILL.md`、`commands/`、`agents/`、`hooks/`、`references/`、`evals/`、`scripts/`
  保持產品規格，不用維護索引覆寫。
- 不把產品 skill／command 翻譯成繁體；產品語言跟隨上游。
- 上游更新必須逐筆審查（commit／PR／issue 三軸都要看，見 `docs/UPSTREAM.md`）。
- 不回貢，除非維護者在當次對話明確同意。

## 2026-09-04：維護線直接推 main

**決定**：fork 維護不開功能分支。改完在本機跑 gate，通過後直接推 `origin/main`。遠端只留
`main`；`upstream/main` 只追蹤。

**理由**：這是單人維護 fork，分支與 PR 沒有第二審查者，只增加同步成本。

**限制**：

- Dependabot 與外部 fork 仍可能開 PR，讀 diff 後再合併，不自動合併。
- 不推 `upstream`，不 force-push `main`。
- 不刪 `upstream` remote。

## 2026-09-04：不啟用 Dependabot 自動合併

**決定**：Dependabot 只開 PR；CI 與人工讀 diff 通過後才合併。

**理由**：本 repo 只有 `github-actions` 生態系一個 Dependabot 來源（無 `package.json`、無
Python 套件依賴），體積小，但自動合併仍會跳過「讀 diff」這一步。

## 2026-09-04：依賴新鮮度檢查涵蓋 GitHub Actions 與 Python dev 依賴

**決定**：`tools/check_dependency_freshness.py` 同時檢查兩個來源——
`requirements-dev.txt` 的 `pytest`／`ruff` 對 PyPI，以及 `.github/workflows/*.yml` 裡每一個
`uses: owner/repo@<sha> # vX.Y.Z` 對 GitHub Releases API。

**理由**：本 repo 沒有 `package.json`，Node 驗證器（`scripts/*.js`）零依賴，所以「依賴」實際
存在的地方是兩處：dev 工具與 CI 裡釘選 SHA 的 Actions。只查其中一處會讓另一處的漂移永遠不會
被任何自動化看到——這正是 `marketingskills` fork（本 fork 的維護骨架範本）只查 PyPI 而漏掉
Actions 版本漂移的落差，這裡一開始就補上。

**限制**：不查 Actions 執行時安裝的間接依賴（例如 `actions/setup-node` 內部拉的 Node 版本）；
只查工作流程檔裡明文釘選的 Action 本身。

## 2026-09-04：pytest 下限升到 9.1；上游工作流程的 Action 版本改記 deferral

**決定**：

- `requirements-dev.txt` 的 `pytest` 下限由 `>=8.3.0` 提到 `>=9.1`。
- `.github/dependency-deferrals.json` 為 `actions/checkout`（reviewed at 7.0.1）與
  `actions/setup-node`（reviewed at 7.0.0）各記一筆 deferral。

**理由**：

- pytest：本 repo 的 CI 只跑 Python 3.14 一個版本，沒有 3.9 相容性包袱（那是範本 repo
  `marketingskills` 的限制，不是這裡的）。本機以 pytest 9.1.1 實跑 `python -m pytest -q`
  28 項全過，下限跟著實際支援範圍走，不是為了消音。
- Actions：`v6` 只出現在上游自有的 `.github/workflows/test-plugin-install.yml`。那是產品內容，
  本 fork 的疊加層不改上游檔案，重新釘選是上游的決定。deferral 帶 `deferredLatest`，等上游
  釋出下一個 major 就自己過期並重新提問，不會變成永久靜音。

**限制**：deferral 以套件名為鍵，不分檔案——本線自有工作流程若哪天落後到同一個版本，也會被
同一筆 deferral 蓋住。要避免就是照既有做法：自有工作流程一律釘 SHA 並在同行註記 `# vX.Y.Z`。

## 2026-09-04：公開文件只留繁中與英文；README 只留 credit

**決定**：GitHub About 與公開入口只用繁體中文與英文。README 不轉載作者個人頁、機構、課程、
贊助 CTA 或官網行銷。來源與授權 credit 留在 README 短段與 `NOTICE.md`。

**理由**：這是維護型 fork，不是原作者的宣傳頁。相關 credit 放 README 短段與 `NOTICE.md` 即可
滿足 MIT 標示。

**限制**：上游若把宣傳段落一併推進來，merge 後刪掉／不要合進公開入口。技能／指令目錄表與安裝
方式可同步。
