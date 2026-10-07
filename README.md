# ECU Pro Tune

Aplicação desktop Python para gestão visual de perfis de calibração automóvel, edição de mapas, visualização de curvas, backups, rollback e apresentação operacional.

## Estado atual

- GUI ttkbootstrap funcional.
- Modos Performance e Showcase.
- Dashboard com telemetria simulada.
- Gestor de perfis e mapas.
- Editor de mapa numérico com validação.
- Gráfico live com matplotlib.
- Backup de perfis.
- Testes automatizados.
- Ambiente virtual isolado.
- Nenhuma escrita física de ECU nesta fase.

## Instalação Windows

Executar:

install_ecu_pro_tune.bat

Depois:

.venv\Scripts\python.exe -m src.app.main

## Testes

ecu_test.bat

ou:

.venv\Scripts\python.exe -m pytest -q tests

## Build

build_exe.bat

## Arquitetura

src/app      interface e dashboard
src/core     serviços centrais
src/tuning   mapas, validação e gráficos
src/utils    paths e utilitários
configs      perfis
maps         mapas
tests        testes
docs         documentação

## Segurança

O software atual trabalha em modo de gestão/simulação. Não existe driver de escrita física nem rotina de flash. Qualquer futura integração de hardware deverá ser isolada, explicitamente validada e bloqueada por defeito.

## Roadmap imediato

1. Sons e fallback.
2. Installer com verificação de FFmpeg.
3. Dashboard avançado.
4. Gestão de perfis completa.
5. Empacotamento EXE.
6. Testes de integração.
7. Adapters de hardware somente depois dos gates anteriores.
