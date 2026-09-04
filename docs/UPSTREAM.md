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
