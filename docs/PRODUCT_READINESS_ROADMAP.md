# ECU Pro Tune — Roadmap global de prontidão

**Auditoria:** 27-11-2026 (UTC)  
**Repositório:** [AndreVazao/ecu-pro-tune](https://github.com/AndreVazao/ecu-pro-tune)  
**Branch principal:** `main`  
**SHA confirmado:** `574813fb3ad8f90ad5f34af0a7fd2967c2c8d4ee`  
**Versão declarada:** 0.1.0

Este roadmap é reconciliado com código, documentação, GitHub e CI. Não confunde funcionalidades implementadas com aceitação manual, release publicada ou validação física.

## Estado global

**Classificação:** protótipo desktop/simulador funcional; ainda não aceite para distribuição final a utilizadores.

| Área | Estado | Evidência / lacuna |
|---|---|---|
| GUI desktop | Implementada | ttkbootstrap/Tk; Windows CI constrói dashboard e painel Scheduler; aceitação interativa de utilizador pendente |
| Modos Performance / Showcase | Implementados | Seleção de modo e apresentação no dashboard |
| Dashboard | Simulação | RPM + load em séries e escalas separadas; janela nominal 36 s; não é telemetria real |
| Perfis / mapas | Implementados | JSON estrito, editor numérico e validação; aceitação manual pendente |
| Backup / rollback | Implementados | Backup/restauro com validação e preservação de ficheiros inválidos; CI/testes |
| Scheduler | Core + GUI simulada | Listar, criar, cancelar e refrescar; não há edição de agendamento na GUI; callback apenas regista conclusão simulada |
| Logging | Implementado | Rotação UTF-8; falhas callback/storage com traceback e retry; dados ilegíveis preservados |
| Instalação | CI validado | Smoke em runner Windows limpo; instalação e operação prolongada no PC do utilizador ainda pendentes |
| Build / pacote | CI validado | PyInstaller onedir, versão EXE, ZIP, manifest e SHA-256 |
| Aceitação manual | PENDENTE | 15 casos; não existe relatório real 15/15 PASS |
| Release GitHub | NÃO PUBLICADA | Lista de releases consultada vazia |
| Tags | NÃO CONFIRMADAS | Endpoint de tags/refs não foi disponibilizado nesta verificação; não assumir inexistência |
| Hardware ECU | FORA DO ÂMBITO | Sem driver de escrita, flashing ou ligação a ECU; não testado em hardware |

## Arquitetura observada

- **Interface:** `src/app` — seleção de modo, dashboard, navegação e painel Scheduler.
- **Core:** `src/core` — ECUManager, ProfileManager, RollbackManager, Scheduler, SoundManager e Logger.
- **Tuning/visualização:** `src/tuning` — editor numérico, validators, graphs e tuning panel.
- **Dados locais:** `configs/`, `maps/`, perfis guardados, backups, Scheduler e logs; ficheiros JSON.
- **Instalação/build:** Python 3.11, ambiente virtual, installer batch, PyInstaller onedir e ZIP versionado.
- **CI:** `.github/workflows/windows-ci.yml` — dependências, pip check, compileall, pytest, PowerShell acceptance validator, installer smoke, imports, Tk construction, EXE build/metadata/startup, ZIP e verificação independente.
- **Integrações:** não foi observado backend, API de telemetria, driver ECU, flashing, escrita física ou ligação a veículo.

## Revalidação GitHub

- Main: `574813fb3ad8f90ad5f34af0a7fd2967c2c8d4ee`, commit de 26-11-2026; CI push run #200 [45761769528](https://github.com/AndreVazao/ecu-pro-tune/actions/runs/45761769528) **SUCCESS**.
- Run #200: **78 testes passaram**, 14 warnings; compileall, PowerShell validator, installer smoke, imports, Tk, PyInstaller, EXE metadata, packaged startup, ZIP, independent verification e artifact upload PASS.
- Artefacto CI #200: [15089144559](https://github.com/AndreVazao/ecu-pro-tune/actions/runs/45761769528/artifacts/15089144559), temporário (14 dias); não é release permanente.
- PR #18 strict JSON: merged; run #173 [45499716011](https://github.com/AndreVazao/ecu-pro-tune/actions/runs/45499716011) SUCCESS, 75 testes.
- PR #21 Scheduler diagnostics: merged; run #181 [45760421245](https://github.com/AndreVazao/ecu-pro-tune/actions/runs/45760421245) SUCCESS, 73 testes.
- PR #22 dashboard RPM + load: merged; run #182 [45760551886](https://github.com/AndreVazao/ecu-pro-tune/actions/runs/45760551886) SUCCESS, 77 testes.
- PR #23 Scheduler GUI: merged; run #183 [45761454999](https://github.com/AndreVazao/ecu-pro-tune/actions/runs/45761454999) SUCCESS, 78 testes.
- PRs #19 e #20 foram fechadas sem merge; o trabalho reconciliado foi integrado por #21 e #22. PR #24 está aberta para sincronizar a aceitação manual do Scheduler.
- PR #24 — CI Windows run #206 [45933164869](https://github.com/AndreVazao/ecu-pro-tune/actions/runs/45933164869) SUCCESS no head `15a51e59821209a58931f7a244518464f73673a2`: 78 testes PASS, 14 warnings; PowerShell acceptance harness, installer, imports/Tk, PyInstaller, EXE metadata, startup, ZIP e verificação independente PASS. Artefacto temporário [15170310009](https://github.com/AndreVazao/ecu-pro-tune/actions/runs/45933164869/artifacts/15170310009), SHA-256 `38c8ff1fa4db6531d2b48a9b319ba6894559387bada81e2bd5cb67ad15d71266`, expira 11-12-2026.
- Issues abertas: 0 na API consultada.
- Branches: 25 agora (24 no snapshot da main antes da branch da PR #24), incluindo main e branches históricas. API indicou `protected=false` em todas as branches devolvidas; proteção formal da main não confirmada. Branches históricas não foram eliminadas.
- Releases: 0 na listagem. Tags não confirmadas, devido à falha/indisponibilidade do endpoint de tags.

## Critérios de prontidão 0.1.0

### Gate A — Core e integridade de dados

- [x] Perfil/mapa/backup/rollback com validação e testes.
- [x] JSON estrito integrado.
- [x] Scheduler com persistência, IDs novos, compatibilidade legacy, locking, cancelamento e logging.
- [ ] Expandir testes de recuperação e integridade em todos os fluxos de leitura/escrita; revisar concorrência e corrupção.
- [ ] Avaliar segurança/dependências e documentar política de atualização.

### Gate B — UX e operação desktop

- [x] Modos Performance e Showcase.
- [x] Dashboard simulado com RPM/load e janela temporal coerentes.
- [x] GUI Scheduler: listar, criar, cancelar, estado, refresh automático; execução é somente simulada.
- [ ] Aceitação interativa dos 15 casos em Windows real, incluindo Scheduler.
- [ ] Avaliar experiência prolongada, responsividade e mensagens de erro no PC de utilizador.

### Gate C — Instalação e distribuição

- [x] Installer smoke em Windows CI e pip check.
- [x] Import/Tk construction e startup smoke do EXE.
- [x] Build PyInstaller, metadata, ZIP, manifest, SHA-256 e verificação independente.
- [ ] Instalação/extração e operação prolongada no Windows do utilizador.
- [ ] Relatório de aceitação real 15/15 PASS.
- [ ] Revisão/aprovação explícita das release notes, pacote e checksum; publicação não automática.

### Gate D — Segurança e limites de ECU

- [x] Código e documentação permanecem em simulação/gestão; não há driver flash nem escrita física observada.
- [x] CI usa fixtures e runner de build; não liga ECU ou veículo.
- [ ] Qualquer futura integração de hardware exige autorização explícita, arquitetura isolada, fail-closed, bancada claramente identificada, procedimento e validação próprios. Não é requisito implícito desta versão simulada.

## Próximas frentes independentes

1. **Aceitação Windows:** executar e registar os 15 casos reais; nunca usar fixture CI como aceitação do utilizador.
2. **Integridade:** ampliar testes de corrupção/recuperação de perfis, mapas, backups e scheduler; investigar concorrência de persistência.
3. **Dependências:** avaliar ranges atuais e lock/constraints reproduzíveis; sem atualizar dependências automaticamente nem criar custos.
4. **Operação desktop:** avaliar logs, erros e operação prolongada no Windows de utilizador.
5. **Release:** rever versão, changelog, pacote e hash apenas depois de gates; aguardar aprovação explícita.

## Regra de conclusão

A prontidão 0.1.0 só é declarada quando os gates A–C estiverem satisfeitos, a aceitação manual real for 15/15 PASS, o relatório tiver evidência verificável e pacote/version/hash corresponderem. CI verde, preview ou artefacto temporário não substituem aceitação manual. Hardware ECU permanece fora do âmbito sem autorização explícita.
