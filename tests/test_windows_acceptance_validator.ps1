$ErrorActionPreference = "Stop"

$repositoryRoot = (Resolve-Path (Join-Path $PSScriptRoot "..")).Path
$validatorPath = Join-Path $repositoryRoot "scripts\validate_windows_acceptance.ps1"
$pwshPath = Join-Path $PSHOME "pwsh.exe"

$scriptPaths = @(
    (Join-Path $repositoryRoot "scripts\record_windows_acceptance.ps1"),
    $validatorPath,
    (Join-Path $repositoryRoot "scripts\check_release_readiness.ps1"),
    (Join-Path $repositoryRoot "scripts\verify_release.ps1"),
    (Join-Path $repositoryRoot "scripts\package_release.ps1")
)

foreach ($scriptPath in $scriptPaths) {
    if (-not (Test-Path -LiteralPath $scriptPath -PathType Leaf)) {
        throw "PowerShell script not found: $scriptPath"
    }

    $tokens = $null
    $parseErrors = $null
    [System.Management.Automation.Language.Parser]::ParseFile(
        $scriptPath,
        [ref]$tokens,
        [ref]$parseErrors
    ) | Out-Null

    if ($parseErrors.Count -gt 0) {
        $details = ($parseErrors | ForEach-Object { $_.Message }) -join "; "
        throw "PowerShell parse failed for $scriptPath : $details"
    }
}

$caseTitles = @(
    "Instalação limpa",
    "Virtual environment incompatível",
    "FFmpeg ausente",
    "Arranque e versão",
    "Dashboard",
    "Navegação",
    "Validação de perfil e mapa",
    "Backup e restauro",
    "Launcher de testes",
    "Build local",
    "Metadados do EXE",
    "Extração do ZIP",
    "Integridade da release",
    "Fronteira de segurança",
    "Scheduler GUI (simulação)"
)

$cases = for ($index = 0; $index -lt $caseTitles.Count; $index++) {
    [ordered]@{
        id = $index + 1
        title = $caseTitles[$index]
        result = "PASS"
        notes = "Synthetic CI fixture; not a real user-machine acceptance result."
    }
}

$validReport = [ordered]@{
    schema_version = 1
    product = "ECU Pro Tune"
    application_version = "0.1.0"
    recorded_at_utc = (Get-Date).ToUniversalTime().ToString("o")
    overall_result = "PASS"
    totals = [ordered]@{
        total = 15
        passed = 15
        failed = 0
        skipped = 0
    }
    environment = [ordered]@{
        os_caption = "Windows CI synthetic fixture"
        os_version = "10.0"
        os_build = "20348"
        os_architecture = "X64"
        powershell_version = $PSVersionTable.PSVersion.ToString()
        python_311 = "Python 3.11 CI fixture"
    }
    cases = @($cases)
}

$tempDirectory = Join-Path ([System.IO.Path]::GetTempPath()) ("ecu-acceptance-validator-" + [guid]::NewGuid().ToString("N"))
New-Item -ItemType Directory -Path $tempDirectory -Force | Out-Null

function Write-Fixture {
    param(
        [Parameter(Mandatory = $true)]$Report,
        [Parameter(Mandatory = $true)][string]$Path
    )
    $Report | ConvertTo-Json -Depth 8 | Set-Content -LiteralPath $Path -Encoding utf8
}

function Invoke-ValidatorProcess {
    param(
        [Parameter(Mandatory = $true)][string]$Path,
        [switch]$RequirePass
    )

    $argumentLine = '-NoProfile -File "{0}" -ReportPath "{1}"' -f $validatorPath, $Path
    if ($RequirePass) {
        $argumentLine += " -RequirePass"
    }

    $process = Start-Process -FilePath $pwshPath -ArgumentList $argumentLine -NoNewWindow -Wait -PassThru
    return $process.ExitCode
}

try {
    $validPath = Join-Path $tempDirectory "valid-pass.json"
    Write-Fixture -Report $validReport -Path $validPath
    $validExit = Invoke-ValidatorProcess -Path $validPath -RequirePass
    if ($validExit -ne 0) {
        throw "A valid 15/15 PASS report was rejected (exit $validExit)."
    }
    Write-Host "PASS: valid 15/15 report accepted with -RequirePass."

    $incompleteReport = $validReport | ConvertTo-Json -Depth 8 | ConvertFrom-Json
    $incompleteReport.cases[14].result = "SKIP"
    $incompleteReport.totals.passed = 14
    $incompleteReport.totals.skipped = 1
    $incompleteReport.overall_result = "INCOMPLETE"
    $incompletePath = Join-Path $tempDirectory "incomplete.json"
    Write-Fixture -Report $incompleteReport -Path $incompletePath

    $incompleteExit = Invoke-ValidatorProcess -Path $incompletePath
    if ($incompleteExit -ne 0) {
        throw "A structurally valid INCOMPLETE report was rejected without -RequirePass."
    }

    $incompleteGateExit = Invoke-ValidatorProcess -Path $incompletePath -RequirePass
    if ($incompleteGateExit -eq 0) {
        throw "The -RequirePass gate accepted an INCOMPLETE report."
    }
    Write-Host "PASS: INCOMPLETE report is valid, but -RequirePass rejects it."

    $duplicateReport = $validReport | ConvertTo-Json -Depth 8 | ConvertFrom-Json
    $duplicateReport.cases[13].id = 13
    $duplicatePath = Join-Path $tempDirectory "duplicate-id.json"
    Write-Fixture -Report $duplicateReport -Path $duplicatePath

    $duplicateExit = Invoke-ValidatorProcess -Path $duplicatePath
    if ($duplicateExit -eq 0) {
        throw "The validator accepted a report with duplicate case IDs."
    }
    Write-Host "PASS: duplicate case IDs are rejected."

    $totalsReport = $validReport | ConvertTo-Json -Depth 8 | ConvertFrom-Json
    $totalsReport.totals.passed = 13
    $totalsPath = Join-Path $tempDirectory "incorrect-totals.json"
    Write-Fixture -Report $totalsReport -Path $totalsPath

    $totalsExit = Invoke-ValidatorProcess -Path $totalsPath
    if ($totalsExit -eq 0) {
        throw "The validator accepted inconsistent totals."
    }
    Write-Host "PASS: inconsistent totals are rejected."
}
finally {
    if (Test-Path -LiteralPath $tempDirectory) {
        Remove-Item -LiteralPath $tempDirectory -Recurse -Force
    }
}

Write-Host "PowerShell parser and acceptance validator integration tests: PASS."
