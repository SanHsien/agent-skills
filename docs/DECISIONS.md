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

## 2026-09-06：審完 13 個 upstream commits 與 PR #548–#560

**採用**：`dc469a9`、`f0550d8`、`cca4df5` 的 release-gate SLO 說明；`6a9f2eb` 的單一 log
entry point；`45fd4a0` 的 destructive path allowlist／depth／owner 防線；`878d5d4` 的 session
handoff；`f7fe1a4` 的 Copilot CLI 與 VS Code 分流。產品檔以 cherry-pick 保留上游作者與提交，
`README.md` 只解安裝入口衝突，英文增量同步到 `README.en.md`。

**略過**：`8c8cfd1`、`85ea8fb`、`4d10bcb`、`858c1ae`、`469d00f` 是上述內容的 merge
commit，沒有額外產品 diff；`84ee506` 的 0.6.9 manifest bump 依賴上游 tag ancestry，單獨
cherry-pick 會讓 `scripts/validate-versions.js` 仍以 fork 可達的 0.6.8 tag 判定並失敗，因此等
下一次可保留 tag topology 的 release 同步。

**PR 水位**：#549、#550 已由上述 commit 採用；#548 與 #551–#560 仍 open，已讀 diff 後
記為等待。#548 是 13 檔、1252 行的 catalog generator；#551 是跨 19 檔的 `/review` →
`/code-review` 相容性改名；#552–#560 分別涵蓋穩定 skill 名稱、既有專案安裝、外部 spec
artifact、社群影片、互動教學、native router、agent-first CLI、restartable boundary 與 host
adapter 表。這些都跟隨上游定稿，不在 open 狀態先做 fork-only 搬運。

## 2026-09-11：審完 11 個 upstream commits、PR #561–#567、issue #565

**採用**（cherry-pick，全部乾淨套用，保留原作者）：

- `cd33117`／`8714f2b`：observability-and-instrumentation 的 Runbook 撰寫小節（三問格式、最小
  範本、何時擴充、保持更新的紀律），第二筆是 federicobartoli review 後的收斂（nest 成 `####`、
  指回 rule 2、SQL 加防呆、平台措辭鬆綁）。
- `a1c8fa9`／`cf0ba3f`／`cc48b69`：context-engineering 新增「Context Budget Management」一節
  （75% 門檻、優先捨棄表、保護清單、先壓縮再捨棄、recency 排序），後兩筆分別是 nucliweb 與
  federicobartoli review 後的修正（合併重複 red flag、把 Level 5 接到新小節、把「transformer
  attention 偏好近期 token」的錯誤機制敘述換成有引註的 lost-in-the-middle U 型效應）。
- `78970d5`：把既有的「不完整 plan 不可靜默覆寫」防線（fork 已在 `.claude/commands/plan.md`
  有，來自本線先前採用的 `#518`）鏡像進 `commands/planning.toml` 與 `.gemini/commands/planning.toml`
  ——這兩檔在 fork 裡原本沒有這道防線，純粹補齊，無衝突。
- `cda4542`：11 個 skill description 補上使用者實際會說的詞彙（debugging 的「昨天還能動」、
  documentation-and-adrs 的「記錄一個架構決策」等），CI 的 `--min-rank1` 門檻從 80 提到 95
  （trigger rank-1 從 86% 升到 100%），`evals/README.md` 與上游自有的
  `.github/workflows/test-plugin-install.yml` 同步調整；fork 對這個 workflow 檔沒有疊加層差異，
  乾淨套用。
- PR **#563**（`fix(evals): reject null grader expectations without crashing`，commit
  `e6a58d5`）：`scripts/run-evals.js` 的 `parseGrading` 在 grader 回傳的 `expectations` 陣列含
  `null` 元素時會直接丟 `TypeError`（`expectation.passed`／`expectation.text` 存取 null 的屬性），
  fork 上這個缺陷原樣存在（`scripts/run-evals.js:442` 與 `:448`），符合「未合併 PR 但修的是 fork
  demonstrably 有的缺陷」，予以 cherry-pick；帶回歸測試（全 null 與混合 null 的 expectations
  陣列）。

**略過**（沒有額外 diff的 merge commit）：`48cb116`（#447 merge）、`38e2a4a`（#434 merge）、
`fe6f081`（#422 merge）、`6ca0cd7`（#531 merge）——四筆的 child commit 已個別 cherry-pick，
merge 本身在 `--stat` 對照下沒有額外內容。

**擱置**（open PR，未合併，且不是 fork 現有缺陷）：

- **#561**（`test merge upstream`，已 CLOSED）／**#562**（`Temp/plugin bump`，已 CLOSED）：
  兩筆都是提交者個人開發機的殘留分支（`.serena/`、`debug/`、`docs/INITIATIVES/`、
  未發布的 `plugins/audit-suite`、`plugins/foreman-line` 等與本 repo 主題無關的內容），且都已
  關閉未合併，不動。
- **#564**（`Align skill workflows with GPT-6 Astra guidance [just FYI]`）：作者本文明講
  「Not looking for approvals or get merged this, just your comments」，是徵詢意見用的展示
  PR，不是要合併的修正；且大幅改寫 22 個 SKILL.md（多筆刪減兩三成內容），跟隨上游是否定稿，
  不先行搬運。
- **#566**（`feat: add task-ledger skill`）：新增一整個 `skills/task-ledger/` skill（含
  README／CLAUDE.md 目錄表、evals fixture）。這是全新功能而非修 fork 現有缺陷，等上游合併或
  head 改變後再評估是否要跟進。
- **#567**（`docs: compatibility guidance for downstream renames of browser-testing-with-devtools`，
  closes upstream #541）：在 `skills/browser-testing-with-devtools/SKILL.md` 加一段「下游改名
  要留相容別名或遷移規則」的說明，是給下游 fork／catalog 的預防性指引，fork 本身沒有把這個 skill
  改名，不是本 fork 現有的缺陷，等上游合併定稿。

**issue**：#565 是感謝信（作者的 AI-SDLC Template 引用了本專案並附 credit），無需動作，僅推進
水位。

**baseline**：commit 推進到 `6ca0cd7`（upstream `main` HEAD）；PR 水位到 **#567**；issue 水位到
**#565**。

## 2026-09-12：SkillSpector baseline 重產到 2.11.2，並在每筆記下所屬 skill

**問題**：`.skillspector-baseline.yaml` 的 `scanner_version` 還是 `2.11.0`，PATH 上的
`skillspector` 已是 `2.11.2`。精確 fingerprint 由 `suppression.finding_fingerprint` 同時雜湊
掃描器版本、元件內容與 finding，所以升版讓 46 筆全部失效——本機 `tools/dev_check.ps1` 的自我掃描
把每一筆 baseline 裡的 finding 都報成新的，這道關卡自升版起就一直是紅的。CI 不安裝掃描器
（`ci.yml` 只裝 `requirements-dev.txt`），自我掃描在 CI 走「skipped: not found on PATH」，
所以紅燈只出現在本機，沒有人看見。

**決定**：以 2.11.2 重產，46 筆 → 26 筆，理由逐字保留，並在每筆加上 `skill:` 欄位。

**逐項理由**：

- **16 筆 RP1／PE3 fingerprint 移除**：本檔頂部的兩條 id-only `rules` 已涵蓋這兩類。實際重掃
  25 個 skill，RP1／PE3 的 finding 全部落在 rule 抑制側（`ci-cd-and-automation` 5 筆、
  `security-and-hardening` 2 筆等，共 16 筆），沒有任何一筆需要 fingerprint。留著等於替 rule
  影子重算雜湊，移除不放寬任何東西：規則本身沒動。
- **4 筆重複項移除**：`AR2`（shipping-and-launch）、`EA2`（security-and-hardening）、
  `SSRF1`（security-and-hardening）、`YR4`（security-and-hardening）各有兩筆對到同一個 finding
  ——一筆是分類式理由、一筆是後來補的逐行理由。2.11.2 對這些位置各只產生一個 finding，多出來的
  那筆永遠對不到任何雜湊。保留內容較穩定的分類式理由（逐行理由寫死行號，內容一動就過期）。
- **26 筆換新雜湊**：一對一對應，rule_id 與 skill 都相同，沒有任何一組數量增加，也就沒有需要
  重新審查的新 finding。
- **新增 `skill:` 欄位**：每個 skill 各自掃描，`file` 永遠是 `SKILL.md`，只靠 `(rule_id, file)`
  無法分辨是哪個 skill——通用重產工具就是因此中止的。掃描器忽略未知欄位（`baseline_from_dict`
  只讀 `hash`／`reason`），所以這個欄位純粹是給維護者與工具用的。

**驗證**：`pwsh -NoProfile -File tools\dev_check.ps1` 全綠，自我掃描 25 個 skill 無新 finding。

**觸發條件**：下次掃描器升版時重跑同一流程；若某一組 finding 數量增加，那是真的新 finding，
要逐筆審查後才准加 fingerprint。

## 2026-09-12：審完 17 個 upstream commits、PR #552–#560 合併、同步 0.6.9 release 與 tag

**採用**：
- `674921c`（PR #552）：`docs/skill-anatomy.md` 澄清 `browser-testing-with-devtools` 為上游穩定名稱，下游 catalog 若改名須自行維護別名與映射。
- `4fd76c6`（PR #553）：`docs/getting-started.md` 補充既有專案導入無需遷移架構或複製本倉庫根目錄之 `AGENTS.md`／`CLAUDE.md`。
- `15af65e`（PR #554）：`skills/spec-driven-development/SKILL.md` 澄清外部規格工具（如 OpenSpec）格式無關，產物格式由外部工具擁有，本技能負責內容、釐清與核准關卡。
- `5b98a0b`（PR #556）：`docs/getting-started.md` 增加可執行的互動式教學連結（`https://skills.addy.ie/tutorials/`）。
- `a71eb51`（PR #557）：`docs/adoption-guide.md`、`docs/codex-setup.md`、`docs/getting-started.md` 補充在已具備原生技能路由的宿主（如 Codex、Claude Code）上，安裝個別技能即可，不要再將 `using-agent-skills` 貼入常駐 context 造成雙重路由。
- `a1c9bd6`（PR #559）：`skills/context-engineering/SKILL.md` 增補「Restartable Session Boundaries」一節，明確規範切換新 session 前應持久化的五項狀態，並在 `docs/getting-started.md` 加入 Ralph loops 邊界與外部 harness 職責說明。
- `17d8e52`（PR #560）：`README.md`（繁中）、`README.en.md`（英文）、`docs/antigravity-setup.md`、`docs/gemini-cli-setup.md`、`docs/getting-started.md` 加入核心流程與宿主適配器分層架構表，並將指令計數調整為 9 個（納入 `/constraints`）。

**略過**：
- `e6a58d5`（PR #563）：修復 `scripts/run-evals.js` null expectation 崩潰，本 fork 已在 2026-09-11 提早 cherry-pick 為 `b70ccd8`，diff 完全一致，無需重複動作。
- `226bdd3`、`20e8699`、`a9d4b46`、`57c0196`、`bc97fd4`、`17cbf4b`、`4e94bb5`、`fd00a70`、`be4e44a`：九筆 merge commit，在 `--stat` 對照下無額外 diff。

**發布與版本（0.6.9）**：
- 上游於 2026-09-05 發布 0.6.9（commit `84ee506`，tag `0.6.9`）。先前本 fork 因 tag ancestry 暫緩 manifest bump；現藉由完整引進 0.6.9 實質內容，將 5 份 plugin manifest 升版至 `0.6.9`，在最新 commit 建立 tag `0.6.9`，使 `validate-versions.js`（`git describe --tags --abbrev=0`）順利驗證通過。
- 同步推送至 `origin/main` 及 tag `0.6.9`，並在 `SanHsien/agent-skills` 建立 GitHub Release 0.6.9。嚴格只發在 fork 本身，絕不觸碰 upstream。

**baseline**：commit baseline 推進至 `be4e44a9fbc5e8df0beaefadbb28bd22ee61cc39`；PR 水位維持 **#567**；issue 水位維持 **#565**。

## 2026-09-12：嚴格落實單一最新分支、Release 與 Tag 政策

**背景與糾正**：
在推送 0.6.9 升版後，GitHub `SanHsien/agent-skills` 上仍殘留先前的 `0.6.8` tag。維護者糾正要求「單一最新」指的不僅是單一分支，也涵蓋單一最新 release 與單一最新 tag。先前誤以為「單一」僅修飾「分支」而依常規保留歷史 tag，導致遠端出現多個 tag。

**決定與動作**：
1. 刪除遠端 `origin` 上的舊 tag `0.6.8`（`git push origin --delete 0.6.8`），並刪除本機所有舊 tag，使 GitHub 與本地皆只存在唯一最新 tag `0.6.9`。
2. 將「單一最新分支、單一最新 release、單一最新 tag」明文寫入 `CLAUDE.md` 與 `FORK.md`，未來任何版本升級均需清理舊 tag，保持絕對乾淨的單一最新狀態。
