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

Write-Host "WINDOWS DEV CHECK GREEN"
