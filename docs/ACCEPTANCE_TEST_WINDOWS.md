# Windows manual acceptance plan — ECU Pro Tune 0.1.0

## Purpose

This plan covers the user-machine checks that GitHub Actions cannot fully replace. The automated Windows CI validates imports, tests, Tk construction, packaging and a short executable startup. It does not validate prolonged interactive use on every Windows installation.

## Test environment

- Windows 10 or Windows 11, x64.
- Python 3.11 x64 and Python Launcher.
- ECU Pro Tune repository checkout or the versioned release ZIP.
- No ECU hardware connection is required. Keep all checks in simulation mode.
- FFmpeg may be absent; it is optional.

## Acceptance cases

1. **Clean installation**
   - Start without an existing .venv.
   - Run install_ecu_pro_tune.bat.
   - Expected: Python 3.11 virtual environment created, dependencies installed, pip check passes, application imports validate.

2. **Incompatible existing virtual environment**
   - Use an existing .venv created with a Python version other than 3.11.
   - Run the installer.
   - Expected: clear error; existing .venv is not deleted or overwritten.

3. **FFmpeg absent**
   - Ensure FFmpeg is not on PATH and answer N to the optional winget prompt.
   - Expected: installation completes; GUI and WAV fallback audio remain functional.

4. **Application launch and version**
   - Launch with .venv\Scripts\python.exe -m src.app.main.
   - Expected: main window opens and title shows ECU Pro Tune v0.1.0.

5. **Dashboard simulation**
   - Start and stop the dashboard simulation several times.
   - Expected: RPM, boost, load, temperature, lambda, gauges and graph update while running and stop cleanly.
   - Expected: no physical ECU connection or write operation is attempted.

6. **Navigation**
   - Navigate from dashboard to Profiles/Maps and return.
   - Expected: screens render, controls remain responsive, and no exception is shown.

7. **Profile and map validation**
   - Load the sample Stage 1 profile and inspect its map.
   - Try a valid numeric map value and an out-of-range value.
   - Expected: valid values are accepted; invalid values are rejected with a useful validation message.

8. **Backup and restore**
   - Create a profile backup, change the profile, then restore the backup.
   - Expected: restored JSON matches the backup content.

9. **Automated test launcher**
   - Run ecu_test.bat.
   - Expected: Python 3.11 check, pip check, compileall and pytest all pass.

10. **Local executable build**
    - Run build_exe.bat.
    - Expected: dist\ECUProTune\ECUProTune.exe and the versioned release ZIP are created.
    - Expected: unrelated content under dist is preserved.

11. **Executable file properties**
    - Run:
      
          (Get-Item .\dist\ECUProTune\ECUProTune.exe).VersionInfo | Format-List FileVersion,ProductVersion

    - Expected: FileVersion and ProductVersion both show 0.1.0.0.

12. **Release ZIP extraction**
    - Extract ECUProTune-Windows-Python311-v0.1.0.zip into a directory whose path contains spaces.
    - Launch ECUProTune\ECUProTune.exe from the extracted folder.
    - Expected: application opens with the _internal directory alongside the EXE.

13. **Release integrity**
    - Compare the ZIP hash with SHA256SUMS.txt and the sha256 field in BUILD-MANIFEST.json.
    - Expected: hashes match exactly.

14. **Safety boundary**
    - Confirm the application remains in simulation/visualization mode.
    - Expected: no ECU flash, physical write, or hardware programming control is present.

## Result recording

For each case, record PASS/FAIL, Windows edition/build, CPU architecture, Python version, date, and any error output. Do not mark the release as manually accepted until these checks have actually been run on a Windows user machine.


## Structured result recording

After executing the cases on the target Windows machine, a structured JSON report can be generated from the repository root:

    powershell -NoProfile -ExecutionPolicy Bypass -File scripts\record_windows_acceptance.ps1

For every case, enter PASS, FAIL or SKIP and optionally add notes/evidence. The script records Windows edition/build, architecture, PowerShell version, Python 3.11 availability, UTC timestamp and per-case results under reports\acceptance\.

The overall result is:
- PASS only when all 14 cases are marked PASS.
- FAIL when any case is marked FAIL.
- INCOMPLETE when there are no failures but one or more cases are SKIP.

The recorder does not execute or validate the GUI checks itself. Results must reflect tests actually performed; never mark a case PASS based only on CI.


## Validar o relatório gerado

O nome do relatório inclui data, hora e milissegundos; se já existir um ficheiro com o mesmo nome, o gravador acrescenta um sufixo para nunca substituir evidência anterior.

Depois de registar os resultados, valida a estrutura, os 14 IDs/títulos, os estados permitidos, os totais recalculados, a data UTC e os metadados do ambiente:

    $report = Get-ChildItem reports\acceptance\ECUProTune-Acceptance-*.json | Sort-Object LastWriteTime -Descending | Select-Object -First 1 -ExpandProperty FullName
    powershell -NoProfile -ExecutionPolicy Bypass -File scripts\validate_windows_acceptance.ps1 -ReportPath $report

Para transformar a aceitação completa num gate com código de saída diferente de zero quando o resultado não for PASS:

    powershell -NoProfile -ExecutionPolicy Bypass -File scripts\validate_windows_acceptance.ps1 -ReportPath $report -RequirePass

O validador confirma a consistência estrutural do relatório; não executa a GUI, não verifica por si só a veracidade das notas e não substitui a revisão das evidências recolhidas durante os testes.


## Testes automáticos do validador

O Windows CI executa também:

    pwsh -NoProfile -File tests\test_windows_acceptance_validator.ps1

Este teste:
- analisa a sintaxe dos scripts PowerShell de instalação de aceitação e release;
- cria um relatório sintético 14/14 PASS e confirma que o validador o aceita com -RequirePass;
- confirma que um relatório INCOMPLETE é estruturalmente válido, mas bloqueado por -RequirePass;
- confirma que IDs duplicados e totais inconsistentes são rejeitados.

Os relatórios sintéticos existem apenas no diretório temporário do runner e são apagados no fim. Nunca são usados como evidência de aceitação manual real.


## Gate final de prontidão para release

Depois de executar os 14 casos no Windows real e validar o relatório, o gate combinado verifica:
- integridade do ZIP, manifesto, tamanho e SHA-256;
- correspondência da versão da aplicação entre o manifesto e o relatório;
- estrutura e consistência dos 14 casos;
- resultado global 14/14 PASS.

Comando, a partir da raiz do repositório:

    $report = Get-ChildItem reports\acceptance\ECUProTune-Acceptance-*.json | Sort-Object LastWriteTime -Descending | Select-Object -First 1 -ExpandProperty FullName
    powershell -NoProfile -ExecutionPolicy Bypass -File scripts\check_release_readiness.ps1 -ReleaseDirectory release -AcceptanceReport $report

O comando termina com sucesso apenas quando o pacote está íntegro e o relatório da mesma versão tem todos os 14 casos em PASS. Isto é um gate local de prontidão; não publica automaticamente uma GitHub Release nem substitui a revisão humana das evidências.
