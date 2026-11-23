# ECU Pro Tune — Development Status

## 2026-11-23 — PR #18 validation checkpoint
- PR #17 remains merged; Windows CI #162 completed successfully.
- PR #18 adds strict JSON decoding across saved/config profiles, ECU profiles, maps and scheduler persistence, with regression coverage.
- Windows CI #167 exposed one overly strict test assumption: large JSON integers are valid; the test and decoder were corrected to preserve standards-compliant arbitrary-precision integers while rejecting `NaN`, infinities and float overflow.
- Current validation: Windows CI #171 is running against the latest PR #18 head `fae181165bb0f7fcc140fe224160a1ab08a7c925`.
- PR #18 is not merged; merge remains gated on full Windows CI success.
- No ECU hardware write, flash or programming path is enabled.


## 2026-11-22 — PR #17 merged / strict JSON hardening in progress
- PR #17 — `fix: protect rollback snapshots and restore integrity` merged after Windows CI run #162 completed SUCCESS.
- Run #162 verified: Python tests, PowerShell acceptance-validator integration, clean installer smoke, imports, Tk construction, PyInstaller, EXE metadata, packaged startup, release ZIP verification and artifact upload all passed.
- Merge commit: `d0eb6b2a0c6a2ddc468ddf8b911bc626ac0d5da2`.
- New branch: `fix/strict-json-data-loading-20261122`.
- Current work hardens JSON loading to reject NaN/Infinity in saved/config profiles, ECU profiles, maps and scheduler files, and filters non-finite map arrays.
- CI validation is pending for the strict-JSON changes. No hardware ECU write, flash or programming path has been introduced.


## 2026-11-21 — Persistent checkpoint / estado consolidado
- Handoff verificado contra main: PR #12, #13, #14 e #15 estão integrados.
- PR #13 executa testes reais PowerShell para o validador de relatórios sintéticos; cobre 14/14 PASS, INCOMPLETE bloqueado por -RequirePass, IDs duplicados e totais inconsistentes.
- PR #14 smoke test do instalador em runner Windows limpo: ECU_PRO_TUNE_CI=1, cria/valida .venv, pip check e imports Python 3.11.
- PR #15 adiciona gate combinado de prontidão: integridade ZIP/manifest/hash, versão e relatório manual 14/14 PASS; chama verify_release e validate_windows_acceptance -RequirePass, sem publicar tag/release automaticamente.
- CI main run #155: SUCCESS; 53 testes Python em 0.27s; PowerShell parser/integration, instalador, .venv, Tk, PyInstaller, EXE metadata, startup smoke, ZIP, verificação independente e upload: PASS.
- SHA-256 ZIP da main: 6f8b7b0920bf00a91e263dd54714347f07309fdfb196bc600abacd5de8800e3c.
- Artefacto main ID 14674238646 (temporário, retenção até 2026-12-04); o artefacto não é release permanente.
- PC-Vazao-Anjos permanece offline na última verificação; aceitação manual real dos 14 casos continua pendente. Synthetic CI reports não são aceitação.
- Segurança: aplicação mantém gestão/visualização/simulação; sem ECU write, flash driver ou programação hardware.
- Próxima direção: expandir testes GUI e recuperação de ficheiros sem hardware, e preparar a aceitação real quando o Windows de utilizador final estiver disponível.

## 2026-11-20 — PR #15 integrado / gate combinado de prontidão
- PR #14 — ci: smoke test the Windows installer end to end — merged em main.
- Merge commit PR #14: 74903c0a6e1f6a64542a977e79b1127ca9690ef2.
- CI push run #144: 44827167408 — SUCCESS; 52 testes Python passaram em 0.39s.
- O Windows CI executa install_ecu_pro_tune.bat num runner limpo com ECU_PRO_TUNE_CI=1, cria .venv, executa pip check e valida imports Python 3.11.
- PR #14 CI run #145: 44827608921 — SUCCESS.
- Nova branch: feature/release-readiness-gate-20261120.
- Adicionado scripts/check_release_readiness.ps1: verifica integridade do ZIP, manifesto e SHA-256, compara a versão do manifesto com a versão do relatório manual e exige 14/14 PASS.
- O gate chama verify_release.ps1 e validate_windows_acceptance.ps1 -RequirePass; não publica automaticamente uma GitHub Release.
- CI push run #152: 44828225084 — SUCCESS; 53 testes Python passaram em 0.27s.
- CI PR run #153: 44828615406 — SUCCESS.
- PowerShell parser, validador de aceitação, instalador Windows, .venv, Tk, PyInstaller, EXE metadata, startup smoke, ZIP, verificação independente e upload: PASS.
- SHA-256 ZIP: f66f2e5331733d9c3448159338d4edb940c3bff6ac8ab55125737df1bd7f2cac.
- Artefacto ID 14675371712, 53,129,222 bytes; digest sha256:63f9ef2d76608aaf70ea4d1834aa4b59bff4068ce45bc5ea69baa4b67715a7aa; expira 2026-12-04T22:23:26Z.
- PR #15 — build: add a combined release readiness gate — merged em main; merge commit 68aa28ddd5e518325c06b401f613124212beebcc.
- Main CI run #155: 44829024190 — SUCCESS; 53 testes Python passaram em 0.27s; PowerShell parser/integration, instalador, .venv, Tk, PyInstaller, EXE metadata, startup smoke, ZIP, verificação independente e upload: PASS.
- Artefacto main ID 14674238646, 53,130,071 bytes; digest sha256:bbfae10fb0b41cf3018129469066f2c4f21eaf1d41501516369559edf90fcf8c; expira 2026-12-04T22:29:26Z.
- SHA-256 ZIP main: 6f8b7b0920bf00a91e263dd54714347f07309fdfb196bc600abacd5de8800e3c.
- PC-Vazao-Anjos permanece OFFLINE (última consulta 96 horas atrás); não foi possível executar aceitação manual real.
- Os relatórios sintéticos do CI não contam como aceitação. Todos os 14 casos continuam pendentes até execução no Windows de utilizador final.
- Segurança funcional mantida: sem escrita física ECU, driver flash ou programação hardware.

## 2026-11-20 — PR #13 integrado / testes reais do validador PowerShell
- PR #12 — test: validate structured Windows acceptance reports — merged em main.
- Merge commit PR #12: 1afd679306602c29a617a0f111e911ca34cd3047.
- CI PR #12 run #127: 44825379046 — SUCCESS; 49 testes passaram em 0.18s.
- Nova branch: feature/windows-acceptance-validator-ci-20261120.
- Adicionado tests/test_windows_acceptance_validator.ps1: análise sintática de quatro scripts PowerShell e execução real do validador contra relatórios sintéticos temporários.
- O teste confirma 14/14 PASS com -RequirePass, bloqueia INCOMPLETE com -RequirePass, rejeita IDs duplicados e totais inconsistentes.
- O Windows CI executa este harness antes dos smoke tests da aplicação.
- A primeira execução detetou erro de interpolação PowerShell ($caseId:); corrigido para ${caseId} e validado novamente.
- CI push run #135: 44826111889 — SUCCESS; 50 testes Python passaram em 0.21s.
- CI PR run #136: 44826505018 — SUCCESS.
- PowerShell parser e integração do validador: PASS.
- PyInstaller, EXE version metadata, startup smoke, ZIP, verificação independente e upload: PASS.
- SHA-256 ZIP: aef62d63f889c34358e1e62fc42c45395e2636b49ae872925564710f46a33c58.
- Artefacto ID 14674850402, 53,130,873 bytes; digest sha256:337d4662d6e0a1227bb57b20d3662507a03fc48c3b1f9aaddcee578815dcbae1; expira 2026-12-04T22:08:40Z.
- PR #13 — ci: execute Windows acceptance validator integration tests — merged em main; merge commit e9835b7b4b4cafc7ddcb4d60e1bce7bf98d742a1.
- Main CI run #137: 44826843675 — em execução no checkpoint.
- Aceitação manual em Windows real continua pendente; relatórios sintéticos do CI não contam como aceitação real.
- Segurança funcional: sem escrita física ECU, driver flash ou programação hardware.

## 2026-11-18 — PR #11 integrado / registo de aceitação Windows
- PR #11 — test: add structured Windows manual acceptance recorder — merged em main.
- Merge commit: f72307e2875ac60f4bec84229634a54d7f0af363.
- CI do PR #11: run #117, 44399033395 — SUCCESS; 46 testes passaram em 0.22s.
- CI pós-merge da main: run #118, 44399399468 — em execução no checkpoint.
- scripts/record_windows_acceptance.ps1 regista os 14 casos manuais com PASS/FAIL/SKIP e gera JSON com dados do ambiente.
- O relatório só resulta em PASS se os 14 casos forem efetivamente marcados PASS.
- Não executa testes GUI por si; continua a ser necessário testar num Windows real.
- Aceitação manual permanece pendente; não criar tag/release pública até completar e rever o relatório.
- Segurança: sem escrita física ECU, driver flash ou programação hardware.

## 2026-11-18 — registo estruturado de aceitação manual Windows
- PR #10 — security: reject unsafe paths in Windows release archives — merged em main.
- Merge commit: 5b9dce59f2bec0f5c9176fbd9fa9eaf2aa567391.
- CI do PR #10: run #109, 44397532910 — SUCCESS.
- CI pós-merge da main: run #110, 44397930870 — SUCCESS.
- Nova branch: feature/windows-acceptance-recorder-20261118.
- Criado scripts/record_windows_acceptance.ps1 para registar os 14 casos manuais como PASS/FAIL/SKIP.
- O relatório JSON inclui versão, timestamp UTC, Windows edition/version/build, arquitetura, PowerShell, disponibilidade Python 3.11 e notas por caso.
- Resultado global PASS apenas se os 14 casos forem PASS; FAIL se algum falhar; INCOMPLETE se existir SKIP sem FAIL.
- README e docs/ACCEPTANCE_TEST_WINDOWS.md documentam o processo.
- CI run #115: 44398214617 — SUCCESS; 46 testes passaram em 0.18s.
- PyInstaller, EXE version metadata, startup smoke test, ZIP, verificador independente e upload: PASS.
- Release ZIP SHA-256: 275a871dc5fbc90b1257710236daeb2a8dafe3ddd9c8a950245f0dd83a1e28b4.
- GitHub artifact ID 14471692980, 53,129,769 bytes; digest 4b2de2a29fb668ee401ef774e3f760dd95440647b3deb06970049a82029c2c3f; expira 2026-12-02T21:09:24Z.
- PR #11 integrado em 2026-11-18 (merge commit f72307e2875ac60f4bec84229634a54d7f0af363).
- Aceitação manual real continua pendente; o script apenas regista resultados introduzidos pelo utilizador e não simula execução.
- Segurança: sem escrita física ECU, driver flash ou programação hardware.

## 2026-11-18 — segurança de caminhos dentro do ZIP de release
- PR #9 — build: independently verify Windows release integrity — merged em main.
- Merge commit: 6baca49faff34b97d88b2b9c783fd987752ba1bf.
- CI do PR #9: run #102, 44396154831 — SUCCESS.
- CI pós-merge da main: run #103, 44396501334 — SUCCESS; 45 testes passaram em 0.21s.
- Nova branch: feature/release-archive-path-safety-20261118.
- Verificador agora rejeita caminhos absolutos, segmentos . e .., caminhos fora de ECUProTune/ e entradas ZIP duplicadas.
- Confirma ainda que ECUProTune.exe existe e não está vazio, e que _internal contém ficheiros.
- Teste regressivo cobre traversal, duplicados e layout do ZIP.
- GitHub Actions run #107: 44396707008 — SUCCESS.
- 45 testes passaram em 0.21s.
- Build PyInstaller, versão EXE, smoke test, empacotamento, verificação independente e upload: PASS.
- SHA-256 do ZIP: 92ca165e0f8dfb554228a5fd68e365fb306297fde9cf5a53404fbfa57d741a1c.
- Artefacto GitHub ID 14471276293, 53,128,733 bytes; digest sha256:91f6304821a9f39febebaf90287193b18db2f671b99235efb66b269e8f071e5e; expira 2026-12-02T21:00:51Z.
- PR #10 a abrir após CI da atualização documental.
- Aceitação manual em Windows real continua pendente; não criar tag/release pública ainda.
- Segurança funcional ECU mantida: sem escrita física, flash driver ou programação hardware.

## 2026-11-18 — Verificador independente de integridade da release
- Main CI run #94, 44040965817 — SUCCESS após merge do PR #8.
- Nova branch: feature/release-integrity-verifier-20261118.
- Adicionado scripts/verify_release.ps1 para verificar produto, versão, plataforma, versão Windows, nome do ZIP, tamanho, SHA-256 no manifesto e SHA256SUMS.txt.
- O verificador também abre o ZIP e confirma ECUProTune/ECUProTune.exe e conteúdo PyInstaller em ECUProTune/_internal/.
- Windows CI executa a verificação independente após empacotar e antes de carregar o artefacto.
- README e docs/RELEASE_PACKAGING.md documentam o comando de verificação.
- Novos testes estáticos cobrem a verificação e a ordem do workflow.
- GitHub Actions run #100: 44395319597 — SUCCESS.
- 44 testes passaram em 0.21s.
- Build PyInstaller, metadados EXE, smoke test de arranque, ZIP, verificação independente, SHA-256 e upload: PASS.
- SHA-256 do ZIP de release: 9b7156513b9d2526820c65a81d72dbd05dc5c970057941418ecbe110de17bbd2.
- Artefacto GitHub ID 14471145182, 53,130,269 bytes; digest do artefacto: f60e833192b762d7eba9842508ea6b188f94a31aa37b112fffe5f8da737ba2bf; expira 2026-12-02T20:52:59Z.
- PR #9 a abrir após validar a atualização documental.
- Aceitação manual num Windows de utilizador final continua pendente; não publicar tag/release nem declarar v0.1.0 manualmente aceite.
- Segurança: sem escrita física ECU, driver de flash ou programação hardware.

## 2026-11-17 — PR #7 integrado / preparação de aceitação 0.1.0
- PR #7 — ci: verify embedded Windows executable version metadata — merged em main.
- Merge commit: 227f73821e7c2d5f261bd9ec8e613de51cbe5c15.
- CI do PR #7: run #86, 44040161974 — SUCCESS; 42 testes passaram em 0.18s.
- CI push da branch: run #85, 44039854917 — SUCCESS.
- CI verifica FileVersion e ProductVersion do EXE real e confirma 0.1.0.0.
- Nova branch: feature/release-acceptance-20261117.
- CHANGELOG.md criado para 0.1.0.
- docs/ACCEPTANCE_TEST_WINDOWS.md criado com 14 casos manuais: instalação, venv, FFmpeg opcional, dashboard, navegação, mapas, backup/restore, build, version info, ZIP, hash e fronteira de segurança.
- README liga changelog, plano manual e guia de empacotamento.
- Não declarar aceitação manual nem publicar release/tag até executar o plano num Windows de utilizador final.
- Segurança: sem escrita física ECU, driver flash ou programação hardware.

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
1. Abrir e validar PR #8 com changelog e plano de aceitação manual.
2. Executar os 14 casos de aceitação num Windows de utilizador final antes de publicar release.
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
