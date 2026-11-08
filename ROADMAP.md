# 路線圖

> 本 repo 後續工作的單一真相源。做完一項，就在同一個 commit 刪掉那一列；新工作只加在這裡。
> 現況是 2026-11-02 本輪工作樹驗收範圍；遠端 CI 與其他 GitHub 狀態未在本輪重查。

## 現況

這是 addyosmani/agent-skills 的 Windows-first 維護型 fork。2026-11-02 本輪工作樹已同步 `eb07f19..7947664` 的 21 筆 commit、30 個產品檔；逐筆 SHA／裁決／理由見 `docs/DECISIONS.md`。2026-11-08 五份 manifest 已從 0.6.9 升到 0.6.15（內容早已同步、版本號停住會讓 Claude Code 的版本快取拿不到新檔；舊 tag 0.6.9 保留，單一 tag 政策取消，見 `docs/DECISIONS.md` 2026-11-08）。`hooks/hooks.json` 已決定保留：相容性與可回復優先，重複路由成本與重看條件已登記；未宣稱已解決原生宿主的雙重注入。pytest 9.2.0 在 repo 專用環境驗證，下限維持 9.1，依 deferrals 記錄針對 9.2.0 的暫緩理由。PR／issue 水位為 780／776（2026-11-08 續審 #774–#780 與 issue #776，見 `docs/DECISIONS.md`；起算時為 768／765）；#768 已關閉未合併，讀完 diff 後不採用，本輪未驗證遠端 CI；7947664..301b02b 的 14 筆 commit 與 PR #769–#773 已於同日續審：20 個產品路徑同步至 `301b02b`，當時 0.6.15 版本號未採用（2026-11-08 已採用），PR 水位推進到 773 並把 #769–#773 釘在 `monitored`，Upstream strict 為 exit 0。本機 gate 與 commit 水位以 `docs/UPSTREAM.md` 的本輪驗收紀錄為準。

## 近期：可以直接動手

| 項目 | 為什麼 | 驗收方式 | 建議執行者 | 證據 |
| --- | --- | --- | --- | --- |
| 發 0.6.15 的 GitHub Release（不建 tag、不 push tag） | 版號 0.6.15 已在 `main`（c9998d4）；GitHub Release 沒發，原因是代理工具的權限檢查擋下 `gh release create`。Claude Code 依 manifest 版號更新 plugin，不依賴 Release，所以不影響使用者拿到新版 | 在 repo 外的目錄執行（以免帶到本機那個從上游來的同名 tag）：`gh release create 0.6.15 -R SanHsien/agent-skills --target c9998d4339361e0b724492ade60eeb44f365ec0d --title 0.6.15 --latest --notes-file <CHANGELOG 0.6.15 段>`；之後 `gh release view 0.6.15 -R SanHsien/agent-skills` 存在且為 Latest，`gh release view 0.6.9 -R SanHsien/agent-skills` 仍在；做完刪這一列 | 維護者 | `docs/DECISIONS.md` 2026-11-08（發版指令）；CHANGELOG 0.6.15 段為 `CHANGELOG.md` 的 `## [Unreleased] - 2026-11-08` 一節 |

## 中期：等條件成立再做

| 項目 | 觸發條件 | 驗收方式 | 建議執行者 | 證據 |
| --- | --- | --- | --- | --- |
| 上游合併 open PR 後同步（所有 open PR 都等合併；近輪重查過：#769–#779、#722、#730–#732、#736、#742、#744、#750、#753、#755、#757、#761–#764、#766；更早的見 `docs/UPSTREAM.md:105`） | 任一筆被上游合併、commit 軸出現新 commit；依慣例未合併 PR 不單獨摘取 | 同步後，除登記的分岔檔（繁中 `README.md`、`AGENTS.md`、`.gitignore`、`scripts/validate-reference-links*.js`、`hooks/hooks.json`、5 份 plugin manifest 的版本號）外，上游動到的檔案與 `upstream/main` 逐位元組一致；`reviewed_through` 推進；`tools\dev_check.ps1` 綠 | Claude Sonnet | `docs/DECISIONS.md`；`tools/upstream_baseline.json` |
| #748 已 closed 未合併；本線出現 `references/*.md#...%XX` 連結或 CJK 標題錨點時最小重做 | 本線出現 `references/*.md#...%XX` 形式連結或 CJK 標題錨點（#748 已於 2026-10-29 closed，不再等上游合併） | 在 `validate-reference-links.js` 最小重做 fragment 解碼比對，與本線的 `stripInlineHtml` 並存，node 測試全過；`tools\dev_check.ps1` 綠 | Codex | `docs/DECISIONS.md:362` |

## 刻意不做

| 不做什麼 | 理由 | 什麼情況下重新考慮 |
| --- | --- | --- |
| 單獨摘取未合併的上游 PR | 未合併 PR 可能在審查中改寫；例外只限本線已確認存在缺陷的項目（如已採用的 #563、#573） | 缺陷在本線實際造成損害，且上游長期不動 |
| 把 hook 的 bash 測試納入 `tools\dev_check.ps1` | Windows 本機以 bash 腳本為主，CI 已跑（接續開發報告 2026-10-25） | CI 缺席，或 hook 測試開始只在 Windows 出錯 |
| 對上游開 PR／回貢 | 預設只打 `SanHsien/` 名下 repo | 維護者在新的對話中明確要求回貢 |

## 維護方式

fork：以 `Upstream check` workflow 為訊號（failure＝上游有新 PR／commit／issue 未審），三軸（commit、PR、issue）水位分開推進，審完在 `docs/DECISIONS.md` 記理由。直接推 `main`；Dependabot 只開 PR，CI 綠且讀完 diff 才合併。本機跑 `tools\dev_check.ps1` 約需 10 分鐘以上，逾時是未完成不是失敗。
