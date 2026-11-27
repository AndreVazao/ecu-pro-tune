[CmdletBinding()]
param(
    [string]$OutputDirectory = "reports\acceptance"
)

$ErrorActionPreference = "Stop"
$repositoryRoot = (Resolve-Path (Join-Path $PSScriptRoot "..")).Path
if (-not [System.IO.Path]::IsPathRooted($OutputDirectory)) {
    $OutputDirectory = Join-Path $repositoryRoot $OutputDirectory
}

$versionPath = Join-Path $repositoryRoot "VERSION"
if (-not (Test-Path -LiteralPath $versionPath -PathType Leaf)) {
    throw "VERSION não encontrado. Executa o script a partir de um checkout completo do ECU Pro Tune."
}
$applicationVersion = (Get-Content -LiteralPath $versionPath -Raw).Trim()
if ($applicationVersion -notmatch '^\d+\.\d+\.\d+$') {
    throw "O ficheiro VERSION contém uma versão inválida."
}

$cases = @(
    @{ id = 1; title = "Instalação limpa"; detail = "Executar install_ecu_pro_tune.bat sem .venv existente." },
    @{ id = 2; title = "Virtual environment incompatível"; detail = "Confirmar que um .venv de outra versão Python é rejeitado sem ser apagado." },
    @{ id = 3; title = "FFmpeg ausente"; detail = "Confirmar instalação e GUI funcionais sem FFmpeg." },
    @{ id = 4; title = "Arranque e versão"; detail = "Abrir a aplicação e confirmar o título v$applicationVersion." },
    @{ id = 5; title = "Dashboard"; detail = "Executar e parar a simulação repetidamente." },
    @{ id = 6; title = "Navegação"; detail = "Navegar entre Dashboard, Perfis e Mapas." },
    @{ id = 7; title = "Validação de perfil e mapa"; detail = "Testar valores válidos e inválidos no mapa." },
    @{ id = 8; title = "Backup e restauro"; detail = "Criar backup, alterar perfil e restaurar." },
    @{ id = 9; title = "Launcher de testes"; detail = "Executar ecu_test.bat." },
    @{ id = 10; title = "Build local"; detail = "Executar build_exe.bat e confirmar que outros conteúdos de dist são preservados." },
    @{ id = 11; title = "Metadados do EXE"; detail = "Confirmar FileVersion e ProductVersion iguais a $applicationVersion.0." },
    @{ id = 12; title = "Extração do ZIP"; detail = "Extrair para um caminho com espaços e iniciar ECUProTune.exe." },
    @{ id = 13; title = "Integridade da release"; detail = "Comparar SHA256SUMS.txt com BUILD-MANIFEST.json e o ZIP." },
    @{ id = 14; title = "Fronteira de segurança"; detail = "Confirmar que não existe escrita física ECU, flash ou programação hardware." },
    @{ id = 15; title = "Scheduler GUI (simulação)"; detail = "Criar agendamento futuro, confirmar PENDENTE, cancelar e confirmar remoção; verificar callback apenas simulado." }
)

$os = Get-CimInstance -ClassName Win32_OperatingSystem
$python311 = "Python Launcher não encontrado"
if (Get-Command py -ErrorAction SilentlyContinue) {
    $pythonOutput = & py -3.11 --version 2>&1
    if ($LASTEXITCODE -eq 0) {
        $python311 = ($pythonOutput | Out-String).Trim()
    }
    else {
        $python311 = "Python 3.11 não disponível através de py -3.11"
    }
}

Write-Host ""
Write-Host "ECU Pro Tune v$applicationVersion — registo de aceitação Windows"
Write-Host "Sistema: $($os.Caption) | Build $($os.BuildNumber) | $([System.Runtime.InteropServices.RuntimeInformation]::OSArchitecture)"
Write-Host "Python: $python311"
Write-Host "Regista o resultado real de cada caso. Não marques PASS sem o executar."
Write-Host ""

$results = foreach ($case in $cases) {
    Write-Host ""
    Write-Host "[$($case.id)/$($cases.Count)] $($case.title)"
    Write-Host $case.detail
    do {
        $result = (Read-Host "Resultado (PASS/FAIL/SKIP)").Trim().ToUpperInvariant()
        if ($result -notin @("PASS", "FAIL", "SKIP")) {
            Write-Host "Valor inválido. Usa PASS, FAIL ou SKIP."
        }
    } while ($result -notin @("PASS", "FAIL", "SKIP"))

    $notes = Read-Host "Notas ou evidência (opcional)"
    [PSCustomObject]@{
        id = $case.id
        title = $case.title
        result = $result
        notes = $notes
    }
}

$failed = @($results | Where-Object { $_.result -eq "FAIL" }).Count
$skipped = @($results | Where-Object { $_.result -eq "SKIP" }).Count
$overall = if ($failed -gt 0) { "FAIL" } elseif ($skipped -gt 0) { "INCOMPLETE" } else { "PASS" }

$report = [ordered]@{
    schema_version = 1
    product = "ECU Pro Tune"
    application_version = $applicationVersion
    recorded_at_utc = (Get-Date).ToUniversalTime().ToString("o")
    overall_result = $overall
    totals = [ordered]@{
        total = $results.Count
        passed = @($results | Where-Object { $_.result -eq "PASS" }).Count
        failed = $failed
        skipped = $skipped
    }
    environment = [ordered]@{
        os_caption = $os.Caption
        os_version = $os.Version
        os_build = $os.BuildNumber
        os_architecture = [System.Runtime.InteropServices.RuntimeInformation]::OSArchitecture.ToString()
        powershell_version = $PSVersionTable.PSVersion.ToString()
        python_311 = $python311
    }
    cases = @($results)
}

New-Item -ItemType Directory -Path $OutputDirectory -Force | Out-Null
$timestamp = (Get-Date).ToUniversalTime().ToString("yyyyMMdd-HHmmss-fff")
$reportPath = Join-Path $OutputDirectory "ECUProTune-Acceptance-$timestamp.json"
$suffix = 1
while (Test-Path -LiteralPath $reportPath) {
    $reportPath = Join-Path $OutputDirectory "ECUProTune-Acceptance-$timestamp-$('{0:D3}' -f $suffix).json"
    $suffix++
}
$report | ConvertTo-Json -Depth 6 | Set-Content -LiteralPath $reportPath -Encoding UTF8

Write-Host ""
Write-Host "Resultado global: $overall"
Write-Host "PASS: $($report.totals.passed) | FAIL: $failed | SKIP: $skipped"
Write-Host "Relatório: $reportPath"
if ($overall -ne "PASS") {
    Write-Warning "A aceitação não está completa. Corrige falhas e executa os casos em falta antes de declarar a release aceite."
}
