$ErrorActionPreference = "Stop"

$repoRoot = Split-Path -Parent (Split-Path -Parent $MyInvocation.MyCommand.Path)
$pythonExe = Join-Path $repoRoot ".venv\Scripts\python.exe"
$requirementsFile = Join-Path $repoRoot "requirements.txt"
$checkScript = Join-Path $repoRoot "scripts\check_env.py"

if (-not (Test-Path $pythonExe)) {
    Write-Error "Project virtual environment not found at .venv\Scripts\python.exe"
    exit 2
}

Push-Location $repoRoot
try {
    & $pythonExe -m pip freeze | Sort-Object | Set-Content -Path $requirementsFile -Encoding Ascii

    & $pythonExe $checkScript
    if ($LASTEXITCODE -ne 0) {
        Write-Error "requirements.txt was generated but validation failed."
        exit $LASTEXITCODE
    }

    Write-Host "requirements.txt frozen and validated successfully."
}
finally {
    Pop-Location
}
