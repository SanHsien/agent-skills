# 上游維護

## Remote

- Fork：`origin` → `https://github.com/SanHsien/agent-skills.git`
- 原作者：`upstream` → `https://github.com/addyosmani/agent-skills.git`
- 追蹤分支：`main`

## 檢查新提交

```powershell
git fetch upstream main
python tools\check_upstream_updates.py --strict
```

工具以 `tools/upstream_baseline.json` 的 `reviewed_through` 為起點，列出所有未審查提交；
`reviewed_pr_through` 與 `reviewed_issue_through` 是另外兩個獨立水位，涵蓋 PR 與 issue
（用 `--state all`，已關閉但未合併的項目也算未審查）。有新項目或檢查失敗時，`--strict`
回傳非零；排程 workflow 也會因此明確失敗。

## 審查清冊

每次只做一次批次審查：

1. 讀 commit 主旨與變更檔案（open PR 必須讀 diff，禁止只憑標題結案）。
2. 判斷是否與繁中 README、Windows gate 或測試衝突。
3. 可直接同步的提交用 merge；只需要部分修正時 cherry-pick 或最小重做。
4. 跑 `pwsh -NoProfile -File tools\dev_check.ps1`。
5. 在 [`docs/DECISIONS.md`](DECISIONS.md) 記錄採用／略過理由（須引用具體檔案與衝突點）。
6. 驗證完成後才把 baseline 推進到已審查的完整 40 字元 SHA，以及對應的 PR／issue 水位。

Baseline 代表「已審查」，不代表「全部已合併」。

README 衝突的解法：上游新英文說明翻進 `README.md`，並同步 `README.en.md`。技能／指令／
角色目錄表可同步。來源與授權 credit 留在 README 與 `NOTICE.md`。

## 2026-09-04：fork 起點

本 fork 自上游 `main` `1c760d643497e9da289300e5eb2f5aca861503f7`
（`Merge pull request #316 from nucliweb/docs/advanced-per-agent-configuration`）建立。
此 SHA 設為第一個 `reviewed_through`。之後的上游 commit 才需要進入審查清冊。

水位：

- PR：已看到 **#547**（`reviewed_pr_through`）
- issue：已看到 **#542**（`reviewed_issue_through`）
- commit baseline：`1c760d6`（完整 SHA 見 `tools/upstream_baseline.json`）
- 下次只看編號更大的，或已評估項目是否出現新 commit／新 head

## 2026-09-06：13 commits／13 PR bounded review

- commit baseline：`469d00f4e67ff4a21eb6e6e467a086c9a1f1deb8`
- PR：已看到 **#560**；issue：仍為 **#542**（沒有新增）
- 採用七筆實質內容：shipping SLO 三筆、observability entry point、destructive path guard、
  lifecycle handoff、Copilot CLI／VS Code 文件。
- 五筆 merge commit 沒有額外 diff；0.6.9 manifest bump 因 fork tag ancestry 不相容而略過。
- #548、#551–#560 都仍 open；完整逐筆理由在 [`DECISIONS.md`](DECISIONS.md)，合併或 head
  改變後再重新判斷，不 raw merge 47 檔的 fork overlay 差異。

## 2026-09-11：11 commits／PR #561–#567／issue #565 bounded review

- commit baseline：`6ca0cd7db39b41b1c37e26d335c507ee92382c6d`
- PR：已看到 **#567**；issue：已看到 **#565**
- 採用八筆：observability runbook 撰寫小節（初版＋review 收斂）、context-engineering
  Context Budget Management（初版＋兩筆 review 收斂）、`commands/planning.toml` 與
  `.gemini/commands/planning.toml` 補齊既有的 plan-clobber 防線、11 個 skill 的
  description-vocabulary 補詞＋eval rank-1 floor 提到 95；另從未合併的 #563 cherry-pick
  `scripts/run-evals.js` 的 null-grader-expectation 崩潰修復（fork 上該缺陷原樣存在）。
- 四筆 merge commit（`48cb116`／`38e2a4a`／`fe6f081`／`6ca0cd7`）沒有額外 diff，child commit
  已個別採用。
- #561、#562 已關閉且是提交者個人開發機殘留分支，與本 repo 無關；#564 是作者明講不求合併的
  展示 PR；#566（新 skill）、#567（下游改名相容指引）都是未合併且不是 fork 現有缺陷，等上游
  定稿後再評估。issue #565 是感謝信，無需動作。完整逐筆理由見 [`DECISIONS.md`](DECISIONS.md)。

## 2026-09-17：17 commits／PR #568–#578／issue #569、#572 bounded review

- commit baseline：`be4e44a9fbc5e8df0beaefadbb28bd22ee61cc39`
- PR：已看到 **#578**；issue：已看到 **#572**
- 採用：五筆 docs cherry-pick；`a1c9bd6`（restartable session boundaries）與 `17d8e52`（adapter 對照表，
  落在英文鏡像 `README.en.md`；命令數 8 → 9）最小重做。本批上游改過的檔案除繁中 `README.md` 外，
  都已與 `upstream/main` 逐位元組相同。
- 採用未合併 #573：reference-link 驗證器在 Windows 印反斜線，本機 7 個測試 1 個失敗；一行修正後 7/7。
- 延後至合併：#570、#574（含 issue #569）、#568、#571、#576、#577、#578。逐筆理由見
  [`DECISIONS.md`](DECISIONS.md)。

## 2026-09-30：78 commits／PR #579–#621／issue #581–#622 bounded review

- commit baseline：`2686b620fc1fed2e8f60c704839c766b8594c6b6`（upstream 0.6.11）；PR：已看到 **#621**；issue：已看到 **#622**
- 方法：本 repo 與上游無共同祖先，且上游變更檔（skills/、scripts/、hooks/、evals/、references/、四份 docs、CONTRIBUTING.md、test-plugin-install.yml、manifests）在本 fork 與 `be4e44a` 逐位元組相同，故以 `git checkout upstream/main -- <paths>` 同步，等同 78 個 commit 中全部有實質 diff 者（其餘約 30 個為無 diff 的 merge commit）。
- 採用（已合併的上游 PR，本機驗證：7 支 node 測試、3 支 hook shell 測試、`dev_check.ps1`）：#586、#587、#588、#594、#595、#596、#598、#600、#605、#607、#611、#612，以及 commit 範圍內的 #493／#496／#497／#498／#501／#510／#517／#545／#568／#570／#571／#573／#574／#576／#578（含 #569 的 SessionStart 不再自動注入）。`README.en.md` 標題 24 → 25（#570），中文 `README.md` 為維護索引不動。`.gitignore` 加 `evals/plugin/results/`。
- **adoption pending: #579／#589（security-and-hardening 拆出 `references/hardening-patterns.md`）**：同步後 `dev_check.ps1` 的 SkillSpector 自掃描對該 skill 報 16 筆新 finding（YR4／EA2／MP3／SSRF1 為既有誤判類別改行號重生，另 11 筆 AE1「本地參考檔 partial」）。放行需把新 fingerprint 寫進 `.skillspector-baseline.yaml`，那是放寬安全掃描，需維護者明確核可；本輪保留 fork 現有版本（`skills/security-and-hardening/`、`references/security-checklist.md` 不動）。重查條件：維護者核可 baseline 條目，或掃描器對本地參考檔不再標 partial。
- **release bump 不採用**：`c004a74`（0.6.10）、`2686b62`（0.6.11）。fork 只保留單一 tag／release（現為 0.6.9），升版需要刪舊 tag 與 release，屬維護者授權動作；manifests 內容（含 `experimental.evals`）已同步，版本維持 0.6.9。`validate-versions` 現以 root `plugin.json` 為準，五份一致。
- 開放中、待上游合併（follow-upstream）：PR #580、#593、#603、#606、#608、#613、#614、#615、#616、#618、#621；#617（draft，Oh My Pi 整合，本 fork 不支援該 agent）。
- 已關閉未合併：#582、#601、#609（新增 skill 投稿）、#592（安裝徽章宣傳）、#604、#610（上游拒收的 validator 功能）、#619（"Temp"）——不採用。
- issue：#581、#585（→#588）、#591（→#598）、#599（→#600）已由上游修正隨同步抵達；#583、#584、#597、#602、#620、#622 為上游開放中的討論／使用問題，無可套用修正（#597 的「找不到 references」與 #579 的 skill-local references 相關，隨 #579 一併延後）。
