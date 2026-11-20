[CmdletBinding()]
param(
    [Parameter(Mandatory = $true, Position = 0)]
    [ValidateNotNullOrEmpty()]
    [string]$ReportPath,

    [switch]$RequirePass
)

$ErrorActionPreference = "Stop"

if (-not (Test-Path -LiteralPath $ReportPath -PathType Leaf)) {
    throw "Relatório de aceitação não encontrado: $ReportPath"
}

$resolvedReportPath = (Resolve-Path -LiteralPath $ReportPath).Path
try {
    $report = Get-Content -LiteralPath $resolvedReportPath -Raw | ConvertFrom-Json
}
catch {
    throw "O relatório não contém JSON válido: $($_.Exception.Message)"
}

function Assert-ReportProperty {
    param(
        [Parameter(Mandatory = $true)]$Object,
        [Parameter(Mandatory = $true)][string]$Name
    )
    if ($null -eq $Object -or $Object.PSObject.Properties.Name -notcontains $Name) {
        throw "Campo obrigatório ausente no relatório: $Name"
    }
}

$requiredTopLevel = @(
    "schema_version", "product", "application_version", "recorded_at_utc",
    "overall_result", "totals", "environment", "cases"
)
foreach ($propertyName in $requiredTopLevel) {
    Assert-ReportProperty -Object $report -Name $propertyName
}

if ([int]$report.schema_version -ne 1) {
    throw "Versão de schema não suportada: $($report.schema_version)"
}
if ($report.product -ne "ECU Pro Tune") {
    throw "O relatório pertence a outro produto."
}
if ([string]$report.application_version -notmatch '^\d+\.\d+\.\d+$') {
    throw "Versão da aplicação inválida."
}

$recordedAt = [DateTimeOffset]::MinValue
if (-not [DateTimeOffset]::TryParse(
    [string]$report.recorded_at_utc,
    [Globalization.CultureInfo]::InvariantCulture,
    [Globalization.DateTimeStyles]::RoundtripKind,
    [ref]$recordedAt
)) {
    throw "recorded_at_utc não contém uma data ISO 8601 válida."
}
if ($recordedAt.Offset -ne [TimeSpan]::Zero) {
    throw "recorded_at_utc tem de estar em UTC."
}

$expectedCases = @(
    @{ id = 1; title = "Instalação limpa" },
    @{ id = 2; title = "Virtual environment incompatível" },
    @{ id = 3; title = "FFmpeg ausente" },
    @{ id = 4; title = "Arranque e versão" },
    @{ id = 5; title = "Dashboard" },
    @{ id = 6; title = "Navegação" },
    @{ id = 7; title = "Validação de perfil e mapa" },
    @{ id = 8; title = "Backup e restauro" },
    @{ id = 9; title = "Launcher de testes" },
    @{ id = 10; title = "Build local" },
    @{ id = 11; title = "Metadados do EXE" },
    @{ id = 12; title = "Extração do ZIP" },
    @{ id = 13; title = "Integridade da release" },
    @{ id = 14; title = "Fronteira de segurança" }
)

if ($report.cases -isnot [array] -or $report.cases.Count -ne $expectedCases.Count) {
    throw "O relatório tem de conter exatamente 14 casos."
}

$allowedResults = @("PASS", "FAIL", "SKIP")
$seenIds = @{}
$passed = 0
$failed = 0
$skipped = 0

foreach ($case in $report.cases) {
    foreach ($propertyName in @("id", "title", "result", "notes")) {
        Assert-ReportProperty -Object $case -Name $propertyName
    }

    $caseId = [int]$case.id
    if ($caseId -lt 1 -or $caseId -gt $expectedCases.Count) {
        throw "ID de caso fora do intervalo permitido: $caseId"
    }
    if ($seenIds.ContainsKey($caseId)) {
        throw "ID de caso duplicado: $caseId"
    }
    $seenIds[$caseId] = $true

    $expected = $expectedCases[$caseId - 1]
    if ([string]$case.title -cne $expected.title) {
        throw "Título inesperado para o caso $caseId."
    }

    $result = [string]$case.result
    if ($result -cnotin $allowedResults) {
        throw "Resultado inválido no caso ${caseId}: $result"
    }
    if ($null -eq $case.notes) {
        throw "O campo notes tem de existir no caso $caseId."
    }

    switch ($result) {
        "PASS" { $passed++ }
        "FAIL" { $failed++ }
        "SKIP" { $skipped++ }
    }
}

foreach ($propertyName in @("total", "passed", "failed", "skipped")) {
    Assert-ReportProperty -Object $report.totals -Name $propertyName
}
if ([int]$report.totals.total -ne $expectedCases.Count -or
    [int]$report.totals.passed -ne $passed -or
    [int]$report.totals.failed -ne $failed -or
    [int]$report.totals.skipped -ne $skipped) {
    throw "Os totais do relatório não correspondem aos resultados dos 14 casos."
}

foreach ($propertyName in @(
    "os_caption", "os_version", "os_build", "os_architecture",
    "powershell_version", "python_311"
)) {
    Assert-ReportProperty -Object $report.environment -Name $propertyName
    if ([string]::IsNullOrWhiteSpace([string]$report.environment.$propertyName)) {
        throw "Informação de ambiente vazia: $propertyName"
    }
}

$expectedOverall = if ($failed -gt 0) {
    "FAIL"
}
elseif ($skipped -gt 0) {
    "INCOMPLETE"
}
else {
    "PASS"
}

if ([string]$report.overall_result -cne $expectedOverall) {
    throw "Resultado global inconsistente. Esperado: $expectedOverall."
}

Write-Host "Relatório de aceitação estruturalmente válido."
Write-Host "Produto: $($report.product) v$($report.application_version)"
Write-Host "Resultado: $expectedOverall | PASS: $passed | FAIL: $failed | SKIP: $skipped"
Write-Host "Ficheiro: $resolvedReportPath"

if ($RequirePass -and $expectedOverall -ne "PASS") {
    Write-Error "A aceitação não está completa. O gate exige os 14 casos em PASS."
    exit 2
}
