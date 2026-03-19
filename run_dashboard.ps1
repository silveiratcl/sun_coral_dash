$ErrorActionPreference = "Stop"

$repoRoot = Split-Path -Parent $MyInvocation.MyCommand.Path
$pythonExe = Join-Path $repoRoot ".venv\Scripts\python.exe"
$checkScript = Join-Path $repoRoot "scripts\check_env.py"
$appScript = Join-Path $repoRoot "cs_index.py"

if (-not (Test-Path $pythonExe)) {
    Write-Error "Project virtual environment not found at .venv\Scripts\python.exe"
    exit 2
}

if (-not (Test-Path $checkScript)) {
    Write-Error "Environment check script not found: scripts\check_env.py"
    exit 2
}

Push-Location $repoRoot
try {
    & $pythonExe $checkScript
    if ($LASTEXITCODE -ne 0) {
        exit $LASTEXITCODE
    }

    & $pythonExe $appScript
    exit $LASTEXITCODE
}
finally {
    Pop-Location
}
