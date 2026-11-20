[CmdletBinding()]
param(
    [string]$ReleaseDirectory = "release",

    [Parameter(Mandatory = $true)]
    [ValidateNotNullOrEmpty()]
    [string]$AcceptanceReport
)

$ErrorActionPreference = "Stop"
$repositoryRoot = (Resolve-Path (Join-Path $PSScriptRoot "..")).Path

function Resolve-ProjectPath {
    param([Parameter(Mandatory = $true)][string]$Path)

    if ([System.IO.Path]::IsPathRooted($Path)) {
        return $Path
    }
    return (Join-Path $repositoryRoot $Path)
}

$releasePath = Resolve-ProjectPath -Path $ReleaseDirectory
$reportPath = Resolve-ProjectPath -Path $AcceptanceReport

if (-not (Test-Path -LiteralPath $releasePath -PathType Container)) {
    throw "Diretório da release não encontrado: $releasePath"
}
if (-not (Test-Path -LiteralPath $reportPath -PathType Leaf)) {
    throw "Relatório de aceitação não encontrado: $reportPath"
}

$manifestPath = Join-Path $releasePath "BUILD-MANIFEST.json"
if (-not (Test-Path -LiteralPath $manifestPath -PathType Leaf)) {
    throw "BUILD-MANIFEST.json não encontrado na release."
}

try {
    $manifest = Get-Content -LiteralPath $manifestPath -Raw | ConvertFrom-Json
    $report = Get-Content -LiteralPath $reportPath -Raw | ConvertFrom-Json
}
catch {
    throw "Não foi possível ler o manifesto ou o relatório JSON: $($_.Exception.Message)"
}

if ($manifest.product -ne "ECU Pro Tune" -or $report.product -ne "ECU Pro Tune") {
    throw "Produto do manifesto ou do relatório não corresponde a ECU Pro Tune."
}
if ([string]$manifest.version -ne [string]$report.application_version) {
    throw "Versão do relatório ($($report.application_version)) não corresponde à release ($($manifest.version))."
}

$verifierPath = Join-Path $PSScriptRoot "verify_release.ps1"
$validatorPath = Join-Path $PSScriptRoot "validate_windows_acceptance.ps1"

if (-not (Test-Path -LiteralPath $verifierPath -PathType Leaf)) {
    throw "Verificador da release não encontrado: $verifierPath"
}
if (-not (Test-Path -LiteralPath $validatorPath -PathType Leaf)) {
    throw "Validador de aceitação não encontrado: $validatorPath"
}

Write-Host "A verificar integridade do pacote..."
& $verifierPath -ReleaseDirectory $releasePath

Write-Host "A validar aceitação manual 14/14..."
& $validatorPath -ReportPath $reportPath -RequirePass

Write-Host ""
Write-Host "RELEASE READY: pacote íntegro e aceitação manual 14/14 PASS."
Write-Host "Versão: $($manifest.version)"
Write-Host "Relatório: $reportPath"
