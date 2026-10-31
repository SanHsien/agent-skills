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

## 2026-09-17：審完 17 個 upstream commits、PR #568–#578、issue #569／#572

commit 水位 `6ca0cd7` → `be4e44a`；PR 水位 567 → 578；issue 水位 565 → 572。

**採用（cherry-pick，保留原作者）**：`674921c`（穩定的 browser skill 名稱）、`4fd76c6`（既有專案
不需遷移）、`5b98a0b`（可執行的 workflow 教學連結）、`a71eb51`（原生會路由 skill 的 host 不要再疊
一層 `using-agent-skills`）、`15af65e`（spec 的外部產物歸屬）。

**採用（最小重做）**：
- `a1c9bd6`（Restartable Session Boundaries）：本 fork 的 `context-engineering/SKILL.md` 已帶
  2026-09-11 採用的 Context Budget Management，插入點前後文不同而衝突；段落文字逐字取用，只換位置。
- `17d8e52`（shared core → native adapters）：上游改的是英文 `README.md`，本 fork 的 `README.md`
  是繁中入口，所以結構表落在英文鏡像 `README.en.md`；繁中 README 沒有專案結構段，無需同步。
  `docs/` 三份的命令數 8 → 9 與 `/constraints` 列照收——本 fork 在 `commands/`、`.gemini/commands/`、
  `.claude/commands/` 各有 9 個 wrapper，舊的「8」在這裡也是錯的。

**已涵蓋**：`e6a58d5`（#563）已於 2026-09-11 cherry-pick。8 個 merge commit 沒有額外 diff。
**驗證**：本批上游改動過的每個檔案，除了繁中 `README.md` 外，現在都與 `upstream/main` 逐位元組相同。

**採用未合併 PR #573**（reference-link 驗證器在 Windows 輸出反斜線）：本 fork 在 Windows 實測
`node --test scripts/validate-reference-links-test.js` 為 7 個測試 1 個失敗——驗證器用
`path.relative` 印出 `skills\using-agent-skills\references\…`，測試比對的是 `/`。這是本 fork 可重現的
缺陷，符合採用未合併 PR 的門檻。#573 的淨變更只有一行，把輸出路徑統一成 `/`；套用後 7/7 通過。
issue #572 是同一問題，已由此解決。#575 已被上游關閉（同一修法的另一版本）。

**延後至合併**：
- #570（README 標題寫「All 24 Skills」，實際列 25 個）：本 fork 的 `README.en.md` 也有這個錯字，但它
  同時改 `docs/adoption-guide.md` 的錨點；單獨採用會讓該檔與上游分岔，外觀問題不值得。上游合併後隨
  commit 軸進來。
- #574 與 issue #569（Claude Code plugin 在每次 SessionStart 注入 `using-agent-skills`，與剛採用的
  `a71eb51`「不要雙重路由」互相矛盾）：矛盾是真的，但修法是改變 plugin 的 hook 行為，屬產品決策；
  上游文件與 hook 目前也是同樣的矛盾狀態，本 fork 跟著上游定案。
- #568、#571、#577（skill linter 的新規則與 CI）、#576（grader 依 id 綁定期望）、#578（simplify-ignore
  hook 還原）：都是未合併的新功能或本 fork 未重現的缺陷——本機 `validate-skills.js` 通過。

**fingerprint**：`context-engineering` 與 `spec-driven-development` 的 SKILL.md 內容改變，依
`(skill, rule_id)` 對應重算雜湊；見提交紀錄。

## 2026-09-17：SkillSpector 同步到 `82bbe8b` 後的 gate 調整

**背景**：本機的 `skillspector`（uv tool）是 editable 安裝、指向 SkillSpector fork 的 checkout，所以 fork
同步上游 53 個 commit（`82bbe8b`，版本號仍 2.11.2）後，這個 repo 的自我掃描立刻換成新版掃描器。

**變數改名**：`tools/dev_check.ps1` 原本設 `SKILLSPECTOR_MAX_STATIC_SECONDS=86400`，那是 SkillSpector fork
自己的變數，同步時已由上游 #522 的 `SKILLSPECTOR_MAX_STATIC_ANALYSIS_SECONDS_PER_ARTIFACT` 取代。
改用新名稱；舊名稱在新版會被忽略，每檔預算就會退回 300 秒。

**fingerprint**：新版改了 finding 的識別內容，4 筆既有項目雜湊漂移（`browser-testing-with-devtools` P1、
`doubt-driven-development` EA5、`shipping-and-launch` AR2、`source-driven-development` P1），同 skill、同規則、
同行、同證據，理由不變只換雜湊。

**新增 2 筆 AE1（逐筆審查後接受）**：新版 `static_patterns_tool_misuse` 在
`constraint-driven-development/references/floor-guard.md` 碰到有界解析器的跨度上限（ledger 記
`static_parse_limit`），`SKILL.md` 第 216、258 行引用該檔時各回報一筆 AE1「referenced artifact not
completely inspected」。收進 baseline 等於接受這塊沒被這個 analyzer 完整檢查，所以先人工逐行審閱該檔：
一段 JS 參考實作，只以 `execFileSync` 的 argv 陣列呼叫 `git`（不經 shell），參數是固定字面值、`--base`
參數與 `git ls-files` 輸出；沒有網路、寫檔或讀環境變數，輸出截斷到 120 字元。沒被完整覆蓋的是第 57、59 行
兩條很長的正規表示式，內容無害。兩筆共用同一段審查理由。

**工具教訓**：`skillspector baseline` 與掃描圖的 `filtered_findings` 都只給出第 216 行那筆的雜湊，第 258 行
那筆只出現在未過濾的 `findings` 清單，而 CLI 報告兩筆都列。這正是本檔頭已記載的「近似行會少列指紋」問題；
補雜湊時要從未過濾清單算。

**驗證**：`pwsh -NoProfile -File tools\dev_check.ps1` WINDOWS DEV CHECK GREEN，25 個 skill 無新 finding。

## 2026-09-17：修復 squash 後缺乏可達 release tag 與 manifest 版本漂移問題

**問題**：
1. 本倉庫先前執行歷史 squash 初始化單一 root commit（`58e0269`）時，既有的歷史 release tag（`0.6.9`）未接續至新歷史上，GitHub Actions 的 `Test Plugin Installation / Validate skill content`（`scripts/validate-versions.js`）執行 `git describe --tags --abbrev=0` 時因無任何可達 tag 而拋出 `fatal: No tags can describe ...` 導致 CI 失敗。
2. 同時 5 份 plugin manifest 在 squash 初始化時漂移回退為 `0.6.8`，而上游及本 fork 正式 release 均為 `0.6.9`。
3. `CLAUDE.md` 與 `FORK.md` 遺失先前制訂之「單一最新分支、單一最新 release、單一最新 tag」政策條款。

**決定與動作**：
1. 將 5 份 plugin manifest（`plugin.json`、`.codex-plugin/plugin.json`、`.claude-plugin/plugin.json`、`.claude-plugin/marketplace.json`、`.agents/plugins/marketplace.json`）版本全面同步至 `0.6.9`。
2. 補回 `CLAUDE.md` 與 `FORK.md` 之單一最新分支、Release 與 Tag 條款。
3. 清理本機所有歷史 tag，在 `main` 最新提交重新建立 annotated tag `0.6.9`，並強制推送至 `origin`，使 `git describe --tags --abbrev=0` 正確返回 `0.6.9`。
4. 驗證本機 `dev_check.ps1` 與 manifest version validator 全數通過。

## 2026-09-30：同步上游 0.6.11 範圍，security-and-hardening 拆分與版本升號延後

產品路徑以上游為準（見 `docs/UPSTREAM.md` 2026-09-30 段）。兩項刻意不採：(1) #579／#589——SkillSpector 自掃描會新增 16 筆需人工核可的 baseline 條目，等維護者核可；(2) 0.6.10／0.6.11 版本號——單一 tag 政策下升版需刪舊 tag，等維護者授權。Baseline 表示已審查，不表示已全數合併。

## 2026-10-24：上游批次同步到 `aeac41d`（0.6.13；PR #718、issue #717）

**決定**：112 個 commit 的範圍只動到 61 個檔案，逐檔比對後發現本 fork 自己持有的只有 5 份 plugin manifest（差別僅版本號）與繁中 `README.md`。其餘 55 個檔案（含 9 個上游新增檔）直接取上游版本；5 份 manifest 的內容也取上游，但依 2026-09-30 的既有決策，版本號維持 0.6.9。

**理由**：本 fork 的定位是「產品內容以上游為準、維護骨架自持」。這批上游改動集中在 `skills/`、`scripts/`、`evals/`、`hooks/`、`docs/` 與 `.claude/commands/`，全部屬於產品側；逐 commit 重做只會製造分岔。比對確認本 fork 沒有在這 60 個檔案上疊過任何修改，所以 fast-forward 到上游是零資訊損失的做法。

**README 兩份的處理**：`README.en.md` 是上游英文 README 的逐字鏡像，以上游現行版重建並保留頂部語言列。繁中 `README.md` 補譯上游本批的三處改動——Claude Code 裡這些是 plugin command、與內建同名時要用 `/agent-skills:review`；`.cursor/skills/` 與 `.cursor/rules/` 都在使用者自己的專案裡，本 repo 不附 `.cursor/` 資料夾；能安裝但未列出的宿主見 `docs/other-hosts.md`。上游第四處（在格式規格段落補 `docs/advanced-per-agent-configuration.md` 連結）對應的段落繁中版本來就沒有，不為此新增。

**PR 與 issue 軸**：#622–#718 共 86 筆。28 筆已合併，隨本次 commit 同步進來；14 筆 closed 未合併，不處理；其餘 open 的依慣例等合併。issue 軸 #573–#717 沒有一筆需要本 fork 單獨處置，全部對應到 open PR 或已 closed。

**自我掃描**：上游新文件讓五個 skill 冒出 8 筆 finding，逐筆讀過命中的原文後確認全是自我指涉誤判，以具體理由收錄，沒有為了過掃描改上游內容：

- `api-and-interface-design` 的 TM1 命中 REST 範例表的 `DELETE /api/tasks/:id`，那是路由設計教學表格。
- `security-and-hardening` 的 SSRF1 命中 SSRF 防禦範例在說明 `169.254.169.254` 是頭號攻擊目標；這筆本來就已收錄，是上游在同段補了 TOCTOU 說明才換雜湊。
- `shipping-and-launch` 的 AR2 命中上線前檢查清單。
- `spec-driven-development` 的 EA2 命中三層邊界表的「Never do」那一列；三筆 AS3 命中同一行對本 repo 另外三個 skill 的路徑引用。
- `test-driven-development` 的 EA2 命中 Red Flags 裡「宣稱全部測試通過、但其實沒跑過測試」。

**release bump 不採用**：`a06bc63`（0.6.12）、`aeac41d`（0.6.13）。本 fork 只保留單一 tag／release（現為 0.6.9），升版需要刪舊 tag 與 release，屬維護者授權動作，與 2026-09-30 對 0.6.10／0.6.11 的處理相同。上游已把 tag 檢查從 `scripts/validate-versions.js` 移除，五份 manifest 版本一致即通過。

## 2026-10-24：自我掃描跟上 SkillSpector 2.12.0

**決定**：本機 gate 改用 PATH 上的 SkillSpector 2.12.0（`uv tool install --editable C:\GitHub\SkillSpector`，對應 SanHsien/SkillSpector `350e638`），指紋逐筆搬移，報告改由 stdout 導向寫檔。

**理由與做法**：

- **報告寫檔**：2.12.0 在沒有 `O_NOFOLLOW`／`dir_fd` 的平台（Windows）拒絕 `--output`，要求改用 stdout 導向，這是上游防止輸出路徑被換成 symlink 的安全設計。`tools/dev_check.ps1` 改成 `skillspector scan … > 報告檔`；PowerShell 7.4 起原生指令導向會原樣保留位元組，UTF-8 JSON 不會被主控台編碼轉壞，gate 會先檢查版本。報告寫在 `.skillspector-reports/`，不在被掃描的 skill 裡。
- **指紋搬移**：指紋綁掃描器版本。對 2.12.0 回報的每個 finding 分別以 2.11.2 與 2.12.0 計算，舊雜湊對上已審條目的原地換新、保留理由（27 筆）。`constraint-driven-development` 那兩筆 `floor-guard.md` 連帶的 AE1 因規則識別方式改變而重新計算；`floor-guard.md` 今天隨上游 `aa68c3e` 改過，重讀後判斷不變。不再產生的 7 筆過期條目刪除。

**驗證**：`tools/dev_check.ps1` 綠燈，25 個 skill 無新 finding。

## 2026-10-24：修正 CodeQL alert #1（`js/incomplete-multi-character-sanitization`）

**決定**：`scripts/validate-reference-links.js` 的 `slugify()` 原本用單次 `.replace(/<[^>]+>/g, '')` 剝掉標題裡的 inline HTML，CodeQL 判定輸出仍可能含 `<script`。抽出 `stripInlineHtml()`：重複剝除標籤直到字串不再變化，再移除殘留的 `<`、`>`。只在單次 replace 後補 `[<>]` 過濾，CodeQL 仍會標同一行，所以兩者都做。另加 `require.main === module` 守門並匯出 `slugify`、`stripInlineHtml`，讓測試能直接呼叫。

**暴露面**：輸出只用來和連結的 `#fragment` 比對 heading anchor，不寫進 HTML，也不輸出給瀏覽器。單次剝除會殘留的只有未閉合的 `<`（例如 `a <script`）；`slugify()` 最後的字元過濾本來就會丟掉 `<`、`>`，所以 slug 對任何輸入都不變。實測 repo 內 1408 個 heading 的 slug，修正前後逐行一致。

**例外說明**：`scripts/` 依 fork 規則以上游為準；這是 security alert 修正，範圍限一個函式，上游同步時若上游改了同一段，以上游版為準再確認 alert 是否仍成立。

## 2026-10-25：審完上游 PR #719–#731，reviewed_pr_through 推到 #731

**決定**：13 筆 PR 全部讀完整 diff，全是 open 未合併，不採用、等上游合併後隨 commit 軸同步。`reviewed_pr_through` 718 → 731；commit 軸無新增（`aeac41d`），issue 軸無新增（#717）。

**證據**：本 fork 的產品檔與上游逐位元組相同，所以這些缺陷在本線同樣存在，下次同步時會自然被修掉。實測：

- #719 `references/accessibility-checklist.md` 仍有 2 處 `htmlFor`（HTML 範例應為 `for`）；#720 仍寫 `npx axe-core`（第 127 行）；#725 兩處 `aria-busy` 缺 `role="status"`。
- #721 `skills/performance-optimization/SKILL.md:209` 仍是 `npx lhci autorun`；#727 `references/performance-checklist.md:195` 仍是 `https://localhost:3000`。
- #722 `lighthouse_audit --output-format` 在 commands／agents 仍有 7 處未帶頁面 id；#723 `docs/cursor-setup.md` 仍有 `docs.cursor.com` 連結。
- #724 `skills/idea-refine/SKILL.md:32` 仍是 `bash skills/idea-refine/scripts/idea-refine.sh`；#729 `constraint-driven-development` 仍有 3 處 `gitleaks detect`（issue #717 的同源問題）；#731 `git-workflow-and-versioning` 第 153–154 行 worktree 範例仍缺 `-b`；#728 引文第 161 行仍是舊句；#726、#730 的範例片段仍是舊版。

**不採用的理由**：不單獨摘取未合併 PR（它們可能在審查中改寫，已摘取的會與日後合併版本分岔），與 2026-09-17、2026-10-24 的處理一致。

**觸發條件**：任一筆合併時，下次 commit 軸同步自動帶入；若 #729／#717 長期不動，再評估是否因 secret 值外洩到 agent 日誌而提前採用。

## 2026-10-25：依賴新鮮度紅燈的處理

- GitHub Actions 重新釘 SHA（本線自有 workflow）：`actions/setup-node` 7.0.0 → 7.1.0、`actions/setup-python` 7.0.0 → 7.1.0、`github/codeql-action` 4.38.2 → 4.39.1。讀過發版說明，都是功能與依賴更新，沒有破壞性變更。
- `actions/setup-node` 的 deferral 更新到 7.1.0：v6 仍只出現在上游自有的 `test-plugin-install.yml`。
- `ruff>=0.16` 加 `# freshness-hold`：下限是相容承諾，不是追新。以 ruff 0.17.2 實測 `ruff check --select E9,F` 與 pytest 32 項全過；沒有提高下限來消紅燈。

## 2026-10-25：補審上游 PR #732，reviewed_pr_through 推到 #732；dev_check 補上 CI 專有的 Node 檢查

**上游 #732**（open 未合併，只動 `skills/frontend-ui-engineering/SKILL.md`）：加 5 步 Workflow、Interactive Widget Contracts 表（menu button、dialog、tabs、disclosure、listbox/combobox 的 role／ARIA／鍵盤行為）、Verification 改成「用專案既有工具驗證、不為了驗證另裝工具」。本 fork 該檔與上游逐位元組相同，所以這是新增內容而非本線缺陷。依既有慣例不單獨摘取未合併 PR；觸發條件同上：合併時隨 commit 軸帶入。commit 軸仍是 `aeac41d`，issue 軸仍是 #717。

**dev_check 補檢查**：`tools/dev_check.ps1` 原本只跑 validate-skills／validate-commands，CI（`test-plugin-install.yml`）多跑的 `validate-versions`、`validate-reference-links`、`validate-artifact-paths`、`run-evals --min-rank1 95` 與 7 個 `node --test` 檔，本機推送前看不到。補進去，讓本機綠燈等於 CI 的 Node 部分綠燈。`hooks/*-test.sh` 是 bash 腳本，仍只在 CI 跑。


## 2026-10-25：補審上游 PR #733，reviewed_pr_through 推到 #733

#733（open 未合併）：修 WCAG 對比門檻與 resize 穩定檢查，動 `evals/cases/` 兩個 case、新增兩個 eval fixture（`contrast.html`、`resize.html`）、`references/accessibility-checklist.md`、`skills/browser-testing-with-devtools/SKILL.md`。本 fork 這兩份產品檔與上游逐位元組相同，所以是新增內容。新增 eval case 屬上游測試資產，未合併前不單獨摘取；觸發條件：合併時隨 commit 軸帶入。commit 軸仍是 `aeac41d`，issue 軸仍是 #717。

## 2026-10-26：補審上游 PR #734–#744，reviewed_pr_through 推到 #744

11 筆全為 open 未合併，逐筆取 head 讀完 diff，並掃過隱藏內容（`eval`／`new Function`／`global.`／base64／長空白後接程式／超長單行），無命中。內容：#734、#742–#744 動 `scripts/run-evals.js`（stemmer 縮寫比對、單案例選取、不完整 executor 串流拒絕、skill 資源暫存位置）；#735 `hooks/SDD-CACHE.md` 措辭；#736–#741 為 skill 文件加固與對應 eval case／fixture。

**決定**：不單獨摘取，等上游合併後隨 commit 軸同步（與 2026-10-25 慣例一致：未合併 PR 可能在審查中改寫）。commit 軸仍是 `aeac41d`、issue 軸仍是 #717，無新增。

**觸發條件**：任一筆合併時，下次 commit 軸同步自動帶入。

補充：#742–#744 另動 `evals/README.md`；#743 新增 `scripts/lib/execution-status.js`、#744 新增 `scripts/lib/skill-resources.js`。

## 2026-10-26：補審上游 PR #745–#748，reviewed_pr_through 推到 #748

取每筆**目前**的 head 讀完 diff（#745 `00d044d`、#746 `480a538`、#747 `de0fb0f`、#748 `2e927ca`；時間軸上沒有 force-push），並掃過隱藏內容（`\S\s{40,}\S`、`eval`／`new Function`／`global.`／base64／hex 長字串、超長單行），無命中。

- **#745**（closed，未合併）：同一作者把它拆成 #747（文件）與 #748（驗證器）後自己關掉，內容分別在下面兩筆，不另處理。
- **#748**（open）`scripts/validate-reference-links.js` +14/-4、測試 +28：`REFERENCE_LINK_RE` 的 fragment 字元集加入 `%`，比對 heading 前先 `decodeURIComponent`，壞的跳脫序列回報為 violation 而不崩潰。**缺陷在本 fork 存在**，實測 `REFERENCE_LINK_RE`（第 60 行，字元集 `[\p{L}\p{N}_-]` 不含 `%`）：`references/patterns.md#caf%C3%A9` 只抓到 `caf`（對 `## Café` 誤報找不到 heading）、`references/patterns.md#%70atterns` 抓不到 fragment（整段略過，無效錨點被放行）。但 `grep -rnE 'references/[^ )]+\.md#[^ )]*%' skills references docs README*.md` 在本線 0 筆命中，沒有任何現存連結踩到。本 fork 在同一個檔案另有 `stripInlineHtml` 的自有修正（與上游分歧 +16/-4），照抄會與上游日後合併版本分岔。**不採用**，等上游合併。
- **#747**（open）`docs/antigravity-setup.md` +3/-1：不再叫使用者把本 repo 的貢獻者 `AGENTS.md` 複製到自己的專案，改為自建專案專屬 `AGENTS.md`，並連到 `CONTRIBUTING.md#repo-scoped-files`。本 fork 該檔與上游逐位元組相同，第 110 行仍是「copy or link `AGENTS.md`」，所以是新增內容而非本線缺陷。**不採用**，等上游合併。
- **#746**（open）`plugin.json` +1：加 `"$schema": "https://agent-plugins.org/schemas/1.0.0/plugin.schema.json"`（URL 實測回 200 `application/json`）。`plugin.json` 是本 fork 持有的 manifest（版本維持 0.6.9，與上游分歧），作者只以第三方規格頁面主張「必填」，沒有上游維護者回應，也不是本線任何 gate 的要求。**不採用**，等上游表態。

**觸發條件**：#747／#748 任一合併 → 下次 commit 軸同步自動帶入（#748 合併後 `validate-reference-links.js` 需與本線的 `stripInlineHtml` 手動合併）；本線出現 `references/*.md#...%XX` 形式的連結或 CJK 標題錨點 → 提前採用 #748；#746 被上游合併 → 同步時一併處理並確認 5 份 manifest 一致。commit 軸仍是 `aeac41d`、issue 軸仍是 #717，無新增。

## 2026-10-28：補審上游 PR #749，reviewed_pr_through 推到 #749

取目前 head `ab8a5ca` 讀完 diff（+44/-35），並掃過隱藏內容（`\S\s{40,}\S`、`eval`／`new Function`／`globalThis`、base64／hex 長字串、超長單行），無命中。

- **#749**（open，未合併）「Fix/user invoked commands」：在 `.claude/commands/` 的 9 個生命週期指令（build、code-simplify、constraints、plan、review、ship、spec、test、webperf）frontmatter 加 `disable-model-invocation: true`，讓這些指令只能由使用者觸發，底下的 skill 仍可被模型路由。理由是 Claude Code 把 command 檔當 skill 看待，模型可能自行觸發 `/build auto`、`/ship` 這類有副作用的流程。本 fork 這 9 個檔與上游逐位元組相同（`ship.md` blob `fa7b7ef` 兩邊一致），`git grep disable-model-invocation` 無命中，所以行為在本線一樣存在。
- **#749 的其他改動**（逐字比對 head 版本與本線，PR 說明沒有提）：`skills/using-agent-skills/SKILL.md` 只是技能清單的欄位對齊空白；另有 5 個指令檔的說明被改寫並刪掉防護文字——`build.md` 拿掉「每個任務自己一個 commit」等句子，並把「無法用 `git revert` 復原」換成 `git reset --hard`／`git checkout --` 的說法；`constraints.md` 拿掉 gitleaks（一律 `--redact`）等工具清單；`ship.md` 拿掉 persona 彼此獨立所以平行安全的說明；`spec.md` 拿掉「依相依順序逐一寫各模組的 spec」；`webperf.md` 刪減 Chrome DevTools MCP 用法。這些改寫是削弱，不是修正。

**決定**：不單獨摘取，等上游合併後隨 commit 軸同步（與 2026-10-25 起的慣例一致：未合併 PR 可能在審查中改寫）。

**觸發條件**：#749 合併 → 經 commit 軸同步時，上述 5 個指令檔的說明改寫要逐行審，不整檔照收；本線實際發生模型自行觸發 `/ship`、`/build auto` → 提前採用時只移植 9 行 `disable-model-invocation: true`（移植做法不是 diff），不帶入說明改寫。

## 2026-10-30：審查上游 PR #750、#751、#752，reviewed_pr_through 推到 #752

取每筆目前 head（#750 `2b14012`、#751 `1cb26d0`、#752 `0c85514`）讀完 diff 並掃過隱藏內容（`\S\s{40,}\S`、`eval`／`new Function`／`globalThis`、base64／hex 長字串、超長單行）：
- #750、#751 無命中。
- #752 命中兩處：一處為 `evals` 出現在文件表格文字、一處為 markdown 說明中的長網址，皆屬正常文件字串，無惡意注入或隱藏指令。

- **#750**（open，未合併）`docs(tdd): exercise the real boundary for crash and rollback tests`（diff +166/-0）：在 `skills/test-driven-development/SKILL.md` 的「Prefer Real Implementations Over Mocks」段落增加一句：「For crash or rollback behavior, exercise the real boundary: an injected exception is not process termination, and a mocked transaction call is not a database rollback.」；並新增 `evals/cases/test-driven-development.json`（case 4）、`evals/fixtures/test-driven-development-persistence/`（BUG.md、README.md、test_vault.py、vault.py）與離線 oracle `scripts/test-driven-development-fixture-test.py`。上游維護者（addyosmani）已要求作者收斂到僅保留該句提醒，作者已於 `2b14012` 配合修改；eval case 與 fixture 仍保留（作者於 PR 留言說明）。此為文件強化與 eval 資產擴充，本線無急迫缺陷。
- **#751**（closed，未合併）`docs(review): verify formal evidence against its scope`（diff +165/-0）：在 `skills/code-review-and-quality/SKILL.md` 新增對 formal-proof／model-checking 證據的審查原則，並提供驗證 fixture 與 oracle 測試。因上游維護者駁回 #752，認定若無 formal model checking 技能則該 review 指引亦無單獨保留必要，已於 2026-10-29 關閉。
- **#752**（closed，未合併）`feat(skills): add bounded formal model checking workflow`（diff +493/-10）：新增第 26 個技能 `formal-model-checking`、相關 fixture／eval 及文件索引。上游維護者於 2026-10-29 明確拒絕並關閉（指出此為利基型技能，維持 catalog 只包含多數團隊通用工作流，建議做成外部 standalone skill）。

**決定**：#750 不單獨摘取，等上游合併後隨 commit 軸同步；#751 與 #752 因已被上游明確拒絕並關閉，本線遵循上游產品核心邊界，不採用。

**觸發條件**：#750 被上游合併 → 經 commit 軸同步自動帶入；若本線日後由維護者授權引進 formal verification 類工作流 → 重新評估 #751／#752 或改為獨立外掛。

## 2026-10-30：審查上游 0.6.14 commit 軸（aeac41d..eb07f19）、PR #753–#767、issue #765

### 一、Commit 軸審查（aeac41d..eb07f19，落後 70 commit）

上游發布 0.6.14（commit `eb07f19f52c2669f2364897aaa293e2aaddd7b1c`），包含 70 個 commit，涉及 53 個檔案變更。

**逐項審查與決策**：
1. **Release bump 0.6.14（`eb07f19`）**：**不採用**。本 fork 嚴格維持「單一最新分支（main）、單一最新 tag、單一最新 release」（現為 0.6.9）政策。升版需刪除舊 tag 與 release，屬維護者專屬授權動作（見路線圖近期第一列待辦）。5 份 plugin manifest（`plugin.json`、`.agents/plugins/marketplace.json`、`.claude-plugin/marketplace.json`、`.claude-plugin/plugin.json`、`.codex-plugin/plugin.json`）版本號維持 0.6.9。
2. **上游合併之 PR 改動（共 33 項實質變更與其 merge commit）**：
   以下每項為「#PR / 該 PR 的 commit、最後一個是 merge commit」；共 33 個 PR（33 個 merge）、36 個非 merge commit（另有 release bump `eb07f19`，見第 1 項）。逐項裁決格式：`#NNN：採用，已同步；衝突：無／<檔案>`。「衝突」指該 PR 動到本 fork 自持的檔案（5 份 manifest、繁中 `README.md`、`AGENTS.md`、`.gitignore`、`scripts/validate-reference-links*.js`）。
   - **#463 / fb4c9ff、2f06a51、9d00489**：root `plugin.json` 符合 Agent Plugins 1.0.0 規範（加入 `$schema`、author、homepage、repository、license、keywords）與 Copilot CLI 文件說明（`docs/copilot-cli-setup.md`）。#463：採用，已同步；衝突：`plugin.json`（fork 持有的 manifest；內容取上游，版本維持 0.6.9）。
   - **#668 / 46a73df、e4572ef、dae1f9d、3e1f929**：evals 路由修正，處理縮寫、名詞化與 auth case 防護。#668：採用，已同步；衝突：無。
   - **#688 / 70e6fdd、59142df**：testing-patterns 的 Playwright 列表項目改依文字過濾。#688：採用，已同步；衝突：無。
   - **#690 / 0004999、311cc3a**：skills 修正傳入 `--fix` 至 linter 的語法。#690：採用，已同步；衝突：無。
   - **#691 / 7230f52、076030d**：ci-cd-and-automation 的 rollback 版本改由環境變數傳入以防注入。#691：採用，已同步；衝突：無。
   - **#692 / 081b915、11d3171**：frontend-ui-engineering 補齊 empty-state action prop 宣告。#692：採用，已同步；衝突：無。
   - **#696 / f1f6fbf、b8a70d2**：code-simplification 支援貼上 inline 程式碼時觸發（#620）。#696：採用，已同步；衝突：無。
   - **#698 / 9f91cc4、2579798**：deprecation-and-migration 的 adapter 範例型別修正。#698：採用，已同步；衝突：無。
   - **#699 / 8622a3d、f215ac6**：performance-checklist 的 onINP import alias 修正。#699：採用，已同步；衝突：無。
   - **#702 / 2b5e8a6、49ec30b**：validate-artifact-paths 完整檔名比對，避免將 test-plan.md 誤判為 plan.md。#702：採用，已同步；衝突：無。
   - **#704 / 089edac、9d75719**：Windsurf setup 規則檔寫入實體換行分隔。#704：採用，已同步；衝突：無。
   - **#705 / efeb9ab、84fce3b**：Gemini CLI MCP 設定指向 settings.json。#705：採用，已同步；衝突：無。
   - **#706 / 6720a51、f97d842**：frontend-ui-engineering 向 TaskItem 傳遞 toggle 與 delete handler。#706：採用，已同步；衝突：無。
   - **#707 / 8e6726d、4c28939**：documentation-and-adrs 註解與 fixed-window 實作對齊。#707：採用，已同步；衝突：無。
   - **#708 / 29e567f、b209085**：floor-guard 從獨立欄位讀取 ratchet 方向。#708：採用，已同步；衝突：無。
   - **#710 / 63128d0、35870a2**：api-and-interface-design 冪等守衛回傳標準 error shape。#710：採用，已同步；衝突：無。
   - **#711 / d3ffa3c、a4a21f6**：ci-cd-and-automation 修正 setup-node 快取標的說明（npm cache 非 node_modules）。#711：採用，已同步；衝突：無。
   - **#712 / 60b218f、e36949e**：debugging-and-error-recovery 採用 Jest 30 位置參數測試篩選。#712：採用，已同步；衝突：無。
   - **#713 / 27e6020、82be2f5**：constraint-driven-development 補充 Vitest coverage provider 安裝提示。#713：採用，已同步；衝突：無。
   - **#714 / 0929438、fdbc55a**：9 個生命週期指令（build、code-simplify、constraints、plan、review、ship、spec、test、webperf）frontmatter 加 `disable-model-invocation: true`。**經逐行比對確認**：上游只新增該 9 行，未包含先前 #749 中刪改指令說明文字與削弱防護（每任務一個 commit、gitleaks `--redact`、ship 平行 fan-out 句）之內容，健康無害。#714：採用，已同步；衝突：無。
   - **#719 / 6f9906e、09a9144**：accessibility-checklist 將 HTML label 關聯至控制項（`htmlFor` 換 `for`）。#719：採用，已同步；衝突：無。
   - **#720 / 07e0a68、9ec85eb**：accessibility-checklist 改呼叫具備 binary 的 axe CLI。#720：採用，已同步；衝突：無。
   - **#721 / ee3e850、6ace7d6**：performance-optimization 改呼叫 Lighthouse CI（`@lhci/cli`）。#721：採用，已同步；衝突：無。
   - **#723 / 07ff519、2bac5b6**：Cursor setup 文件連結更新。#723：採用，已同步；衝突：無。
   - **#724 / 24596ab、9c555fa**：idea-refine 從已安裝 skill 目錄執行 helper。#724：採用，已同步；衝突：無。
   - **#725 / d14cf2d、2ba5de2**：accessibility loading 區域補齊 `role="status"`。#725：採用，已同步；衝突：無。
   - **#726 / ab15a85、efab8ba**：security-and-hardening 在 task 不存在時先回傳 404 再做擁有權檢查。#726：採用，已同步；衝突：無。
   - **#727 / 0c65ba7、d7cc2cc**：performance-checklist 將 Lighthouse 指向 `http://localhost`。#727：採用，已同步；衝突：無。
   - **#728 / 76cbb8a、974738b**：source-driven-development 引文對齊 React 19 原文。#728：採用，已同步；衝突：無。
   - **#729 / 0b7d58a、604b258**：constraint-driven-development 的 gitleaks 指令從 `gitleaks detect` 改為 `gitleaks dir .`，掃工作目錄而不是只掃已 commit 的歷史（`0b7d58a` 只改這個，`--redact` 本來就有）。issue #717 上游仍 open，本輪不宣稱解決（#729 內文沒提 #717）。同步後 `rg "gitleaks detect" skills` 無命中。#729：採用，已同步；衝突：無。
   - **#735 / 2db4f1c、2ddba6f**：SDD-CACHE.md 一致使用 reuse 術語。#735：採用，已同步；衝突：無。
   - **#743 / 2807f14、2669c40**：evals 在評分前拒絕不完整的執行器 stream。#743：採用，已同步；衝突：無。
   - **#747 / de0fb0f、a06c46d**：Antigravity setup 採用專案專屬 AGENTS.md。#747：採用，已同步；衝突：無。
3. **安全與自有修正比對**：
   - 比對確認 `scripts/validate-reference-links.js` 在本次 70 commit 範圍內上游未動，本 fork 針對 CodeQL alert #1 的 `stripInlineHtml` 自有修正繼續保留。
   - SkillSpector 自我掃描（2026-10-31 同步後實跑，SkillSpector 2.12.0、`--no-llm`、套用現行 `.skillspector-baseline.yaml`）：上游動到的 14 個 skill 逐一掃描，7 個（ci-cd-and-automation、debugging-and-error-recovery、deprecation-and-migration、documentation-and-adrs、frontend-ui-engineering、idea-refine、performance-optimization）0 筆新 finding；另 7 個共 15 筆未被基準涵蓋（api-and-interface-design 1、code-simplification 2、constraint-driven-development 2、context-engineering 2、security-and-hardening 1、source-driven-development 3、spec-driven-development 4）。逐筆讀過命中的原文與位置，15 筆都是已審條目因檔案內容變動而換雜湊（指紋綁內容），判斷不變、沒有新種類 finding；已用 `skillspector baseline --no-llm -o -` 取得新雜湊，原地取代 15 筆過期條目並更新理由與行號，沒有新增條目、沒有為過掃描改上游內容。受影響原文的上游改動：#710 冪等守衛 error shape（TM1）、#696 code-simplification description（RA1、EA3）、#708 floor-guard 正規式與 #729 gitleaks 指令（constraint-driven-development 兩筆 AE1，仍是 git hook 範例，只以 argv 陣列呼叫 git）、#726 在範例補 404（SSRF1，命中的 TOCTOU 句子不變）、#690／#728 等文字調整（context-engineering、source-driven-development、spec-driven-development 的教學性反面範例）。更新後 25 個 skill 完整掃描結果見 2026-10-31 條目。

### 二、PR 軸審查（PR #753–#767，共 14 筆，13 筆 OPEN、1 筆 CLOSED 狀態）

逐筆檢視目前 head 並掃描隱藏內容（`\S\s{40,}\S`、`eval`／`new Function`／`globalThis`、base64／hex 長字串、超長單行），均無惡意注入：
- **#753**（open）：`docs(ci): preserve verification contract during optimization`（CybotTM，head `c7d81190`，+85/-7，3 檔：`skills/ci-cd-and-automation/SKILL.md` +35/-7、`evals/cases/ci-cd-and-automation.json` +17、`evals/fixtures/ci-quality-contract/brief.md` +33）。在 ci-cd-and-automation 加入優化時不破壞驗證合約之規範。依慣例等上游合併後隨 commit 軸同步，不單獨摘取。
- **#754**（open）：`docs(doubt): keep contradicting caller evidence in the review unit`（CybotTM，+2/-0）。在 doubt-driven-development 補充審查單元保留衝突呼叫證據。等上游合併後同步。
- **#755**（open）：`docs(planning): choose continuation by worker lifecycle`（CybotTM，head `12bbc3fc`，+87/-0，5 檔：`skills/planning-and-task-breakdown/SKILL.md` +7、`evals/cases/planning-and-task-breakdown.json` +33、`evals/fixtures/worker-lifecycle/` 3 個 fixture 共 +47）。在 planning-and-task-breakdown 補充依 worker lifecycle 決策接續。等上游合併後同步。
- **#756**（open）：`fix(evals): drop command names from the skill-fired graders after #714; record the re-run`（ayobamiseun）。在 #714 合併後自 grader 移除指令名稱。等上游合併後同步。
- **#757**（open）：`fix(debugging-and-error-recovery): say the skill applies when the diff or stack trace is pasted inline (#620)`（ayobamiseun）。技能描述增加貼上 diff / stack trace 觸發。等上游合併後同步。
- **#758**（open）：`fix(git-workflow-and-versioning): say the skill applies when the diff is pasted inline (#620)`（ayobamiseun）。技能描述增加貼上 diff 觸發。等上游合併後同步。
- **#759**（open）：`fix(security-and-hardening): name session cookies in the description`（ayobamiseun）。技能描述補充 session cookies。等上游合併後同步。
- **#760**（open）：`feat(evals): name a positive prompt that passes top_k without ranking first`（ayobamiseun）。eval 工具回報 top_k 但非第一名的正向提示詞。等上游合併後同步。
- **#761**（open）：`docs(evals): add a ledger of the description clauses measured so far`（ayobamiseun）。補充 eval 量測條款帳本。等上游合併後同步。
- **#762**（open）：`fix(test-driven-development): re-tune the pasted-code clause for the 2.1.312 router (#620)`（ayobamiseun）。微調貼上程式碼條款以適配 router。等上游合併後同步。
- **#763**（open）：`fix(code-review-and-quality): say the review may look quick and what the skill adds (#620)`（ayobamiseun）。微調 review 描述。等上游合併後同步。
- **#764**（open）：`Review evidence and reliability`（Jeddy2023，head `07ab1b58`，+694/-97，38 檔，3 個 commit；2026-10-31 依目前 head 重讀整份 diff，隱藏內容掃描無命中）。提議新增第 26 個技能 `backend-reliability-review`（含 `integration-and-job-checks.md`）、`references/review-evidence-standard.md`、eval case 與 fixture，並改寫 build／plan／review／ship／spec 五個指令（`.claude/commands/`、`commands/*.toml`、`.gemini/commands/`）、三個 persona、`spec-driven-development`、`code-review-and-quality` 等 skill 與 README／docs 的技能數字。**目前 head 另有兩類本線不能照收的改動**：(1) `.claude-plugin/marketplace.json` 把 marketplace 名稱改為 `kenj-agent-skills`、來源 repo 改為 `Jeddy2023/agent-skills`（作者個人 fork），與已 closed 的 #767 同類；(2) 五份 manifest 版本改 0.7.0。persona 檔改寫審查守則（code-reviewer 守則 6 條改 9 條，Verdict 加 HOLD，「What's Done Well」變成可省略）；`agents/security-auditor.md` 與 `agents/test-engineer.md` 各有一處兩條規則被黏在同一行（`otherwise5.`、`functions6.`，缺換行），目前 head 的排版有損壞。動到核心 catalog 結構與指令行為，屬大型 proposal，需由上游維護者決策。**不單獨摘取，等上游合併後重審**（合併版若仍含 marketplace 來源或版本改動，同步時不收）。
- **#766**（open）：`fix(hooks): preserve re-indented placeholders and harden Stop cleanup in simplify-ignore.sh`（Quinnod345，head `52acec00`，+123/-10，2 檔：`hooks/simplify-ignore.sh` +38/-9、`hooks/simplify-ignore-test.sh` +85/-1；2026-10-31 依目前 head 重讀 diff，隱藏內容掃描無命中）。修復 Issue #765：JSON 解析失敗時 `exit 0`、重新縮排後的 placeholder 與改過 reason 的還原、Stop 清理的 `rmdir ... || true`（`set -e` 下不再因缺少 lock 目錄中斷）、`grep -qF --`。只動 hook 與其測試，無網路、`eval` 或寫出專案外的行為。缺陷在本線存在（`hooks/simplify-ignore.sh` 與上游逐位元組相同），但尚未造成本線損害，不符合「單獨摘取」的例外條件。**不單獨摘取，等上游合併後同步**。
- **#767**（closed）：`chore: point Claude Code plugin source at this fork`（ChrisMacpherson，+4/-4）。修改 plugin 來源指向個人 fork，已由作者關閉，上游未合併，不採用。

**決定**：PR #753–#766 共 13 筆全為 open 未合併，依慣例不單獨摘取，等上游合併後隨 commit 軸同步；PR #767 為 closed 未合併不採用。`reviewed_pr_through` 推進至 767。

### 三、Issue 軸審查（Issue #765，1 筆，OPEN 狀態）

- **#765**（open）：`bug(hooks): simplify-ignore.sh corrupts re-indented placeholders and aborts Stop cleanup when .lock dir is missing`。Quinn O'Donnell 回報 `hooks/simplify-ignore.sh` 三處問題（縮排還原語法損壞、`set -euo pipefail` 下缺少 lock 目錄造成 Stop 迴圈中斷、grep 缺乏 `--` 造成 SQL/Lua 註解誤報），並附伴隨 PR #766。本 fork 產品檔案維持上游標準，不單獨處置，等上游合併 #766 後隨 commit 軸同步。`reviewed_issue_through` 推進至 765。

### 四、三軸水位推進與驗證

- `tools/upstream_baseline.json` 水位更新：
  - `reviewed_through`: `eb07f19f52c2669f2364897aaa293e2aaddd7b1c`
  - `reviewed_date`: `2026-10-31`（初審 2026-10-30；2026-10-31 重讀 #764、#766 目前 head）
  - `reviewed_pr_through`: 767
  - `reviewed_issue_through`: 765
- `python tools/check_upstream_updates.py --strict` 實跑 exit code 0。
- `tools\dev_check.ps1` 實跑 exit code 0（WINDOWS DEV CHECK GREEN）。

## 2026-10-31：同步上游 0.6.14 產品檔（`aeac41d..eb07f19`）

**決定**：把 2026-10-30 審查過的 70 個 commit（動 53 個檔案）同步進本線；版本號不採用，維持單一 tag／release 0.6.9。逐 PR 裁決見上節第一節第 2 項。

**方法**（不 merge、不動 HEAD）：

1. `git fetch upstream main`，確認 `upstream/main` 是 `eb07f19`。
2. 逐檔比對 53 個檔案在本線與 `aeac41d` 的 blob：48 個相同（含 6 個新增檔）、5 個不同（5 份 plugin manifest，只差 `version` 0.6.9）。
3. 48 個相同的檔案用 `git show eb07f19:<path>` 寫入工作樹。5 份 manifest 中 4 份上游這段範圍內只改了版本號（0.6.13 → 0.6.14），不動；`plugin.json` 取上游新內容（#463：`$schema`、author、homepage、repository、license、keywords），版本維持 0.6.9。
4. 逐檔驗證：53 檔中 48 檔與 `eb07f19` 的 blob 相同（`git hash-object --no-filters` 對 `git rev-parse eb07f19:<path>`），其餘 5 檔只差版本號。全樹（223 個檔案）再比對一次，與 `eb07f19` 不同的只有下列登記的分岔檔。 全樹比對只涵蓋上游路徑，本線獨有檔另列。

**分岔登記（同步後未與 `eb07f19` 一致的檔案與理由）**：

| 檔案 | 理由 |
| --- | --- |
| `plugin.json`、`.claude-plugin/plugin.json`、`.claude-plugin/marketplace.json`、`.agents/plugins/marketplace.json`、`.codex-plugin/plugin.json` | 版本維持 0.6.9（單一 tag 政策，升版需刪舊 tag 與 release，屬維護者授權；見路線圖近期第一列）。`plugin.json` 其餘內容與上游一致 |
| `README.md` | 繁中主檔，英文原文在 `README.en.md` |
| `AGENTS.md`、`.gitignore` | `AGENTS.md` 尾端 fork 維護規則；`.gitignore` 多出 fork 本機工具輸出（`.venv/`、`.pytest_cache/`、`.ruff_cache/`、兩份檢查報告、`.skillspector-reports/`） |
| `scripts/validate-reference-links.js`、`scripts/validate-reference-links-test.js` | CodeQL alert #1 的 `stripInlineHtml` 自有修正（2026-10-24）；這 70 個 commit 上游沒動這兩個檔 |
| `CLAUDE.md`（本線不存在） | 只維護 `AGENTS.md` |
| `hooks/hooks.json`（上游已刪、本線仍在） | 上游 `a598aab`（#569）刪除，本線未跟進，非刻意分岔；是否刪除見路線圖近期表 |

**#729 與 issue #717**：`rg "gitleaks detect" skills` 同步後無命中。issue #717 上游仍 open，本輪不宣稱解決。

**#748**：2026-10-29 已 closed 未合併，不再等上游合併；本線出現 `references/*.md#...%XX` 連結或 CJK 標題錨點時才最小重做（路線圖中期表）。

**驗證**（實跑）：

- SkillSpector 自我掃描：同步前（舊基準）上游動到的 14 個 skill 有 15 筆未涵蓋 finding（7 個 skill），全為既有已審條目換雜湊；原地取代後，`tools\dev_check.ps1` 的 25 個 skill 完整掃描為 0 筆新 finding。
- `pwsh -NoProfile -File tools/dev_check.ps1` exit 0；`python tools/check_upstream_updates.py --strict` exit 0；`git diff --check` exit 0。
