# 安全政策

## 支援範圍

安全修正以本 fork 的最新 `main` 為主；上游版本的問題也會視需要回報原作者。

## 私下回報

請使用 GitHub Security Advisories 的 **Report a vulnerability** 私下回報。若該入口不可用，
請透過 GitHub 個人檔案聯絡維護者，不要先建立公開 Issue。

回報請包含影響範圍、重現步驟、受影響版本與最小必要證據。請勿附上真實 API key、憑證，
或客戶專案內容。

## 特別注意

- 產品 skill 與 slash command 可能引導 Agent 呼叫外部工具或 MCP 伺服器。憑證只存在使用者本機；不要提交 `.env`。
- 本 fork 不代為保管任何第三方服務帳號或 API key。
- `skills/`、`commands/`、`agents/`、`hooks/`、`scripts/` 是上游零依賴內容。發現安全問題時，優先回報上游；本線只在 Windows 可重現的崩潰才加最小修正。
