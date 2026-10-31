# 路線圖

> 本 repo 後續工作的單一真相源。做完一項，就在同一個 commit 刪掉那一列；新工作只加在這裡。
> 現況段的 repo 健康數字是 2026-10-30 依 `main` 查的快照；上游同步狀態是 2026-10-31 實測。開工前先重查 GitHub。

## 現況

這是 addyosmani/agent-skills（AI coding agent 工程技能包）的 Windows-first 維護型 fork；在 GitHub 上它不是 fork 關係，但上游基線都指向該 repo（`tools/upstream_baseline.json`）。維護面健康：`main` 上 CI、CodeQL、Test Plugin Installation 最近一次皆 success；Upstream check 為綠燈（`check_upstream_updates.py --strict` 實跑 exit 0），open PR 0 筆、Dependabot 與 Code scanning 告警 0 筆；issue 功能已停用，issue 數「未查到」不是 0（2026-10-29 `gh` 查詢）。已同步到上游 0.6.14 的產品檔（commit 軸水位 `eb07f19f52c2`；版本號未採用，維持 0.6.9）；與 `eb07f19` 不同的檔案只有登記的分岔檔：5 份 plugin manifest（`plugin.json`、`.claude-plugin/plugin.json`、`.claude-plugin/marketplace.json`、`.agents/plugins/marketplace.json`、`.codex-plugin/plugin.json`）只差版本號，以及本線自有的繁中 `README.md`、`AGENTS.md`（尾端 fork 規則）、`.gitignore`、`scripts/validate-reference-links.js` 與其測試（CodeQL 修正）、不存在的 `CLAUDE.md`、上游已刪但本線仍在的 `hooks/hooks.json`。issue 水位 765（#765 已審）；PR 水位已審至 767（open 追蹤見中期表，#751、#752、#767 closed）。

## 近期：可以直接動手

| 項目 | 為什麼 | 驗收方式 | 建議執行者 | 證據 |
| --- | --- | --- | --- | --- |
| 決定 `hooks/hooks.json` 刪除或保留 | 上游 `a598aab`（#569）已刪：SessionStart 注入 meta-skill 造成雙重路由、每 session 多耗約 3.5k tokens；本線仍註冊，與同步進來的 `hooks/session-start.sh:8` 衝突，`AGENTS.md` 又規定 `hooks/` 以上游為準 | 刪除則 `hooks/` 與上游一致；保留則在 `docs/DECISIONS.md` 寫理由；`tools\dev_check.ps1` 綠 | Antigravity | `docs/DECISIONS.md` 2026-10-31 分岔表；`hooks/session-start.sh:8` |
| 維護者決定是否授權升版到上游 0.6.14 | 本 fork 維持單一 tag／release（0.6.9），上游已到 0.6.14（commit `eb07f19` 已同步產品檔，版本號沒採用）；升版需要刪舊 tag 與 release，屬維護者授權動作 | 在 `docs/DECISIONS.md` 記決定。若授權：五份 plugin manifest 版本一致、新 tag／release 存在、舊 tag 處理方式寫明、`validate-versions` 與 `tools\dev_check.ps1` 綠；若不授權：寫明理由並保留單一 tag 政策 | 維護者 | `docs/DECISIONS.md:290`；`gh release list -R SanHsien/agent-skills` |

## 中期：等條件成立再做

| 項目 | 觸發條件 | 驗收方式 | 建議執行者 | 證據 |
| --- | --- | --- | --- | --- |
| 上游合併 open PR 後同步（所有 open PR 都等合併；近輪重查過：#718、#722、#730–#733、#736、#739、#742、#744、#750、#753–#764、#766；更早的見 `docs/UPSTREAM.md:105`） | 任一筆被上游合併、commit 軸出現新 commit；依慣例未合併 PR 不單獨摘取 | 同步後，除登記的分岔檔（繁中 `README.md`、`AGENTS.md`、`.gitignore`、`scripts/validate-reference-links*.js`、5 份 plugin manifest 的版本號）外，上游動到的檔案與 `upstream/main` 逐位元組一致；`reviewed_through` 推進；`tools\dev_check.ps1` 綠 | Claude Sonnet | `docs/DECISIONS.md`；`tools/upstream_baseline.json` |
| 提前採用 #718（issue #717：staged-secret 檢查把憑證原文印進 agent 日誌） | #718 被上游合併（隨 commit 軸帶入）；或本線 agent 日誌實際出現 secret 值、或上游長期不動 | `references/security-checklist.md`、`skills/git-workflow-and-versioning/SKILL.md`、`skills/security-and-hardening/references/hardening-patterns.md` 不再有會印出命中行的 `git diff --cached\|--staged \| grep -i`；`tools\dev_check.ps1` 綠 | Claude Sonnet | `docs/DECISIONS.md:324`；issue #717；PR #718 |
| #748 已 closed 未合併；本線出現 `references/*.md#...%XX` 連結或 CJK 標題錨點時最小重做 | 本線出現 `references/*.md#...%XX` 形式連結或 CJK 標題錨點（#748 已於 2026-10-29 closed，不再等上游合併） | 在 `validate-reference-links.js` 最小重做 fragment 解碼比對，與本線的 `stripInlineHtml` 並存，node 測試全過；`tools\dev_check.ps1` 綠 | Codex | `docs/DECISIONS.md:362` |

## 刻意不做

| 不做什麼 | 理由 | 什麼情況下重新考慮 |
| --- | --- | --- |
| 單獨摘取未合併的上游 PR | 未合併 PR 可能在審查中改寫；例外只限本線已確認存在缺陷的項目（如已採用的 #563、#573） | 缺陷在本線實際造成損害，且上游長期不動 |
| 採用上游版本號 bump（0.6.10–0.6.14） | 單一 tag 政策，升版需刪舊 tag（`docs/DECISIONS.md:290`） | 近期第一列的維護者決定為授權 |
| 把 hook 的 bash 測試納入 `tools\dev_check.ps1` | Windows 本機以 bash 腳本為主，CI 已跑（接續開發報告 2026-10-25） | CI 缺席，或 hook 測試開始只在 Windows 出錯 |
| 對上游開 PR／回貢 | 預設只打 `SanHsien/` 名下 repo | 維護者在新的對話中明確要求回貢 |

## 維護方式

fork：以 `Upstream check` workflow 為訊號（failure＝上游有新 PR／commit／issue 未審），三軸（commit、PR、issue）水位分開推進，審完在 `docs/DECISIONS.md` 記理由。直接推 `main`；Dependabot 只開 PR，CI 綠且讀完 diff 才合併。本機跑 `tools\dev_check.ps1` 約需 10 分鐘以上，逾時是未完成不是失敗。
