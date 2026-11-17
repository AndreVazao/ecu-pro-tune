# ECU Pro Tune

Aplicação desktop Python para gestão visual de perfis de calibração automóvel, edição de mapas, visualização de curvas, backups, rollback e apresentação operacional.

## Estado atual

- GUI ttkbootstrap funcional.
- Modos Performance e Showcase.
- Dashboard com telemetria simulada.
- Gestor de perfis e mapas.
- Editor de mapa numérico com validação.
- Gráfico live com matplotlib.
- Backup de perfis e rollback.
- Scheduler com persistência validada.
- Testes automatizados e Windows CI.
- Ambiente virtual isolado.
- Nenhuma escrita física de ECU nesta fase.

## Instalação Windows

Requisito validado: **Python 3.11**, instalado com o Python Launcher (py).

1. Executa install_ecu_pro_tune.bat.
2. O instalador cria ou valida .venv, instala as dependências e executa pip check.
3. FFmpeg é opcional. O instalador não o instala sem confirmação; a GUI e os sons WAV de fallback funcionam sem FFmpeg.

Arranque:

    .venv\Scripts\python.exe -m src.app.main

Guia detalhado: docs/WINDOWS_INSTALL.md.

## Testes

Executa ecu_test.bat.

Ou diretamente:

    .venv\Scripts\python.exe -m pytest -q tests

## Build Windows

Executa build_exe.bat. O build inclui os diretórios configs e maps, além dos recursos de ttkbootstrap e matplotlib.

O resultado é dist\ECUProTune\ECUProTune.exe. Distribui a pasta completa, incluindo _internal; não copies apenas o EXE.

## Arquitetura

- src/app: interface e dashboard
- src/core: serviços centrais
- src/tuning: mapas, validação e gráficos
- src/utils: paths e utilitários
- configs: perfis
- maps: mapas
- tests: testes
- docs: documentação

## Segurança

O software atual trabalha em modo de gestão/simulação. Não existe driver de escrita física nem rotina de flash. Qualquer futura integração de hardware deverá ser isolada, explicitamente validada e bloqueada por defeito.
