[CmdletBinding()]
param(
    [string]$SourceDirectory = "dist\ECUProTune",
    [string]$OutputDirectory = "release"
)

$ErrorActionPreference = "Stop"
$repositoryRoot = (Resolve-Path (Join-Path $PSScriptRoot "..")).Path

if (-not [System.IO.Path]::IsPathRooted($SourceDirectory)) {
    $SourceDirectory = Join-Path $repositoryRoot $SourceDirectory
}
if (-not [System.IO.Path]::IsPathRooted($OutputDirectory)) {
    $OutputDirectory = Join-Path $repositoryRoot $OutputDirectory
}

$source = (Resolve-Path -LiteralPath $SourceDirectory).Path
$executable = Join-Path $source "ECUProTune.exe"
$versionFile = Join-Path $repositoryRoot "VERSION"
$internalDirectory = Join-Path $source "_internal"

if (-not (Test-Path -LiteralPath $executable -PathType Leaf)) {
    throw "Executável não encontrado: $executable"
}
if (-not (Test-Path -LiteralPath $internalDirectory -PathType Container)) {
    throw "Diretório PyInstaller _internal não encontrado: $internalDirectory"
}
if (-not (Test-Path -LiteralPath $versionFile -PathType Leaf)) {
    throw "Ficheiro VERSION não encontrado: $versionFile"
}

$version = (Get-Content -LiteralPath $versionFile -Raw).Trim()
if ($version -notmatch '^\d+\.\d+\.\d+$') {
    throw "Versão inválida em VERSION: $version"
}

New-Item -ItemType Directory -Path $OutputDirectory -Force | Out-Null

$archiveName = "ECUProTune-Windows-Python311-v$version.zip"
$archivePath = Join-Path $OutputDirectory $archiveName
$manifestPath = Join-Path $OutputDirectory "BUILD-MANIFEST.json"
$checksumsPath = Join-Path $OutputDirectory "SHA256SUMS.txt"

if (Test-Path -LiteralPath $archivePath) {
    Remove-Item -LiteralPath $archivePath -Force
}

Compress-Archive -Path $source -DestinationPath $archivePath -CompressionLevel Optimal -Force

$archiveItem = Get-Item -LiteralPath $archivePath
$sha256 = (Get-FileHash -LiteralPath $archivePath -Algorithm SHA256).Hash.ToLowerInvariant()

$manifest = [ordered]@{
    product = "ECU Pro Tune"
    version = $version
    platform = "Windows x64"
    python = "3.11"
    packaging = "PyInstaller onedir"
    executable = "ECUProTune/ECUProTune.exe"
    archive = $archiveName
    archive_size_bytes = $archiveItem.Length
    sha256 = $sha256
    created_utc = (Get-Date).ToUniversalTime().ToString("o")
}

$manifest | ConvertTo-Json -Depth 4 | Set-Content -LiteralPath $manifestPath -Encoding UTF8
"$sha256  $archiveName" | Set-Content -LiteralPath $checksumsPath -Encoding ASCII

$verifiedHash = (Get-FileHash -LiteralPath $archivePath -Algorithm SHA256).Hash.ToLowerInvariant()
if ($verifiedHash -ne $sha256) {
    throw "Falha na verificação SHA-256 do pacote."
}

Write-Host "Pacote criado: $archivePath"
Write-Host "SHA-256: $sha256"
Write-Host "Manifesto: $manifestPath"
