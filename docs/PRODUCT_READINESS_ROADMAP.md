# ECU Pro Tune — Roadmap global de prontidão

**Auditoria:** 26-11-2026 (UTC)  
**Repositório:** [AndreVazao/ecu-pro-tune](https://github.com/AndreVazao/ecu-pro-tune)  
**Branch principal confirmada:** `main`  
**SHA da main no início da auditoria:** `d0eb6b2a0c6a2ddc468ddf8b911bc626ac0d5da2`  
**SHA atual após PR #23:** `6670fd2e4b89303927fb0b1915b919f54e3f298c`  
**Versão declarada:** 0.1.0

Este documento acompanha o produto completo, não apenas uma PR ou branch. Os estados são baseados em código, documentação, API do GitHub e resultados de CI observados. «Implementado» não significa aceitação manual nem validação em ECU.

## Estado global

**Classificação:** protótipo desktop / demonstração simulada; ainda não aceite para release de utilizador final.

| Área | Estado | Evidência / lacuna |
|---|---|---|
| GUI desktop | Implementada | ttkbootstrap/Tk; CI constrói o dashboard; falta aceitação interativa em Windows de utilizador |
| Performance / Showcase | Implementados | Modos presentes na seleção e dashboard |
| Dashboard | Simulação local | RPM e load em séries distintas com escalas explícitas; janela nominal 36 s; sem telemetria real |
| Perfis e mapas | Implementados | JSON, editor numérico, validação e carregamento; validação manual pendente |
| Backup / rollback | Implementados | cópia/restauro, nomes seguros, backup sem sobrescrever no mesmo segundo e testes de backup corrompido |
| Scheduler | Core + GUI simulada | Gestão de agendamentos na GUI: listar, criar, atualizar e cancelar; callbacks apenas simulados, sem escrita ECU |
| Logs | Implementados | Rotação UTF-8; falhas de callback/storage do Scheduler registadas com traceback e retry pendente |
| Instalação | CI validado | smoke do instalador em Windows CI; instalação no PC de utilizador por confirmar |
| Build / pacote | CI validado | PyInstaller onedir, metadados Windows, ZIP, manifest e SHA-256 |
| Aceitação manual | PENDENTE | 14 casos; não existe relatório de aceitação real 14/14 PASS no repositório |
| Release publicada | NÃO | API de GitHub Releases devolveu lista vazia nesta auditoria |
| Hardware ECU | FORA DO ÂMBITO ATUAL | Sem driver de escrita, flash ou programação; nenhuma validação física efetuada |

## Arquitetura observada

- **Interface:** `src/app` — seleção de modo, dashboard, navegação para perfis/mapas.
- **Serviços core:** `src/core` — ECUManager (ficheiros de configuração e mapas), ProfileManager, RollbackManager, Scheduler, SoundManager e Logger.
- **Tuning / visualização:** `src/tuning` — editor de mapas numéricos, validators, live graphs e tuning panel.
- **Dados:** `configs/`, `maps/`, perfis guardados, backups, scheduler e logs locais em JSON/ficheiros.
- **Empacotamento:** instalador Windows baseado em Python 3.11, build PyInstaller onedir, ZIP versionado, manifest e checksum.
- **CI:** `.github/workflows/windows-ci.yml` — Windows latest / Python 3.11, dependências, pip check, compileall, pytest, PowerShell acceptance-validator, installer smoke, imports, construção Tk, EXE, startup smoke, pacote e verificação independente.
- **Integrações:** não foi observado backend, API de telemetria, driver de ECU, flashing, escrita de hardware nem ligação a veículo.

## Evidência GitHub desta auditoria

- Main atual: `6670fd2e4b89303927fb0b1915b919f54e3f298c` após integração de PR #23 em 26-11-2026.
- PR #18 — [strict JSON/profile loading](https://github.com/AndreVazao/ecu-pro-tune/pull/18): integrada em 26-11-2026 no commit `1fae378641740ab9ca61900dc3f24df5c514d885`; CI Windows run [45499716011](https://github.com/AndreVazao/ecu-pro-tune/actions/runs/45499716011) SUCCESS; 75 testes passaram.
- PR #21 — [Scheduler diagnostics](https://github.com/AndreVazao/ecu-pro-tune/pull/21): integrada; CI #181 SUCCESS, 73 testes PASS.
- PR #22 — [dashboard RPM + load](https://github.com/AndreVazao/ecu-pro-tune/pull/22): integrada; CI #182 SUCCESS, 77 testes PASS.
- PR #23 — [Scheduler GUI](https://github.com/AndreVazao/ecu-pro-tune/pull/23): integrada; CI #183 SUCCESS, 78 testes PASS. Main push CI #45761702198 em execução neste checkpoint.
- A proteção formal de `main` não foi reavaliada nesta ronda.
- Issues independentes abertas: não reavaliadas neste checkpoint.
- CI main: run [45049828933](https://github.com/AndreVazao/ecu-pro-tune/actions/runs/45049828933) SUCCESS; run #155 [45049828933](https://github.com/AndreVazao/ecu-pro-tune/actions/runs/45049828933) foi revalidado: 59 testes passaram em 0.23s; build/package gates também SUCCESS.
- Releases: lista vazia. A listagem de tags não foi suportada pelo endpoint/fetch utilizado; tags não ficam confirmadas nesta ronda.
- Dependências: `requirements.txt` tem versões parcialmente fixadas e ranges, mas não existe lockfile completo identificado.

## Critérios objetivos para ECU Pro Tune 0.1.0

### Gate A — Core e segurança de dados

- [x] Perfil/mapa/backup/scheduler com validação básica e testes de regressão existentes.
- [x] Backup/restauro com validação de caminho e preservação de backup inválido.
- [ ] PR #18 de JSON estrito integrada, com CI verde no head final.
- [ ] Testes de recuperação e integridade de dados abrangendo todos os fluxos de leitura/gravação relevantes.
- [ ] Diagnóstico de falhas de scheduler verificável em logs (branch independente em curso).

### Gate B — UX e operação desktop

- [x] Modos Performance e Showcase.
- [x] Dashboard de simulação, navegação e painel de perfis/mapas.
- [ ] Aceitação interativa dos 14 casos em Windows real.
- [x] Agendamento disponível na interface com listagem, criação, estado, cancelamento e feedback; execução do callback permanece explicitamente simulada.
- [ ] Corrigir discrepâncias de UI documentadas/confirmadas durante revisão (por exemplo, a legenda do gráfico afirma RPM + load, mas o histórico desenhado contém apenas RPM; a duração indicada também deve corresponder à cadência real).

### Gate C — Instalação e distribuição

- [x] Installer smoke no runner Windows.
- [x] CI verifica dependências, imports, GUI construction, build PyInstaller, metadados EXE e arranque breve.
- [x] Empacotamento versionado e verificação independente de ZIP/manifest/SHA-256.
- [ ] Testes manuais de instalação, extração em caminho com espaços e operação prolongada em Windows de utilizador.
- [ ] Relatório de aceitação manual 14/14 PASS; o gate não pode ser satisfeito por relatório sintético.
- [ ] Rever e aprovar release notes, pacote e checksum antes de qualquer publicação; publicar apenas com aprovação explícita.

### Gate D — Segurança e limites de produto

- [x] Código/documentação confirmam simulação e visualização; não foi observado caminho de escrita física ou flash.
- [x] CI e testes permanecem em fixtures, dados sintéticos e ambiente Windows de build.
- [ ] Avaliação de segurança/dependências e processo de atualização/release documentados com evidência.
- [ ] Qualquer integração futura com ECU exige autorização explícita, arquitetura isolada, fail-closed, bancada identificada e plano de validação próprio. Não é um critério para aceitar a versão simulada e não deve ser implementada implicitamente.

## Próximas frentes independentes

1. **Revisão de integridade de dados:** PR #18 integrada; ampliar testes de recuperação e integridade em todos os fluxos de leitura/gravação.
2. **Diagnóstico operacional:** PR #21 integrada; strict JSON e logging de callback/storage estão na main, com 73 testes PASS no CI #181.
3. **Correção UX do dashboard:** tornar legenda e janela temporal do gráfico RPM precisas, ou implementar a segunda série de load com escala explicitamente definida e testes.
4. **Scheduler UX:** PR #23 integrada; próxima melhoria é validação interativa e usabilidade em Windows real.
5. **Aceitação manual:** executar e registar os 14 casos em Windows real quando o ambiente estiver disponível; não marcar PASS por inferência.

## Regra de conclusão

A prontidão 0.1.0 só é declarada quando os gates A–C estiverem satisfeitos, a aceitação manual real for 14/14 PASS, o relatório tiver evidência e o pacote/version/hash corresponderem. CI verde, preview, artefacto temporário ou testes sintéticos, isoladamente, não equivalem a release aceite. Não publicar tag/release nem iniciar hardware sem aprovação explícita.
