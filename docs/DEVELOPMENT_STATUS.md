# ECU Pro Tune — Development Status

## 2026-11-15 — Windows CI verde / PR aberto
- Branch de trabalho: feature/dashboard-advanced-20261108.
- Commit validado pelo CI: ff2c609cac0ce0bd1df9b0eab04231ffa8a25671.
- GitHub Actions run #4: SUCCESS — https://github.com/AndreVazao/ecu-pro-tune/actions/runs/43427809165.
- Runner: windows-latest, Python 3.11.
- Job Windows / Python 3.11: todos os 16 passos concluídos com sucesso.
- pip check, compileall, imports, construção Tk dashboard e PyInstaller: PASS.
- Testes unitários: 4 passed in 0.02s.
- Smoke test do executável: ECUProTune.exe iniciou e permaneceu ativo durante 8 segundos.
- Artefacto publicado: ECUProTune-Windows-Python311, 53,394,215 bytes, 2.310 ficheiros.
- Executável no pacote: ECUProTune.exe (14,852,596 bytes); pacote onedir, manter todos os ficheiros e a pasta _internal.
- SHA-256 do artefacto ZIP: d535beb11fb51fb0bd59c5210d902a8d6aff84e03501f181a4bd6ba9abcb19dc.
- Retenção do artefacto até 2026-11-27.
- PR #1 aberto para main: https://github.com/AndreVazao/ecu-pro-tune/pull/1.
- PR está aberto e mergeable; não fazer merge sem autorização explícita.
- O CI valida compilação/testes e arranque breve no runner, não substitui teste visual prolongado nem valida hardware real.

## 2026-11-13 — Windows CI / Actions
- Workflow: .github/workflows/windows-ci.yml.
- Commit do workflow: 940c7ecd5c26eb9a4ea1e66935b53cba00a44d65.
- Triggers: push em main/feature/**, pull_request para main e workflow_dispatch.
- Pipeline: instalar requirements, pip check, compileall, pytest, smoke imports, construir dashboard Tkinter, build PyInstaller e upload do artefacto.
- Artefacto: ECUProTune-Windows-Python311, retenção de 14 dias.

## 2026-11-08 — Dashboard avançado
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
- Python global apresentou falha DLL com NumPy 2.4.6; usar sempre .venv.
- FFmpeg não estava no PATH no último checkpoint; GUI não depende dele.

## Segurança
A aplicação atual é gestão, visualização e simulação. Não existe driver de escrita física nem rotina de flash. Qualquer futura integração de hardware deverá ser isolada, explicitamente validada e bloqueada por defeito.

## Próximos gates
1. Rever PR #1 e obter autorização explícita antes de integrar em main.
2. Deixar o CI disparado pelo PR/documentação completar e confirmar novamente o estado verde.
3. Fazer teste visual manual no PC Windows quando estiver disponível.
4. Endurecer installer/FFmpeg.
5. Testes de integração adicionais.
6. Só depois adapters de hardware isolados e sem escrita física por defeito.
