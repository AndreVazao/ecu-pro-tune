[CmdletBinding()]
param(
    [string]$ReleaseDirectory = "release"
)

$ErrorActionPreference = "Stop"
$repositoryRoot = (Resolve-Path (Join-Path $PSScriptRoot "..")).Path

if (-not [System.IO.Path]::IsPathRooted($ReleaseDirectory)) {
    $ReleaseDirectory = Join-Path $repositoryRoot $ReleaseDirectory
}
$releaseRoot = (Resolve-Path -LiteralPath $ReleaseDirectory).Path

$manifestPath = Join-Path $releaseRoot "BUILD-MANIFEST.json"
$checksumsPath = Join-Path $releaseRoot "SHA256SUMS.txt"

foreach ($requiredFile in @($manifestPath, $checksumsPath)) {
    if (-not (Test-Path -LiteralPath $requiredFile -PathType Leaf)) {
        throw "Ficheiro obrigatório em falta: $requiredFile"
    }
}

$manifest = Get-Content -LiteralPath $manifestPath -Raw | ConvertFrom-Json
if ($manifest.product -ne "ECU Pro Tune") {
    throw "Produto inesperado no manifesto."
}
if ($manifest.platform -ne "Windows x64" -or $manifest.python -ne "3.11") {
    throw "Plataforma ou versão Python inesperada no manifesto."
}
if ($manifest.packaging -ne "PyInstaller onedir") {
    throw "Formato de empacotamento inesperado."
}
if ($manifest.version -notmatch '^\d+\.\d+\.\d+$') {
    throw "Versão semântica inválida no manifesto."
}
if ($manifest.windows_file_version -ne "$($manifest.version).0") {
    throw "Windows FileVersion não corresponde à versão do produto."
}
if ($manifest.archive -ne "ECUProTune-Windows-Python311-v$($manifest.version).zip") {
    throw "Nome do arquivo ZIP não corresponde à versão declarada."
}
if ([System.IO.Path]::GetFileName($manifest.archive) -ne $manifest.archive) {
    throw "O nome do ZIP no manifesto não pode conter caminhos."
}
if ($manifest.sha256 -notmatch '^[0-9a-f]{64}$') {
    throw "SHA-256 inválido no manifesto."
}
if ([long]$manifest.archive_size_bytes -le 0) {
    throw "Tamanho do ZIP inválido no manifesto."
}

$archivePath = Join-Path $releaseRoot $manifest.archive
if (-not (Test-Path -LiteralPath $archivePath -PathType Leaf)) {
    throw "ZIP de release não encontrado: $archivePath"
}

$archiveItem = Get-Item -LiteralPath $archivePath
if ($archiveItem.Length -ne [long]$manifest.archive_size_bytes) {
    throw "O tamanho do ZIP não corresponde ao manifesto."
}

$actualHash = (Get-FileHash -LiteralPath $archivePath -Algorithm SHA256).Hash.ToLowerInvariant()
if ($actualHash -ne $manifest.sha256) {
    throw "SHA-256 do ZIP não corresponde ao manifesto."
}

$checksumLine = (Get-Content -LiteralPath $checksumsPath -Raw).Trim()
$expectedChecksumLine = "$actualHash  $($manifest.archive)"
if ($checksumLine -ne $expectedChecksumLine) {
    throw "SHA256SUMS.txt não corresponde ao manifesto e ao ZIP."
}

Add-Type -AssemblyName System.IO.Compression
$zip = [System.IO.Compression.ZipFile]::OpenRead($archivePath)
try {
    $entryNames = @()
    $seenEntries = @{}
    foreach ($entry in $zip.Entries) {
        $entryName = $entry.FullName.Replace("\", "/")
        if ([string]::IsNullOrWhiteSpace($entryName) -or $entryName.StartsWith("/")) {
            throw "O ZIP contém um caminho vazio ou absoluto."
        }
        if ($entryName -match '^[A-Za-z]:' -or $entryName -match '(^|/)\.\.(/|$)' -or $entryName -match '(^|/)\.(/|$)') {
            throw "O ZIP contém um caminho inseguro: $entryName"
        }
        if ($entryName -notlike "ECUProTune/*") {
            throw "O ZIP contém conteúdo fora da pasta ECUProTune: $entryName"
        }
        if ($seenEntries.ContainsKey($entryName)) {
            throw "O ZIP contém entradas duplicadas: $entryName"
        }
        $seenEntries[$entryName] = $true
        $entryNames += $entryName
    }

    $executableEntry = $zip.GetEntry("ECUProTune/ECUProTune.exe")
    if ($null -eq $executableEntry -or $executableEntry.Length -le 0) {
        throw "O ZIP não contém um ECUProTune.exe válido."
    }

    $internalFiles = @($zip.Entries | Where-Object {
        $name = $_.FullName.Replace("\", "/")
        $name -like "ECUProTune/_internal/*" -and $_.Length -gt 0
    })
    if ($internalFiles.Count -eq 0) {
        throw "O ZIP não contém ficheiros PyInstaller válidos em _internal."
    }
}
finally {
    $zip.Dispose()
}

Write-Host "Release verificada com sucesso."
Write-Host "Versão: $($manifest.version) (Windows $($manifest.windows_file_version))"
Write-Host "ZIP: $($manifest.archive)"
Write-Host "Tamanho: $($archiveItem.Length) bytes"
Write-Host "SHA-256: $actualHash"
