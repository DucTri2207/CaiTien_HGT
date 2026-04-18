$ErrorActionPreference = "Stop"

$scriptDir = Split-Path -Parent $MyInvocation.MyCommand.Path
Set-Location $scriptDir

$rootEnvPython = Join-Path (Split-Path $scriptDir -Parent) ".venv-amdgt\Scripts\python.exe"
$localEnvPython = Join-Path $scriptDir ".venv\Scripts\python.exe"

if (Test-Path $rootEnvPython) {
    $pythonExe = $rootEnvPython
} elseif (Test-Path $localEnvPython) {
    $pythonExe = $localEnvPython
} else {
    throw "Khong tim thay Python env. Hay tao .venv-amdgt hoac ductri_hgt_update\\.venv truoc."
}

$defaultArgs = @(
    "train_DDA.py",
    "--epochs", "1000",
    "--k_fold", "10",
    "--neighbor", "20",
    "--lr", "0.0005",
    "--weight_decay", "0.0001",
    "--hgt_layer", "3",
    "--hgt_in_dim", "128",
    "--dataset", "C-dataset",
    "--eval_every", "1",
    "--early_stop_metric", "auc"
)

if ($args.Count -gt 0) {
    $defaultArgs += $args
}

Write-Host "Using Python:" $pythonExe
Write-Host "Working directory:" $scriptDir
Write-Host "Command:" $pythonExe ($defaultArgs -join " ")

& $pythonExe @defaultArgs
