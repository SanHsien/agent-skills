[CmdletBinding()]
param()

Set-StrictMode -Version Latest
$ErrorActionPreference = "Stop"

$repoRoot = Split-Path -Parent $PSScriptRoot
Set-Location -LiteralPath $repoRoot

$venvPython = Join-Path $repoRoot ".venv\Scripts\python.exe"
if (Test-Path -LiteralPath $venvPython) {
    $pythonExe = $venvPython
} else {
    $pythonExe = (Get-Command python -ErrorAction Stop).Source
}

$env:PYTHONUTF8 = "1"
$env:PYTHONIOENCODING = "utf-8"

function Invoke-Step {
    param(
        [Parameter(Mandatory)]
        [string]$Label,
        [Parameter(Mandatory)]
        [string]$Exe,
        [Parameter(Mandatory)]
        [string[]]$Arguments
    )

    Write-Host "==> $Label"
    & $Exe @Arguments
    if ($LASTEXITCODE -ne 0) {
        throw "$Label failed with exit code $LASTEXITCODE"
    }
}

$pythonTools = @(
    "tools\check_upstream_updates.py",
    "tools\check_dependency_freshness.py",
    "tools\check_links.py"
)

Invoke-Step -Label "Compile maintained Python" -Exe $pythonExe -Arguments (
    @("-m", "compileall", "-q", "tests") + $pythonTools
)
Invoke-Step -Label "Ruff (E9 + F)" -Exe $pythonExe -Arguments @(
    "-m", "ruff", "check", "--select", "E9,F", "--target-version", "py312",
    "tests", "tools\check_upstream_updates.py", "tools\check_dependency_freshness.py",
    "tools\check_links.py"
)
Invoke-Step -Label "Pytest" -Exe $pythonExe -Arguments @("-m", "pytest", "tests", "-q")

$nodeExe = (Get-Command node -ErrorAction Stop).Source
Invoke-Step -Label "Validate skills" -Exe $nodeExe -Arguments @("scripts\validate-skills.js")
Invoke-Step -Label "Validate commands" -Exe $nodeExe -Arguments @("scripts\validate-commands.js")

Invoke-Step -Label "Check Markdown links" -Exe $pythonExe -Arguments @(
    "tools\check_links.py"
)

function Invoke-SkillSpectorSelfScan {
    # Pre-publish self-scan: run the SkillSpector security scanner against every
    # skill this repo ships, the same way a downstream host would scan a
    # third-party skill before installing it. Ratchet, not one-time: new findings
    # (anything not already in .skillspector-baseline.yaml) fail this gate; they
    # must be reviewed and either fixed or added to the baseline with a specific
    # reason -- never rubber-stamped.
    #
    # Gate signal is the JSON report's `issues` array, not $LASTEXITCODE:
    # SkillSpector's exit code reflects an aggregate risk-score threshold (see its
    # docs/SUPPRESSION.md), not "any un-suppressed finding present", so relying on
    # exit code alone would silently let new LOW/MEDIUM findings through.
    param(
        [Parameter(Mandatory)]
        [string]$RepoRoot,
        [Parameter(Mandatory)]
        [string]$SkillsRoot
    )

    $skillSpectorCmd = Get-Command skillspector -ErrorAction SilentlyContinue
    if (-not $skillSpectorCmd) {
        Write-Host "==> SkillSpector self-scan (skipped: 'skillspector' not found on PATH)"
        return
    }

    $baselinePath = Join-Path $RepoRoot ".skillspector-baseline.yaml"
    if (-not (Test-Path -LiteralPath $baselinePath)) {
        throw ("Missing $baselinePath -- generate baseline entries with " +
            "'skillspector baseline skills\<name> --no-llm --reason ...' for every " +
            "skill under skills\ before this gate can run.")
    }

    $reportDir = Join-Path $RepoRoot ".skillspector-reports"
    New-Item -ItemType Directory -Force -Path $reportDir | Out-Null

    # Lift the scanner's time ceilings for the self-scan. They bound pathological
    # input, but a large file on slow storage sits close enough to them that machine
    # load decides whether the scan completes -- the same tree then passes or exits 2
    # depending on what else is running. A gate has to be reproducible, so here we buy
    # completeness with wall time.
    #
    # 86400 (one day), not 0. SKILLSPECTOR_MAX_WORKFLOW_SECONDS has been upstream's own
    # variable since SkillSpector 2.11.1, and upstream rejects 0, negatives and
    # non-finite values with a warning and falls back to its 600-second default -- so
    # "0" would silently mean 600 s. A large positive value means the same thing under
    # every build. SKILLSPECTOR_MAX_STATIC_SECONDS (per artifact, default 30 s) exists
    # only in the SanHsien fork and takes the same value; builds without it ignore it,
    # which is the previous behaviour rather than a silent weakening.
    $previousStaticBudget = $env:SKILLSPECTOR_MAX_STATIC_SECONDS
    $previousWorkflowBudget = $env:SKILLSPECTOR_MAX_WORKFLOW_SECONDS
    $env:SKILLSPECTOR_MAX_STATIC_SECONDS = "86400"
    # The graph-wide ceiling binds before the per-artifact one on a skill with
    # many files; lifting only one leaves the same load-dependent verdict.
    $env:SKILLSPECTOR_MAX_WORKFLOW_SECONDS = "86400"
    try {
    Write-Host "==> SkillSpector self-scan (skills\*)"
    $skillDirs = Get-ChildItem -LiteralPath $SkillsRoot -Directory
    $failedSkills = @()
    foreach ($skill in $skillDirs) {
        $reportPath = Join-Path $reportDir "$($skill.Name).json"
        & $skillSpectorCmd.Source scan $skill.FullName --no-llm --format json `
            --output $reportPath --baseline $baselinePath
        if ($LASTEXITCODE -ne 0 -and $LASTEXITCODE -ne 1) {
            throw ("skillspector scan crashed on skill '$($skill.Name)' " +
                "(exit code $LASTEXITCODE); see $reportPath")
        }
        $report = Get-Content -LiteralPath $reportPath -Raw | ConvertFrom-Json
        if ($report.issues.Count -gt 0) {
            $failedSkills += "$($skill.Name) ($($report.issues.Count) finding(s))"
        }
    }

    if ($failedSkills.Count -gt 0) {
        throw ("SkillSpector found new, un-baselined finding(s) in: " +
            "$($failedSkills -join '; '). Review the reports under $reportDir and " +
            "either fix the skill content or add a reviewed fingerprint/rule to " +
            ".skillspector-baseline.yaml with a specific reason -- do not rubber-stamp " +
            "CRITICAL or otherwise real findings into the baseline.")
    }

    Write-Host "SkillSpector self-scan: no new findings across $($skillDirs.Count) skill(s)."
    }
    finally {
        $env:SKILLSPECTOR_MAX_STATIC_SECONDS = $previousStaticBudget
        $env:SKILLSPECTOR_MAX_WORKFLOW_SECONDS = $previousWorkflowBudget
    }
}

Invoke-SkillSpectorSelfScan -RepoRoot $repoRoot -SkillsRoot (Join-Path $repoRoot "skills")

Write-Host "WINDOWS DEV CHECK GREEN"
