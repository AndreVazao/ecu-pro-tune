# ECU Pro Tune — Development Status

## 2026-11-17 — PR #6 integrado / verificação real da versão Windows
- PR #6 — build: embed Windows file version metadata in executable — merged em main.
- Merge commit: 872788763e78f3272dd97f7b301d1ba3022408b3.
- CI do PR #6: run #78, 44039120682 — SUCCESS; 41 testes passaram em 0.20s.
- CI push da branch: run #77, 44039079454 — SUCCESS.
- Nova branch: feature/exe-version-verification-20261117.
- Workflow acrescenta validação real de VersionInfo do EXE após o build.
- FileVersion e ProductVersion têm de corresponder a VERSION + .0; mismatch bloqueia o pipeline antes do pacote.
- Teste estático garante que o workflow executa as duas verificações.
- PR #7 ainda por abrir.
- Segurança mantida: sem escrita física ECU, driver flash ou programação hardware.

## 2026-11-17 — PR #5 integrado / metadados Windows do executável
- PR #5 — build: add versioned Windows release archives and integrity manifests — merged em main.
- Merge commit: fc6fd26ade4b5b5c4713c1378d5e0c83d4686a48.
- CI pós-merge da main: run #63, 44038630985 — SUCCESS.
- Nova branch: feature/windows-version-metadata-20261117.
- Novo gerador scripts/generate_windows_version_info.py lê VERSION e produz build/windows_version_info.txt para PyInstaller.
- build_exe.bat e Windows CI usam --version-file; o EXE recebe FileVersion/ProductVersion 0.1.0.0 nas propriedades Windows.
- BUILD-MANIFEST.json regista também windows_file_version.
- Testes cobrem geração/sintaxe do recurso, tuple filevers/prodvers e integração no build local/CI.
- CI run #75: 44038890038 — status pending/queued no último check; ainda sem resultado confirmado.
- PR #6 foi integrado em 2026-11-17 (merge commit 872788763e78f3272dd97f7b301d1ba3022408b3).
- Segurança mantida: sem escrita física ECU, driver flash ou programação hardware.

## 2026-11-17 — PR #4 integrado / release Windows versionada
- PR #4 — build: harden Windows installer and packaging workflow — merged em main.
- Merge commit: ee82b350a6b3bb48915f595389366045082c2ab6.
- CI pós-merge da main: run #43, 44037630731 — SUCCESS.
- Nova branch: feature/release-packaging-20261117.
- Versão inicial do produto: 0.1.0; VERSION e src/version.py são mantidos sincronizados por teste.
- Janela da aplicação apresenta a versão.
- Novo scripts/package_release.ps1 valida ECUProTune.exe, a pasta _internal e VERSION; cria ZIP onedir versionado, BUILD-MANIFEST.json e SHA256SUMS.txt.
- O script calcula e verifica SHA-256; CI repete a verificação antes do upload.
- Windows CI atualizado para publicar release/ em vez da pasta de build solta.
- build_exe.bat também gera o pacote versionado localmente.
- Release ZIP: ECUProTune-Windows-Python311-v0.1.0.zip.
- SHA-256 do ZIP de release: aff9f001f9420342c07aa9e9847cfa451c7d73887bde00f6b94404a75c286740.
- GitHub Actions run #60: 44038026199 — SUCCESS.
- 39 testes passaram em 0.18s.
- pip check, compileall, imports, construção Tk, PyInstaller, verificação do EXE, smoke test de arranque, geração do ZIP, verificação SHA-256 e upload: PASS.
- Artefacto GitHub: ECUProTune-Windows-Python311, ID 14308052177, 53,129,794 bytes.
- SHA-256 do artefacto GitHub: 71c0d617d14891f2e1a0d209e8a3832e27566e228bf24cea9887c42eef03ee55.
- Retenção até 2026-12-01T07:22:53Z.
- PR #5 foi integrado em 2026-11-17 (merge commit fc6fd26ade4b5b5c4713c1378d5e0c83d4686a48).
- Segurança: gestão/visualização/simulação apenas; sem escrita física ECU nem driver de flash.

## 2026-11-17 — PR #3 integrado / installer Windows endurecido
- PR #3 — fix: harden scheduler persistence and logging behavior — merged em main.
- Merge commit: 8409dce3b6f1ddcabaa2191a34deb126908ca228.
- Nova branch: feature/windows-installer-hardening-20261117.
- Installer agora exige Python 3.11 validado, valida .venv existente, instala dependências, executa pip check e valida imports centrais.
- FFmpeg passou a ser opcional e só é instalado via winget após confirmação explícita.
- ecu_test.bat valida Python 3.11, pip check, compileall e pytest.
- build_exe.bat alinhado com CI, inclui configs/maps e recursos ttkbootstrap/matplotlib.
- Limpeza do build limitada às pastas build/ECUProTune e dist/ECUProTune; não apaga outros conteúdos de build/dist.
- README e docs/WINDOWS_INSTALL.md atualizados.
- Novos testes estáticos para os scripts Windows.
- GitHub Actions run #39: 44037045786 — SUCCESS.
- 33 testes passaram em 0.15s.
- pip check, compileall, imports, construção Tk, PyInstaller, verificação do EXE, smoke test de arranque e upload do artefacto: PASS.
- Artefacto Windows: ECUProTune-Windows-Python311, ID 14308435021, 53,396,794 bytes.
- SHA-256: fcf00546f29a068064e3d5a001168a8a4ac21b0eeb83b7c85991aacbb8325be9.
- Retenção até 2026-12-01T07:15:17Z.
- PR #4 foi posteriormente integrado em 2026-11-17 (merge commit ee82b350a6b3bb48915f595389366045082c2ab6).
- Segurança: gestão/visualização/simulação apenas; sem escrita física ECU nem driver de flash.

## 2026-11-17 — PR #2 integrado / scheduler e logging
- PR #2 — test: harden profile, map and rollback integration flows — merged em main.
- Merge commit: 0980530a17368c919f07867953e51da3dea649da.
- CI do PR #2: run #20, 44035539787 — SUCCESS.
- CI pós-merge da main: run #21, 44035795100 — SUCCESS.
- Nova branch: feature/scheduler-logging-tests-20261117.
- Scheduler endurecido: validação de perfil/data/estrutura JSON, preservação de ficheiros corrompidos, gravação atómica, execução de callbacks isolada e espera cancelável através de Event.wait.
- Testes novos: agendamento de itens, rejeição de dados inválidos, preservação de JSON corrompido, execução única de tarefas vencidas, tarefas futuras não executadas, retry após falha de callback e logging UTF-8.
- GitHub Actions run #25: 44035973794 — SUCCESS.
- 29 testes passaram em 0.12s.
- pip check, compileall, imports, construção Tk, PyInstaller, verificação do EXE, smoke test de arranque e upload do artefacto: PASS.
- Artefacto Windows: ECUProTune-Windows-Python311, ID 14306798921, 53,398,443 bytes.
- SHA-256: adc45d75bb8930a77fe25fffb083dd999c45b6ae4f1606396807bb46d0b78796.
- Retenção até 2026-12-01T07:06:49Z.
- PR #3 foi posteriormente integrado em 2026-11-17 (merge commit 8409dce3b6f1ddcabaa2191a34deb126908ca228).
- Segurança: aplicação continua apenas em gestão/visualização/simulação, sem escrita física ECU ou driver de flash.

## 2026-11-17 — PR #1 integrado / reforço de testes de integração
- PR #1 — feat: advanced simulation dashboard and Windows CI — merged em `main`.
- Merge commit: aa388679e1ea0510c66ed588d4d313e2cbe7e1ba.
- A branch `main` foi confirmada no merge commit acima.
- Nova branch de trabalho: `feature/integration-tests-20261117`, criada a partir da main já integrada.
- Commit de testes: 7f1b53e0743f049d5b3929db84ed265d062f782d.
- GitHub Actions run #18: 44035159971 — SUCCESS.
- Run URL: https://github.com/AndreVazao/ecu-pro-tune/actions/runs/44035159971.
- Testes unitários e de integração: 20 passed in 0.10s.
- Foram adicionados testes de round-trip e validação de caminhos para ProfileManager, ECUManager e RollbackManager.
- Validação de mapas numéricos rejeita NaN, infinitos, booleanos e intervalos inválidos.
- Hardening: nomes de perfil/configuração/backup e referências a mapas são validados para impedir path traversal; perfis são gravados com replace atómico e JSON não finito é rejeitado.
- pip check, compileall, import smoke test, construção Tk, build PyInstaller, verificação do EXE, smoke test de arranque e upload do artefacto: PASS.
- Artefacto Windows: ECUProTune-Windows-Python311, ID 14306118545, 53,396,254 bytes.
- SHA-256 do artefacto: 2787bc15238657ec9446f691521b03d66438178e976812a553a2e321d1cce510.
- Retenção do artefacto até 2026-12-01T07:00:26Z.
- Avisos não bloqueantes do build: matplotlib.tests sem baseline image directory, ausência de bindings Qt e aviso de transição Node 20 das actions. Build e smoke test concluíram com sucesso.
- O CI valida testes/build e arranque breve; não substitui teste visual prolongado, validação em todos os PCs ou teste com ECU física.
- Segurança: app permanece em gestão/visualização/simulação; sem escrita física ECU, sem driver flash e sem programação de ECU.

## Próximos passos
1. Abrir e validar PR #7 com verificação real da versão do EXE no Windows.
2. Teste manual do instalador e ZIP num Windows de utilizador final.
3. Expandir testes GUI sem hardware e cobertura de recuperação de ficheiros.
4. Preparar notas de release e processo de publicação, sem publicar automaticamente tags/releases.
5. Só depois avaliar adapters de hardware isolados, fail-closed e sem escrita física por defeito.

## 2026-11-15 — Windows CI verde / PR #1 aberto (histórico)
- Branch de implementação: feature/dashboard-advanced-20261108.
- Commit validado inicialmente: ff2c609cac0ce0bd1df9b0eab04231ffa8a25671.
- GitHub Actions run #4: SUCCESS — https://github.com/AndreVazao/ecu-pro-tune/actions/runs/43427809165.
- Run #6 do commit de documentação também terminou SUCCESS — https://github.com/AndreVazao/ecu-pro-tune/actions/runs/43749616835.
- PR #1 foi posteriormente integrado em 2026-11-17 (merge commit acima).
- O CodeRabbit não corre automaticamente neste repo com menos de 10 stars; isso não afeta o CI.

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
