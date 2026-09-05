<div align="center">

# Agent Skills

### 給 AI 編碼 Agent 的工程紀律技能包：spec、規劃、TDD、review 到上線

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](./LICENSE)
[![Platform: Claude Code](https://img.shields.io/badge/Platform-Claude%20Code-f97316.svg)](https://code.claude.com/)
[![Platform: Codex](https://img.shields.io/badge/Platform-Codex-10a37f.svg)](https://developers.openai.com/codex/skills)
[![Platform: Cursor](https://img.shields.io/badge/Platform-Cursor-000000.svg)](https://cursor.com/)
[![CI](https://github.com/SanHsien/agent-skills/actions/workflows/ci.yml/badge.svg)](https://github.com/SanHsien/agent-skills/actions/workflows/ci.yml)

<p>
  <a href="README.md"><strong>繁體中文</strong></a> ·
  <a href="README.en.md">English</a>
</p>

</div>

> **這是 [`addyosmani/agent-skills`](https://github.com/addyosmani/agent-skills) 的
> Windows-first 維護型 fork**，沿用 MIT 授權與完整 Git 歷史。產品 Skills、Commands、
> Agent Persona 與各宿主整合跟隨上游；本維護線補上繁中入口、Windows 開發／驗收 gate，以及
> 逐筆審查的上游追蹤。差異見 [`FORK.md`](FORK.md)，同步策略見 [`docs/UPSTREAM.md`](docs/UPSTREAM.md)。

給資深工程師用的 Agent Skills：把寫軟體時該遵守的工作流程、品質關卡與最佳實踐，包裝成 AI
編碼 Agent 能穩定照做的指令與腳本。相容 [Agent Skills 規格](https://agentskills.io)，可在
Claude Code、OpenAI Codex、Cursor、Windsurf、Gemini CLI、OpenCode、GitHub Copilot、Antigravity
CLI、Command Code、Kiro 等宿主使用。

## Slash Commands

9 個對應開發生命週期的 slash command，各自自動觸發對應的 skill：

| 情境 | Command | 核心原則 |
|------|---------|---------|
| 定義要做什麼 | `/spec` | 先寫 spec 再寫程式 |
| 規劃怎麼做 | `/plan` | 拆成小而原子的任務 |
| 逐步實作 | `/build` | 一次一個薄切片 |
| 證明可行 | `/test` | 測試就是證據 |
| 定品質底線 | `/constraints` | 決定一次、處處落實 |
| 合併前 review | `/review` | 提升程式碼健康度 |
| 稽核網頁效能 | `/webperf` | 先量測再優化 |
| 簡化程式碼 | `/code-simplify` | 清晰勝過取巧 |
| 上線 | `/ship` | 快即是穩 |

`/build auto` 會在你核准一次 plan 後自動產生任務並逐一實作——拿掉的是人在每個任務之間手動確認
的步驟，不是驗證本身：每個任務仍是 test-driven 並個別提交，遇到失敗或高風險步驟會暫停。

除了 slash command，Agent 也會依當下任務自動觸發對應 skill——設計 API 時觸發
`api-and-interface-design`、寫 UI 時觸發 `frontend-ui-engineering`，以此類推。

## 安裝

### 選項 1：Claude Code（推薦）

**Marketplace 安裝：**

```text
/plugin marketplace add SanHsien/agent-skills
/plugin install agent-skills@addy-agent-skills
```

**本機開發模式：**

```powershell
git clone https://github.com/SanHsien/agent-skills.git
claude --plugin-dir C:\path\to\agent-skills
```

### 選項 2：Codex

```bash
codex plugin marketplace add SanHsien/agent-skills
codex plugin add agent-skills@agent-skills
```

Codex 透過根目錄的 `.codex-plugin/plugin.json` 直接讀 `skills/`。安裝後在對話中用 `@` 呼叫
skill（例如 `@spec-driven-development`）。

### 選項 3：Cursor

把工作流程 skill 放到 `.cursor/skills/`（從本 repo 的 `skills/` 同步），短版政策放
`.cursor/rules/*.mdc`——不要把整份 skill 貼進 rules。詳見
[docs/cursor-setup.md](docs/cursor-setup.md)。

### 其他宿主

Gemini CLI、Windsurf、OpenCode、GitHub Copilot、Antigravity CLI、Command Code、Kiro 的原生安裝
方式，以及沒有原生整合時的通用做法，見英文版
[README.en.md 的 Quick Start 章節](README.en.md#quick-start)，以及對應的宿主設定文件：
[gemini-cli-setup.md](docs/gemini-cli-setup.md)、
[windsurf-setup.md](docs/windsurf-setup.md)、[opencode-setup.md](docs/opencode-setup.md)、
[copilot-setup.md](docs/copilot-setup.md)、[copilot-cli-setup.md](docs/copilot-cli-setup.md)、
[antigravity-setup.md](docs/antigravity-setup.md)、
[commandcode-setup.md](docs/commandcode-setup.md)。這些是上游文件，本 fork 不重寫安裝指令。

### 只想裝單一 skill

用開放的 [skills CLI](https://github.com/vercel-labs/skills)：

```bash
npx skills add SanHsien/agent-skills            # 安裝全部 25 個 skill
npx skills add SanHsien/agent-skills --skill code-review-and-quality
```

> 單獨安裝一個 skill 時，`npx` 只會複製 `skills/<name>/`，不含根目錄的 `references/`。skill
> 仍可運作，但共用 checklist 的路徑會失效；需要的話把該 checklist 複製進安裝後 skill 自己的
> `references/` 目錄。

## 全部 25 個 Skill（依生命週期分組）

Commands 是入口；完整清單依 [`CLAUDE.md`](CLAUDE.md) 的分組如下（24 個生命週期 skill +
`using-agent-skills` 這個判斷該用哪個 skill 的 meta-skill）：

- **Define（定義）**：`interview-me`、`idea-refine`、`spec-driven-development`、`constraint-driven-development`
- **Plan（規劃）**：`planning-and-task-breakdown`
- **Build（實作）**：`incremental-implementation`、`test-driven-development`、`context-engineering`、`source-driven-development`、`doubt-driven-development`、`frontend-ui-engineering`、`api-and-interface-design`
- **Verify（驗證）**：`browser-testing-with-devtools`、`debugging-and-error-recovery`
- **Review（審查）**：`code-review-and-quality`、`code-simplification`、`security-and-hardening`、`performance-optimization`
- **Ship（上線）**：`git-workflow-and-versioning`、`ci-cd-and-automation`、`deprecation-and-migration`、`documentation-and-adrs`、`observability-and-instrumentation`、`shipping-and-launch`
- **Meta**：`using-agent-skills`

每個 skill 的完整說明、觸發條件與依賴關係見 [README.en.md 的 skill 表](README.en.md#all-24-skills)
（英文，逐字對照上游），或直接讀 `skills/<name>/SKILL.md`。

## Agent Persona

4 個預先設定好角色的 subagent，供 `/review` 與 `/ship` 併發呼叫：`code-reviewer`（資深工程師視角
五軸 review）、`test-engineer`（測試策略與涵蓋率）、`security-auditor`（威脅建模與 OWASP）、
`web-performance-auditor`（Core Web Vitals 稽核，`/webperf` 呼叫）。決策矩陣與編排規則見
[docs/agents.md](docs/agents.md)。

## 本 fork 的維護

本 repo 是產品內容跟隨上游、維護骨架屬於這條線的疊加式 fork：

- [`FORK.md`](FORK.md) — 與上游的差異、分支策略、換電腦怎麼開發
- [`docs/DEVELOPMENT.md`](docs/DEVELOPMENT.md) — 本機開發、Windows canonical gate、工具設定
- [`docs/UPSTREAM.md`](docs/UPSTREAM.md) — 上游 remote、審查清冊、水位推進流程
- [`docs/DECISIONS.md`](docs/DECISIONS.md) — 逐筆維護決策與理由
- [`CHANGELOG.md`](CHANGELOG.md) — 本 fork 的維護歷史（不含上游產品演進）

Windows 一鍵驗收：

```powershell
git clone https://github.com/SanHsien/agent-skills.git
cd agent-skills
python -m venv .venv
.venv\Scripts\python -m pip install --upgrade pip
.venv\Scripts\python -m pip install -r requirements-dev.txt
pwsh -NoProfile -File tools\dev_check.ps1
```

## 來源與授權

本倉庫 fork 自 [`addyosmani/agent-skills`](https://github.com/addyosmani/agent-skills)，沿用
MIT License。Skills、Commands、Agent Persona、Hooks、References、Evals 與 plugin manifest 為
上游原作。完整標示見 [`LICENSE`](LICENSE) 與 [`NOTICE.md`](NOTICE.md)。
