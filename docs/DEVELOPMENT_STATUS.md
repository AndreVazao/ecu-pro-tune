# ECU Pro Tune — Development Status

## 2026-11-13 — Windows CI / Actions (em execução após push)
- Branch de trabalho: feature/dashboard-advanced-20261108.
- Workflow: .github/workflows/windows-ci.yml.
- Commit do workflow: 2cfbbb2d16ada4c32eaaacda2c1f293e8479cae3.
- Runner: windows-latest, Python 3.11.
- Pipeline: instalar requirements, pip check, compileall, pytest, smoke imports, construir dashboard Tkinter, build PyInstaller e upload do artefacto.
- Artefacto: ECUProTune-Windows-Python311, retenção de 14 dias.
- Triggers: push em main/feature/**, pull_request para main e workflow_dispatch.
- A execução ainda precisa de terminar para confirmar o resultado; a criação/publicação do YAML não equivale a testes aprovados.

## 2026-11-08 — Dashboard avançado (em validação)
- Commit de implementação: 6d28e3c.
- Dashboard atualizado com seis métricas simuladas, medidores circulares RPM/boost, gráfico rolling de RPM e monitor de sistema.
- Navegação para Perfis/Mapas mantida; foi adicionada ação para regressar ao dashboard.
- Atualização de telemetria limitada a 400 ms; histórico limitado a 90 amostras.
- Identidade visual azul/ciano/preto/cinza, sem dependências novas.
- Segurança mantida: apenas simulação local; sem escrita física, driver ECU ou rotina de flash.

## Checkpoints anteriores
- Repo: AndreVazao/ecu-pro-tune.
- Base GUI: b6900ed — feat: build ECU Pro Tune GUI foundation.
- Som: 8762de4 — feat: harden sound service with wav fallback.
- Documentação de som: adfe003 — docs: record sound fallback checkpoint.
- AndreOS Memory: b232848 — docs: update ECU Pro Tune sound checkpoint.
- Diretório local não versionado andreos-memory foi preservado.

## Implementação existente
- GUI ttkbootstrap com modos Performance e Showcase.
- ProfileManager, ECUManager, Scheduler, RollbackManager, SoundManager e Logger.
- MapEditor, validators e live graph.
- Perfil Stage 1 e mapa de demonstração.
- SoundManager fail-safe: MP3 quando disponível, WAV fallback no Windows e backend ausente não bloqueia a GUI.
- Gerador stdlib de 12 cues WAV fallback, 6 por modo, sem dependência de FFmpeg.
- Ambiente .venv isolado com NumPy 1.26.4 e Matplotlib 3.9.4.
- Installer, scripts de teste e build Windows.

## Ambiente e validação anterior
- Testes anteriores: 4 passed.
- compileall anterior: PASS.
- Python global apresentou falha DLL com NumPy 2.4.6; usar sempre .venv.
- FFmpeg não estava no PATH no último checkpoint; GUI não depende dele.

## Segurança
A aplicação atual é gestão, visualização e simulação. Não existe driver de escrita física nem rotina de flash. Qualquer futura integração de hardware deverá ser isolada, explicitamente validada e bloqueada por defeito.

## Próximos gates
1. Acompanhar o primeiro run do Windows CI; corrigir falhas no pipeline ou na aplicação.
2. Confirmar que o EXE inicia no runner e que o artefacto fica disponível.
3. Abrir PR da branch para main só depois de CI verde e revisão dos resultados.
4. Endurecer installer/FFmpeg.
5. Testes de integração adicionais.
6. Só depois adapters de hardware isolados e sem escrita física por defeito.
