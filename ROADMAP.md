# 路線圖

> 本 repo 後續工作的單一真相源。做完一項，就在同一個 commit 刪掉那一列；新工作只加在這裡。
> 現況段的數字是 2026-10-30 依 `main` 查的快照，開工前先重查 GitHub。

## 現況

這是 addyosmani/agent-skills（AI coding agent 工程技能包）的 Windows-first 維護型 fork；在 GitHub 上它不是 fork 關係，但上游基線都指向該 repo（`tools/upstream_baseline.json`）。維護面健康：`main` 上 CI、CodeQL、Test Plugin Installation 最近一次皆 success；Upstream check 會因下列待審項目轉紅（`check_upstream_updates.py --strict` 實跑 exit 1），open PR 0 筆、Dependabot 與 Code scanning 告警 0 筆；issue 功能已停用，issue 數「未查到」不是 0（2026-10-29 `gh` 查詢）。commit 軸水位 `aeac41d4d005`（上游已發布 0.6.14 `eb07f19`，落後 70 commit 待同步）；issue 水位 717（上游最新已出現 #765 待審）；PR 水位已審至 752（#750 open，#751、#752 closed；上游最新已出現 #753–#766 尚未審）。

## 近期：可以直接動手

| 項目 | 為什麼 | 驗收方式 | 建議執行者 | 證據 |
| --- | --- | --- | --- | --- |
| 維護者決定是否授權升版到上游 0.6.13 | 本 fork 維持單一 tag／release（0.6.9），上游已到 0.6.13（commit `aeac41d` 已同步產品檔，但版本號沒採用）；升版需要刪舊 tag 與 release，屬維護者授權動作 | 在 `docs/DECISIONS.md` 記決定。若授權：五份 plugin manifest 版本一致、新 tag／release 存在、舊 tag 處理方式寫明、`validate-versions` 與 `tools\dev_check.ps1` 綠；若不授權：寫明理由並保留單一 tag 政策 | 維護者 | `docs/DECISIONS.md:290`；`gh release list -R SanHsien/agent-skills` |
| 審上游 0.6.14 commit 軸（`aeac41d..eb07f19`，落後 70 commit）、PR #753–#766、issue #765 | 審完 #752 時上游已再前進；不審的話 Upstream check 會一直紅，水位與實際脫節 | 逐項在 `docs/DECISIONS.md` 記採用／不採用與理由；`tools/upstream_baseline.json` 三軸水位推進；`python tools/check_upstream_updates.py --strict` exit 0；`tools\dev_check.ps1` 綠 | Antigravity | `python tools/check_upstream_updates.py --strict`（2026-10-30 exit 1）；`tools/upstream_baseline.json` |

## 中期：等條件成立再做

| 項目 | 觸發條件 | 驗收方式 | 建議執行者 | 證據 |
| --- | --- | --- | --- | --- |
| 上游合併 open PR 後同步（目前追蹤 #719–#752 中尚未合併者） | 任一筆被上游合併、commit 軸出現新 commit；依慣例未合併 PR 不單獨摘取 | 同步後，除繁中 `README.md` 與 5 份 plugin manifest 外，上游動到的檔案與 `upstream/main` 逐位元組一致；`reviewed_through` 推進；`tools\dev_check.ps1` 綠 | Claude Sonnet | `docs/DECISIONS.md:313-347`；`tools/upstream_baseline.json` |
| 同步 #749（指令檔加 `disable-model-invocation`）時逐行審 5 個被改寫的指令檔 | #749 被上游合併，或本線實際發生模型自行觸發 `/ship`、`/build auto`（此時提前只移植 9 個指令檔 frontmatter 那 9 行） | build／constraints／ship／spec／webperf 五檔逐行比對，確認未刪掉防護文字（每任務一個 commit、gitleaks `--redact`、`ship.md` 的預設平行 fan-out 句）；`tools\dev_check.ps1` 綠 | Claude Opus | `docs/DECISIONS.md` 2026-10-28 條目 |
| 提前採用 #729（`gitleaks detect` 洩漏 secret 值）與 issue #717 | #729 長期未被上游動，或本線 agent 日誌實際出現 secret 值 | `constraint-driven-development` 內不再有 `gitleaks detect` 而是 `--redact` 形式；`rg "gitleaks detect" skills` 無未遮蔽用法；`tools\dev_check.ps1` 綠 | Claude Sonnet | `docs/DECISIONS.md:320-324` |
| 採用 #748（percent-encoded 錨點驗證） | #748 被上游合併，或本線出現 `references/*.md#...%XX` 形式連結／CJK 標題錨點 | `validate-reference-links.js` 與本線的 `stripInlineHtml` 手動合併後 node 測試全過；`tools\dev_check.ps1` 綠 | Codex | `docs/DECISIONS.md:362` |

## 刻意不做

| 不做什麼 | 理由 | 什麼情況下重新考慮 |
| --- | --- | --- |
| 單獨摘取未合併的上游 PR | 未合併 PR 可能在審查中改寫；例外只限本線已確認存在缺陷的項目（如已採用的 #563、#573） | 缺陷在本線實際造成損害，且上游長期不動 |
| 採用上游版本號 bump（0.6.10–0.6.13） | 單一 tag 政策，升版需刪舊 tag（`docs/DECISIONS.md:290`） | 近期第二列的維護者決定為授權 |
| 把 hook 的 bash 測試納入 `tools\dev_check.ps1` | Windows 本機以 bash 腳本為主，CI 已跑（接續開發報告 2026-10-25） | CI 缺席，或 hook 測試開始只在 Windows 出錯 |
| 對上游開 PR／回貢 | 預設只打 `SanHsien/` 名下 repo | 維護者在新的對話中明確要求回貢 |

## 維護方式

fork：以 `Upstream check` workflow 為訊號（failure＝上游有新 PR／commit／issue 未審），三軸（commit、PR、issue）水位分開推進，審完在 `docs/DECISIONS.md` 記理由。直接推 `main`；Dependabot 只開 PR，CI 綠且讀完 diff 才合併。本機跑 `tools\dev_check.ps1` 約需 10 分鐘以上，逾時是未完成不是失敗。
